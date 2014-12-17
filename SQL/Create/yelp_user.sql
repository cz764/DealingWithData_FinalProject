/*
 Navicat Premium Data Transfer

 Source Server         : Local
 Source Server Type    : MySQL
 Source Server Version : 50621
 Source Host           : localhost
 Source Database       : dwdproject

 Target Server Type    : MySQL
 Target Server Version : 50621
 File Encoding         : utf-8

 Date: 12/17/2014 11:53:02 AM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `yelp_user`
-- ----------------------------
DROP TABLE IF EXISTS `yelp_user`;
CREATE TABLE `yelp_user` (
  `user_tagline` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `Friends` int(10) DEFAULT NULL,
  `ReviewCount` int(10) DEFAULT NULL,
  `Elite` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `Useful` int(10) DEFAULT NULL,
  `Funny` int(10) DEFAULT NULL,
  `Cool` int(10) DEFAULT NULL,
  `Location` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `YelpingSince` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `ThingsILove` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `MyHometown` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `userid` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  KEY `userid` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

SET FOREIGN_KEY_CHECKS = 1;
