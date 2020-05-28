-- phpMyAdmin SQL Dump
-- version phpStudy 2014
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2020 �?05 �?28 �?07:48
-- 服务器版本: 5.5.53
-- PHP 版本: 5.5.38

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `weiknew`
--

-- --------------------------------------------------------

--
-- 表的结构 `netdatas`
--

CREATE TABLE IF NOT EXISTS `netdatas` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `account` varchar(50) NOT NULL COMMENT '所属公众号',
  `title` varchar(80) NOT NULL,
  `url` varchar(500) NOT NULL,
  `img` varchar(500) NOT NULL,
  `update_time` datetime NOT NULL COMMENT '文章更新时间',
  `wx_origin_id` varchar(50) NOT NULL,
  `big_type` varchar(10) NOT NULL COMMENT '文章所属类型',
  `createtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=231 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
