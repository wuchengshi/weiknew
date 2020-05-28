import sys
import requests
from urllib import parse
from lxml import etree
import pymysql

class DataSpider(object):
    def __init__(self):
        self.headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'data.wxb.com',
            'Referer': 'https://data.wxb.com/rankArticle',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        }

     #获取响应内容
    def get_page(self,type):
        url = 'https://data.wxb.com/rank/article?baidu_cat=%s&baidu_tag=&page=1&pageSize=50&type=2&order=' % parse.quote(type)
        try:
            resp = requests.get(url, headers=self.headers)
            if resp.status_code == 200:
                self.data = resp
                #pass  # print(resp.json())  #解析内容为json返回
        except requests.ConnectionError as e:
            print('Error', e.args)  # 输出异常信息
        return self.parse_page(type)

    #解析，提取数据
    def parse_page(self,type):
        result = self.data.json()
        count = 0
        data = []
        fields = ['account', 'title', 'url', 'img', 'update_time', 'wx_origin_id', 'big_type']
        for item in result['data']:
            if count >= 10:  # 只取前10条数据
                break
            ones = []
            for field in fields:
                if field in item:
                    ones.append(item[field])
                elif field is 'img':
                    ones.append(self.getFirstPic(item['url']))
                elif field is 'big_type':
                    ones.append(type)
                else:
                    item[field] = ''
                    ones.append(item[field])
            data.append(tuple(ones))
            count += 1
        print(count)
        return data  # print(data) # sys.exit()

    def getFirstPic(self,url):
        '''通过url 获取文章的封面图片地址'''
        # url = "https://mp.weixin.qq.com/s?__biz=MjM5MjAxNDM4MA==&mid=2666274393&idx=1&sn=01364fd7b39f514b5892770cce9bbc54&chksm=bdb4771a8ac3fe0c324d88b6e0d5c098b3acf5b700b701cfe493120a8e68b3b3467881bc6eff"
        page = requests.get(url)
        html = etree.HTML(page.content)
        html_data = html.xpath('/html/head/meta[12]/@content')
        return html_data[0]

    #保存数据
    def write_page(self,LL):
        # 连接database
        conn = pymysql.connect(host='127.0.0.1', user='root', password='root', database='weiknew', charset='utf8')
        # 得到一个可以执行SQL语句并且将结果作为字典返回的游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        sql = "truncate netdatas"  # 清空表
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            print("mysql truncate error:")
            print(e)
            conn.rollback()  # 有异常，回滚事务


        for ii in LL:
            print(ii)
            print(type(ii))
            # 定义要执行的SQL语句
            sql = "INSERT INTO netdatas(account, title, url, img, update_time, wx_origin_id, big_type) VALUES (%s, %s, %s, %s, %s, %s, %s);"  # data = [("Alex", '111', '44'), ("Egon", '22', '44'), ("Yuan", '33', '44')]
            try:
                cursor.executemany(sql, ii)  # 批量执行多条插入SQL语句
                conn.commit()  # 提交事务
                print('save one data')
            except Exception as e:
                print("mysql error:")
                print(e)
                conn.rollback()  # 有异常，回滚事务
        cursor.close()
        conn.close()

    #入口函数
    def run(self):
        Ltype = ['娱乐', '社会']
        LL = []
        for i in Ltype:
            data = self.get_page(i)
            LL.append(data)  # 每个进程函数的返回值存入列表LL
        print(LL)
        print('持久化开始')
        self.write_page(LL)


if __name__ == '__main__':
    spider = DataSpider()
    spider.run()
    print('end...')
