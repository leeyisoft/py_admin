use db_py_admin;
-- MySQL dump 10.13  Distrib 5.7.22, for Linux (x86_64)
--
-- Host: localhost    Database: db_py_admin
-- ------------------------------------------------------
-- Server version	5.7.22-0ubuntu18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `member` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `level_id` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '会员等级ID',
  `password` varchar(128) NOT NULL,
  `username` varchar(40) DEFAULT NULL COMMENT '登录名、昵称',
  `mobile` varchar(11) DEFAULT NULL,
  `email` varchar(80) DEFAULT NULL,
  `experience` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '经验值',
  `sex` enum('hide','male','female') NOT NULL DEFAULT 'hide' COMMENT '性别(男 male ，女 female 隐藏 hide)',
  `avatar` varchar(255) NOT NULL DEFAULT '' COMMENT '头像',
  `sign` varchar(255) DEFAULT '' COMMENT '会员签名',
  `login_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '登陆次数',
  `last_login_ip` varchar(40) NOT NULL DEFAULT '' COMMENT '最后登陆IP',
  `utc_last_login_at` datetime(6) DEFAULT NULL COMMENT '最后登录UTC时间',
  `ref_user_id` char(32) DEFAULT NULL COMMENT '推荐人ID，空字符串表示为推荐人',
  `status` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '状态:( 0 禁用；1 启用, 默认1)',
  `deleted` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '已删除的 1 是 0 否 默认 0',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  `register_ip` varchar(40) DEFAULT NULL COMMENT '注册IP',
  `register_client` varchar(20) DEFAULT NULL COMMENT '客户端：web wechat android ios mobile',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`),
  UNIQUE KEY `uk_email` (`email`),
  UNIQUE KEY `uk_mobile` (`mobile`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='会员表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `member_binding`
--

DROP TABLE IF EXISTS `member_binding`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `member_binding` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` int(11) DEFAULT NULL COMMENT '用户ID',
  `type` enum('QQ','WECHAT','MOBILE','EMAIL','ALIPAY') DEFAULT NULL COMMENT '绑定类型',
  `openid` varchar(80) DEFAULT NULL COMMENT '第三方平台openid',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `member_certification`
--

DROP TABLE IF EXISTS `member_certification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `member_certification` (
  `user_id` int(11) NOT NULL DEFAULT '0' COMMENT '主键，member表 id',
  `realname` varchar(40) NOT NULL DEFAULT '' COMMENT '登录名、昵称',
  `idcardno` varchar(40) NOT NULL DEFAULT '' COMMENT '身份证号码',
  `idcard_img` varchar(200) NOT NULL DEFAULT '' COMMENT '手持身份证照片一张（要求头像清晰，身份证号码清晰）',
  `authorized` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '认证状态:( 0 待审核；1 审核通过, 2 审核失败)',
  `client` varchar(20) DEFAULT NULL COMMENT '客户端：web wechat android ios mobile',
  `ip` varchar(40) DEFAULT NULL COMMENT '添加记录的IP地址',
  `utc_updated_at` datetime(6) DEFAULT NULL COMMENT '更新记录UTC时间',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态:( 0 禁用；1 启用, 默认1)',
  `remark` varchar(200) DEFAULT NULL COMMENT '备注；如果审核不通过，填写原因',
  `authorized_user_id` int(11) DEFAULT NULL COMMENT '审核管理员ID，user 表 uuid',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='会员实名认证信息';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `member_friend`
--

DROP TABLE IF EXISTS `member_friend`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `member_friend` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `from_user_id` int(11) NOT NULL COMMENT '发起人',
  `to_user_id` int(11) NOT NULL COMMENT '接受人',
  `group_id` int(11) DEFAULT '0' COMMENT '用户分组ID friendgroup主键',
  `status` varchar(16) NOT NULL DEFAULT '0' COMMENT '状态 0 请求中 1 接受 2 拒绝请求',
  `utc_updated_at` datetime(6) DEFAULT NULL COMMENT '记录更新时间',
  `utc_created_at` datetime(6) NOT NULL COMMENT '创建记录UTC时间',
  `remark` varchar(200) NOT NULL DEFAULT '' COMMENT '申请好友的验证消息',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='聊天好友关系记录表（A请求B为好友，B接受之后，系统要自动加入一条B请求A的记录并且A自动确认 user_id 是 member表的主键）';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `member_friend_notice`
--

DROP TABLE IF EXISTS `member_friend_notice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `member_friend_notice` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `msgtype` enum('apply_friend','system') DEFAULT NULL COMMENT '消息类型',
  `related_id` int(11) DEFAULT NULL COMMENT '关联业务主键',
  `message` varchar(200) DEFAULT '' COMMENT '附加消息',
  `from_user_id` int(11) DEFAULT NULL COMMENT 'Member 用户ID 消息发送者 0表示为系统消息',
  `to_user_id` int(11) DEFAULT NULL COMMENT '消息接收者 Member 用户ID',
  `utc_read_at` datetime(6) DEFAULT NULL COMMENT '读消息UTC时间',
  `status` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '状态:( 0 未读；1 已读 11 接受 12 拒绝请求)',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='添加好友状态通知，定时删除60天内的已读消息';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `member_friendgroup`
--

DROP TABLE IF EXISTS `member_friendgroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `member_friendgroup` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `groupname` varchar(40) NOT NULL DEFAULT '' COMMENT '分组名称',
  `utc_created_at` datetime(6) NOT NULL COMMENT '创建记录UTC时间',
  `owner_user_id` int(11) NOT NULL DEFAULT '0' COMMENT '分组所属用户ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='好友分组表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `member_level`
--

DROP TABLE IF EXISTS `member_level`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `member_level` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(80) NOT NULL COMMENT '等级名称',
  `min_exper` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '最小经验值',
  `max_exper` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '最大经验值',
  `intro` varchar(255) NOT NULL COMMENT '等级简介',
  `default` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '默认等级',
  `expire` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '会员有效期(天)',
  `status` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '状态:( 0 禁用；1 启用, 默认1)',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='会员等级';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `member_login_log`
--

DROP TABLE IF EXISTS `member_login_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `member_login_log` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` int(11) NOT NULL DEFAULT '0' COMMENT '用户唯一标识',
  `ip` varchar(40) DEFAULT NULL COMMENT '登录IP',
  `client` varchar(20) DEFAULT NULL COMMENT '客户端：web wechat android ios ',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='会员登录日志';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `member_operation_log`
--

DROP TABLE IF EXISTS `member_operation_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `member_operation_log` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` int(11) NOT NULL DEFAULT '0' COMMENT '用户唯一标识',
  `account` varchar(40) NOT NULL DEFAULT '' COMMENT '用户账号： email or mobile or username',
  `action` varchar(20) DEFAULT NULL COMMENT '会员操作类型： email_reset_pwd mobile_reset_pwd activate_email',
  `ip` varchar(40) DEFAULT NULL COMMENT '登录IP',
  `client` varchar(20) DEFAULT NULL COMMENT '客户端：web wechat android ios ',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='会议操作日志记录表(操作成功的时候插入)';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sys_address`
--

DROP TABLE IF EXISTS `sys_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_address` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `country` varchar(8) NOT NULL DEFAULT '中国' COMMENT '所属国家',
  `address` varchar(200) DEFAULT NULL COMMENT '详细地址 街道门牌号',
  `longitude` decimal(12,8) NOT NULL DEFAULT '0.00000000' COMMENT '位置经度',
  `latitude` decimal(12,8) NOT NULL DEFAULT '0.00000000' COMMENT '位置纬度',
  `province_id` varchar(8) NOT NULL DEFAULT '' COMMENT '省编码',
  `city_id` varchar(8) NOT NULL DEFAULT '' COMMENT '市编码',
  `area_id` varchar(8) NOT NULL DEFAULT '' COMMENT '区编码',
  `status` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '状态:( 0 禁用；1 启用, 默认1)',
  `deleted` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '已删除的 1 是 0 否 默认 0',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='联系地址信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sys_admin_menu`
--

DROP TABLE IF EXISTS `sys_admin_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_admin_menu` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` int(11) NOT NULL DEFAULT '0' COMMENT '管理员ID(快捷菜单专用)',
  `parent_id` int(11) NOT NULL DEFAULT '0' COMMENT '父节点ID',
  `code` varchar(64) DEFAULT NULL COMMENT '授权编码',
  `title` varchar(20) NOT NULL COMMENT '菜单标题',
  `icon` varchar(80) NOT NULL DEFAULT 'aicon ai-shezhi' COMMENT '菜单图标',
  `path` varchar(200) NOT NULL DEFAULT '' COMMENT '链接地址(模块/控制器/方法)',
  `param` varchar(200) NOT NULL DEFAULT '' COMMENT '扩展参数',
  `target` varchar(20) NOT NULL DEFAULT '_self' COMMENT '打开方式(_blank,_self)',
  `sort` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '排序',
  `system` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否为系统菜单，系统菜单不可删除',
  `nav` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '是否为菜单显示，1显示0不显示',
  `status` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '状态:( 0 禁用；1 启用, 默认1)',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=142 DEFAULT CHARSET=utf8 COMMENT='管理菜单';
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `spider_document`;
CREATE TABLE `spider_document` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `url` varchar(200) NOT NULL COMMENT '',
  `title` varchar(80) NOT NULL COMMENT '标题',
  `tags` varchar(200) NOT NULL COMMENT '标签 list json 字符串',
  `categories` varchar(80) NOT NULL COMMENT '分类',
  `post_date` varchar(80) NOT NULL COMMENT '发布时间',
  `author` varchar(80) NOT NULL COMMENT '作者',
  `source` varchar(80) NOT NULL DEFAULT '' COMMENT '来源',
  `sitename` varchar(80) NOT NULL DEFAULT '' COMMENT '来源站点名称',
  `imgs` text NOT NULL COMMENT '图片地址 list json 字符串',
  `status` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '状态:( 0 禁用；1 启用, 默认1)',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  UNIQUE KEY `uk_url` (`url`),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
--
-- Table structure for table `sys_admin_role`
--

DROP TABLE IF EXISTS `sys_admin_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_admin_role` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `rolename` varchar(40) DEFAULT NULL COMMENT '角色名称',
  `permission` text COMMENT '角色权限（存储菜单uuid，以json格式存储）',
  `sort` int(11) DEFAULT '20' COMMENT '排序',
  `status` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '状态:( 0 禁用；1 启用, 默认1)',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_rolename` (`rolename`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COMMENT='后台用户角色表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sys_admin_user`
--

DROP TABLE IF EXISTS `sys_admin_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_admin_user` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `role_id` int(11) DEFAULT NULL COMMENT '角色ID',
  `password` varchar(128) NOT NULL,
  `username` varchar(40) DEFAULT NULL,
  `mobile` varchar(11) DEFAULT NULL,
  `email` varchar(80) DEFAULT NULL,
  `permission` text COMMENT '用户权限（存储菜单uuid，以json格式存储，最终权限是用户和角色权限的交集）',
  `login_count` int(11) DEFAULT '0' COMMENT '登录次数',
  `last_login_ip` varchar(40) DEFAULT NULL COMMENT '最后登陆IP',
  `utc_last_login_at` datetime(6) DEFAULT NULL COMMENT '最后登录UTC时间',
  `status` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '状态:( 0 禁用；1 启用, 默认1)',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`),
  UNIQUE KEY `uk_email` (`email`),
  UNIQUE KEY `uk_mobile` (`mobile`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COMMENT='后台管用户表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sys_admin_user_login_log`
--

DROP TABLE IF EXISTS `sys_admin_user_login_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_admin_user_login_log` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` int(11) NOT NULL DEFAULT '0' COMMENT '用户唯一标识',
  `ip` varchar(40) DEFAULT NULL COMMENT '登录IP',
  `client` varchar(20) DEFAULT NULL COMMENT '客户端：web wechat android ios ',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COMMENT='后台用户登录日志';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sys_attach`
--

DROP TABLE IF EXISTS `sys_attach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_attach` (
  `file_md5` varchar(40) NOT NULL DEFAULT '' COMMENT '文件内容md5',
  `file_ext` varchar(20) NOT NULL DEFAULT '' COMMENT '文件扩展名，例如 png',
  `file_size` int(11) unsigned NOT NULL COMMENT '文件大小(单位Byte)',
  `file_mimetype` varchar(40) NOT NULL DEFAULT '' COMMENT '附件类型 application/octet-stream',
  `origin_name` varchar(80) NOT NULL DEFAULT '' COMMENT '源文件名称',
  `path_file` varchar(200) NOT NULL DEFAULT '' COMMENT '带路径的文件',
  `user_id` int(11) DEFAULT NULL COMMENT '上传用户ID(member 或者 admin_user 的 id)',
  `ip` varchar(40) NOT NULL DEFAULT '' COMMENT '客服端IP',
  `utc_created_at` datetime(6) NOT NULL COMMENT '创建记录UTC时间',
  PRIMARY KEY (`file_md5`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='系统附件表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sys_attach_related`
--

DROP TABLE IF EXISTS `sys_attach_related`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_attach_related` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `file_md5` varchar(40) NOT NULL DEFAULT '' COMMENT '文件内容md5',
  `related_table` varchar(40) NOT NULL DEFAULT '' COMMENT '关联表全称',
  `related_id` varchar(32) NOT NULL DEFAULT '' COMMENT '关联表记录主键',
  `ip` varchar(40) NOT NULL DEFAULT '' COMMENT '客服端IP',
  `utc_created_at` datetime(6) NOT NULL COMMENT '创建记录UTC时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='系统附件关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sys_config`
--

DROP TABLE IF EXISTS `sys_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_config` (
  `key` varchar(40) NOT NULL DEFAULT '' COMMENT '主键',
  `value` text,
  `title` varchar(40) DEFAULT NULL COMMENT '标题',
  `sort` int(11) DEFAULT NULL,
  `remark` varchar(128) NOT NULL,
  `system` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否为系统配置，系统配置不可删除',
  `status` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '状态:( 0 禁用；1 启用, 默认1)',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  PRIMARY KEY (`key`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='系统配置';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sys_message`
--

DROP TABLE IF EXISTS `sys_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_message` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `msgtype` enum('apply_friend','accept_friend','system') DEFAULT NULL COMMENT '消息类型',
  `message` varchar(200) DEFAULT '' COMMENT '附加消息',
  `from_user_id` varchar(32) DEFAULT NULL COMMENT 'Member 用户ID 消息发送者 0表示为系统消息',
  `to_user_id` varchar(32) DEFAULT NULL COMMENT '消息接收者 Member 用户ID',
  `utc_read_at` datetime(6) DEFAULT NULL COMMENT '读消息UTC时间',
  `status` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '状态:( 0 未读；1 已读, 默认0)',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='系统消息，定时删除30天内的已读消息';
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `sys_sequence`
--

DROP TABLE IF EXISTS `sys_sequence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_sequence` (
  `key` varchar(40) NOT NULL DEFAULT '',
  `value` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-07-22  9:24:49
