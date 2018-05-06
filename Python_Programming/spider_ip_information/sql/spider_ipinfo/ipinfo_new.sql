/*
Navicat MySQL Data Transfer

Source Server         : 本地数据库
Source Server Version : 50714
Source Host           : 127.0.0.1:3306
Source Database       : yata_data_01

Target Server Type    : MYSQL
Target Server Version : 50714
File Encoding         : 65001

Date: 2018-05-06 08:01:04
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for ipinfo_new
-- ----------------------------
DROP TABLE IF EXISTS `ipinfo_new`;
CREATE TABLE `ipinfo_new` (
  `id` int(12) unsigned NOT NULL AUTO_INCREMENT,
  `ip` varchar(16) DEFAULT NULL,
  `city` varchar(125) DEFAULT NULL,
  `region` varchar(125) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `lon` float(15,5) DEFAULT NULL COMMENT '经度',
  `lat` float(15,5) DEFAULT NULL COMMENT '纬度',
  `postal` varchar(50) DEFAULT NULL,
  `asn` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT 'asn编号',
  `org` varchar(125) DEFAULT NULL,
  `created_at` datetime NOT NULL COMMENT '创建时间',
  `updated_at` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `ip` (`ip`)
) ENGINE=InnoDB AUTO_INCREMENT=1245 DEFAULT CHARSET=utf8mb4;
