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

 Date: 12/17/2014 11:52:55 AM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `yelp_review`
-- ----------------------------
DROP TABLE IF EXISTS `yelp_review`;
CREATE TABLE `yelp_review` (
  `bizid` varchar(255) DEFAULT NULL,
  `userid` varchar(255) DEFAULT NULL,
  `rating` float(2,0) DEFAULT NULL,
  `review_date` date DEFAULT NULL,
  `review` text,
  `useful` varchar(255) DEFAULT NULL,
  `funny` varchar(255) DEFAULT NULL,
  `cool` varchar(255) DEFAULT NULL,
  `checkins` int(3) DEFAULT NULL,
  KEY `id` (`bizid`),
  KEY `userid` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

SET FOREIGN_KEY_CHECKS = 1;
