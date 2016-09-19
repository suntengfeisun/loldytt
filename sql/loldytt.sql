/*
Navicat MySQL Data Transfer

Source Server         : 47.88.1.153_3307
Source Server Version : 50173
Source Host           : localhost:3307
Source Database       : loldytt

Target Server Type    : MYSQL
Target Server Version : 50173
File Encoding         : 65001

Date: 2016-09-01 14:51:32
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for loldytt_category
-- ----------------------------
DROP TABLE IF EXISTS `loldytt_category`;
CREATE TABLE `loldytt_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `url` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for loldytt_content
-- ----------------------------
DROP TABLE IF EXISTS `loldytt_content`;
CREATE TABLE `loldytt_content` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `cast` text NOT NULL,
  `img` varchar(255) NOT NULL,
  `xunlei_download` text NOT NULL,
  `bt_download` text NOT NULL,
  `magnet_download` text NOT NULL,
  `content` text NOT NULL,
  `url` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Unique` (`url`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=29494 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for loldytt_options
-- ----------------------------
DROP TABLE IF EXISTS `loldytt_options`;
CREATE TABLE `loldytt_options` (
  `option_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `option_name` varchar(64) NOT NULL COMMENT '配置名',
  `option_value` longtext NOT NULL COMMENT '配置值',
  `autoload` int(2) NOT NULL DEFAULT '1' COMMENT '是否自动加载',
  PRIMARY KEY (`option_id`),
  UNIQUE KEY `option_name` (`option_name`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COMMENT='全站配置表';

-- ----------------------------
-- Table structure for loldytt_plugins
-- ----------------------------
DROP TABLE IF EXISTS `loldytt_plugins`;
CREATE TABLE `loldytt_plugins` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `name` varchar(50) NOT NULL COMMENT '插件名，英文',
  `title` varchar(50) NOT NULL DEFAULT '' COMMENT '插件名称',
  `description` text COMMENT '插件描述',
  `type` tinyint(2) DEFAULT '0' COMMENT '插件类型, 1:网站；8;微信',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态；1开启；',
  `config` text COMMENT '插件配置',
  `hooks` varchar(255) DEFAULT NULL COMMENT '实现的钩子;以“，”分隔',
  `has_admin` tinyint(2) DEFAULT '0' COMMENT '插件是否有后台管理界面',
  `author` varchar(50) DEFAULT '' COMMENT '插件作者',
  `version` varchar(20) DEFAULT '' COMMENT '插件版本号',
  `createtime` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '插件安装时间',
  `listorder` smallint(6) NOT NULL DEFAULT '0' COMMENT '排序',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='插件表';

-- ----------------------------
-- Table structure for loldytt_route
-- ----------------------------
DROP TABLE IF EXISTS `loldytt_route`;
CREATE TABLE `loldytt_route` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '路由id',
  `full_url` varchar(255) DEFAULT NULL COMMENT '完整url， 如：portal/list/index?id=1',
  `url` varchar(255) DEFAULT NULL COMMENT '实际显示的url',
  `listorder` int(5) DEFAULT '0' COMMENT '排序，优先级，越小优先级越高',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态，1：启用 ;0：不启用',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=62 DEFAULT CHARSET=utf8 COMMENT='url路由表';

-- ----------------------------
-- Table structure for loldytt_url
-- ----------------------------
DROP TABLE IF EXISTS `loldytt_url`;
CREATE TABLE `loldytt_url` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` int(11) NOT NULL,
  `url` varchar(255) NOT NULL,
  `status` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Unique` (`url`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=29460 DEFAULT CHARSET=utf8;
