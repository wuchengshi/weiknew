#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 导入pymysql模块
import pymysql
from urllib.request import quote, unquote
import random,sys
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool #使用进程池，多进程来爬取数据更高、更快、更强

def getFirstPic(url):
    '''通过url 获取文章的封面图片地址'''
    #url = "https://mp.weixin.qq.com/s?__biz=MjM5MjAxNDM4MA==&mid=2666274393&idx=1&sn=01364fd7b39f514b5892770cce9bbc54&chksm=bdb4771a8ac3fe0c324d88b6e0d5c098b3acf5b700b701cfe493120a8e68b3b3467881bc6eff"
    page = requests.get(url)
    #print(page.status_code)
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup.prettify())
    tb = soup.find_all('meta')
    if len(tb) < 9:
        return 'null1'
    list1 = str(tb[8]).split('meta')
    if len(list1) < 4:
        return 'null2'
    list2 = list1[3].split('"')
    return list2[1]

def getArticle(url):
    '''通过url 获取文章简介'''
    pass

def getJson(type='总榜'):
    '''开始爬取数据，根据出入 type 参数，获取各种类型的数据并以列表形式返回'''
    # quote 将单个字符串编码转化为 %xx 的形式
    # strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
    baidu_cat = quote(type).strip()
    refer_url = 'https://data.wxb.com/rankArticle'
    ajax_url = 'https://data.wxb.com/rank/article?baidu_cat=%s&baidu_tag=&page=1&pageSize=50&type=2&order='%baidu_cat

    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'data.wxb.com',
        'Referer': refer_url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    try:
        resp = requests.get(ajax_url, headers=headers)
        if resp.status_code == 200:
           pass # print(resp.json())  #解析内容为json返回
    except requests.ConnectionError as e:
        print('Error',e.args) #输出异常信息

    result = resp.json()
    count = 0
    data = []
    fields = ['account','title','url','img','update_time','wx_origin_id','big_type']
    for item in result['data']:
        if count >= 10:  # 只取前10条数据
            break
        ones = []
        for field in fields:
            if field in item:
                ones.append(item[field])
            elif field is 'img':
                ones.append(getFirstPic(item['url']))
            elif field is 'big_type':
                ones.append(type)
            else:
                item[field] = ''
                ones.append(item[field])
        data.append(tuple(ones))
        count += 1
    print(count)
    return data # print(data) # sys.exit()

if __name__ == '__main__':
    #Ltype = ['总榜','国际','体育','娱乐','社会','财经','时事','科技','情感','汽车','教育','时尚','游戏','军事','旅游','美食','文化','健康','养生','搞笑','家居','动漫','宠物','母婴','育儿','星座','运势','历史','音乐']
    Ltype = ['总榜','国际','体育','娱乐','社会','财经','时事','科技','情感','汽车','教育','时尚','游戏','军事','旅游','美食','文化','健康','养生','搞笑','家居','动漫','母婴','育儿','历史','音乐']
    p = Pool(1)
    LL = []
    for i in Ltype:
        data = p.apply_async(getJson,(i,)) #使用进程池来调用函数
        LL.append(data) #每个进程函数的返回值存入列表LL
    p.close() #关闭进程池
    p.join() #回收进程池中进程

    # 连接database
    conn = pymysql.connect(host='127.0.0.1', user='root', password='root', database='weiknew', charset='utf8')
    # 得到一个可以执行SQL语句并且将结果作为字典返回的游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "truncate netdatas" #清空表
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print("mysql truncate error:")
        print(e)
        conn.rollback()  # 有异常，回滚事务

    for ii in LL:
        print(type(ii))
        data = ii.get()
        # 定义要执行的SQL语句
        sql = "INSERT INTO netdatas(account, title, url, img, update_time, wx_origin_id, big_type) VALUES (%s, %s, %s, %s, %s, %s, %s);"  # data = [("Alex", '111', '44'), ("Egon", '22', '44'), ("Yuan", '33', '44')]
        try:
            cursor.executemany(sql, data)  # 批量执行多条插入SQL语句
            conn.commit()  # 提交事务
        except Exception as e:
            print("mysql error:")
            print(e)
            conn.rollback()  # 有异常，回滚事务
    cursor.close()
    conn.close()
    print("程序结束")



