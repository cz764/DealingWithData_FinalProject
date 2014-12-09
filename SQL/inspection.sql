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

 Date: 12/08/2014 21:02:51 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `inspection`
-- ----------------------------
DROP TABLE IF EXISTS `inspection`;
CREATE TABLE `inspection` (
  `CAMIS` int(11) DEFAULT NULL,
  `DBA` varchar(255) DEFAULT NULL,
  `BORO` varchar(255) DEFAULT NULL,
  `BUILDING` varchar(255) DEFAULT NULL,
  `STREET` varchar(255) DEFAULT NULL,
  `ZIPCODE` varchar(255) DEFAULT NULL,
  `PHONE` varchar(255) DEFAULT NULL,
  `CUISINE DESCRIPTION` varchar(255) DEFAULT NULL,
  `INSPECTION DATE` datetime DEFAULT NULL,
  `SCORE` varchar(255) DEFAULT NULL,
  `GRADE` varchar(255) DEFAULT NULL,
  `GRADE DATE` varchar(255) DEFAULT NULL,
  `RECORD DATE` datetime DEFAULT NULL,
  KEY `PHONE` (`PHONE`),
  KEY `ZIPCODE` (`ZIPCODE`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

SET FOREIGN_KEY_CHECKS = 1;
