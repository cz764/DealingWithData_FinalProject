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

 Date: 12/08/2014 21:02:41 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `insp_norm`
-- ----------------------------
DROP TABLE IF EXISTS `insp_norm`;
CREATE TABLE `insp_norm` (
  `CAMIS` int(11) DEFAULT NULL,
  `DBA` varchar(255) DEFAULT NULL,
  `BORO` varchar(255) DEFAULT NULL,
  `BUILDING` varchar(255) DEFAULT NULL,
  `STREET` varchar(255) DEFAULT NULL,
  `ZIPCODE` varchar(255) DEFAULT NULL,
  `PHONE` varchar(255) DEFAULT NULL,
  KEY `PHONE` (`PHONE`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

SET FOREIGN_KEY_CHECKS = 1;
