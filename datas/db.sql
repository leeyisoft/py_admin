# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.18)
# Database: db_py_admin
# Generation Time: 2018-05-03 09:08:31 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table sys_admin_menu
# ------------------------------------------------------------

DROP TABLE IF EXISTS `sys_admin_menu`;

CREATE TABLE `sys_admin_menu` (
  `uuid` varchar(32) NOT NULL DEFAULT '' COMMENT '主键',
  `user_id` varchar(32) NOT NULL DEFAULT '0' COMMENT '管理员ID(快捷菜单专用)',
  `parent_id` varchar(32) NOT NULL DEFAULT '0' COMMENT '父节点ID',
  `code` varchar(64) DEFAULT NULL COMMENT '菜单编号',
  `title` varchar(20) NOT NULL COMMENT '菜单标题',
  `icon` varchar(80) NOT NULL DEFAULT 'aicon ai-shezhi' COMMENT '菜单图标',
  `path` varchar(200) NOT NULL DEFAULT '' COMMENT '链接地址(模块/控制器/方法)',
  `param` varchar(200) NOT NULL DEFAULT '' COMMENT '扩展参数',
  `target` varchar(20) NOT NULL DEFAULT '_self' COMMENT '打开方式(_blank,_self)',
  `sort` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '排序',
  `system` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否为系统菜单，系统菜单不可删除',
  `nav` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '是否为菜单显示，1显示0不显示',
  `status` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '状态:( 0 禁用；1 启用, 默认1)',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  PRIMARY KEY (`uuid`),
  UNIQUE KEY `uk_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='管理菜单';

LOCK TABLES `sys_admin_menu` WRITE;
/*!40000 ALTER TABLE `sys_admin_menu` DISABLE KEYS */;

INSERT INTO `sys_admin_menu` (`uuid`, `user_id`, `parent_id`, `code`, `title`, `icon`, `path`, `param`, `target`, `sort`, `system`, `nav`, `status`, `utc_created_at`)
VALUES
    ('1','0','0','admin:main','首页','','/admin/main','','_self',0,1,1,1,NULL),
    ('10','0','6','admin:system:setting','系统设置','','/admin/system/index','','_self',1,1,1,1,NULL),
    ('100','0','97','admin:language:del','删除语言包','','/admin/language/del','','_self',100,1,0,1,NULL),
    ('101','0','97','admin:language:sort','排序设置','','/admin/language/sort','','_self',100,1,0,1,NULL),
    ('102','0','97','admin:language:status','状态设置','','/admin/language/status','','_self',100,1,0,1,NULL),
    ('105','0','4','admin:index:welcome','欢迎页面','','/admin/index/welcome','','_self',4,1,0,1,NULL),
    ('106','0','4','admin:user:iframe','布局切换','','/admin/user/iframe','','_self',1,1,0,1,NULL),
    ('107','0','15','admin:log:del','删除日志','','/admin/log/del','table=admin_log','_self',100,1,0,1,NULL),
    ('108','0','15','admin:log:clear','清空日志','','/admin/log/clear','','_self',100,1,0,1,NULL),
    ('109','0','4',NULL,'预留占位','','/','','_self',100,1,1,0,NULL),
    ('11','0','6','admin:config:index','配置管理','','/admin/config/index','','_self',2,1,1,1,NULL),
    ('110','0','4',NULL,'预留占位','','/','','_self',100,1,1,0,NULL),
    ('111','0','4',NULL,'预留占位','','/','','_self',100,1,1,0,NULL),
    ('112','0','4',NULL,'预留占位','','/','','_self',100,1,1,0,NULL),
    ('113','0','4',NULL,'预留占位','','/','','_self',100,1,1,0,NULL),
    ('114','0','4',NULL,'预留占位','','/','','_self',100,1,1,0,NULL),
    ('115','0','4',NULL,'预留占位','','/','','_self',100,1,1,0,NULL),
    ('116','0','4',NULL,'预留占位','','/','','_self',100,1,1,0,NULL),
    ('117','0','4',NULL,'预留占位','','/','','_self',100,1,1,0,NULL),
    ('118','0','4',NULL,'预留占位','','/','','_self',100,1,1,0,NULL),
    ('119','0','4',NULL,'预留占位','','/','','_self',100,1,1,0,NULL),
    ('12','0','6','admin:menu:index','系统菜单','','/admin/menu/index','','_self',3,1,1,1,NULL),
    ('120','0','4',NULL,'预留占位','','/','','_self',100,1,1,0,NULL),
    ('121','0','4',NULL,'预留占位','','/','','_self',100,1,1,0,NULL),
    ('122','0','4',NULL,'预留占位','','/','','_self',100,1,1,0,NULL),
    ('123','0','4',NULL,'预留占位','','/','','_self',100,1,1,0,NULL),
    ('124','0','4',NULL,'预留占位','','/','','_self',100,1,1,0,NULL),
    ('125','0','4',NULL,'预留占位','','/','','_self',100,1,1,0,NULL),
    ('126','0','4',NULL,'预留占位','','/','','_self',100,1,1,0,NULL),
    ('127','0','4',NULL,'预留占位','','/','','_self',100,1,1,0,NULL),
    ('128','0','4',NULL,'预留占位','','/','','_self',100,1,1,0,NULL),
    ('129','0','4',NULL,'预留占位','','/','','_self',100,1,1,0,NULL),
    ('13','0','6','admin:user:role','管理员角色','','/admin/user/role','','_self',4,1,0,1,NULL),
    ('130','0','4',NULL,'预留占位','','/','','_self',100,1,1,0,NULL),
    ('132','0','0','warehousing:index','仓储系统','fa fa-bank','/warehousing/index','','_self',2,1,1,1,NULL),
    ('133','0','132','warehousing:instorage:admin','入库管理','typcn typcn-arrow-up-thick','/warehousing/instorage/index','','_self',1,0,1,1,NULL),
    ('134','0','132','warehousing:outstorage:admin','出库管理','typcn typcn-arrow-up-thick','/warehousing/outstorage/index','','_self',2,0,1,1,NULL),
    ('135','0','132','warehousing:storage:admin','库存管理','typcn typcn-arrow-loop','/warehousing/storage/index','','_self',3,0,1,1,NULL),
    ('136','0','133','warehousing:instorage:index','入库单','','/warehousing/instorage/index','','_self',1,0,1,1,NULL),
    ('137','0','134','warehousing:outstorage:index','出库单','','/warehousing/outstorage/index','','_self',0,0,1,1,NULL),
    ('138','0','135','warehousing:storage:index','库存','','/warehousing/storage/index','','_self',0,0,1,1,NULL),
    ('139','de713937f2e3487ebe54b8863bb1a1b8','4','shortcut:warehousing:storage:index','库存','','/warehousing/storage/index?','','_self',0,0,1,1,NULL),
    ('14','0','6','admin:user:index','系统管理员','','/admin/user/index','','_self',5,1,1,1,NULL),
    ('140','de713937f2e3487ebe54b8863bb1a1b8','4','shortcut:admin:main','后台首页','','/admin/index/index','','_self',100,0,0,1,NULL),
    ('141','de713937f2e3487ebe54b8863bb1a1b8','4','shortcut:admin:user:info','个人信息设置','','/admin/user/info','','_self',5,0,1,1,NULL),
    ('142','de713937f2e3487ebe54b8863bb1a1b8','4','shortcut:warehousing:instorage:index','入库管理','typcn typcn-arrow-down-thick','/warehousing/instorage/index','','_self',0,0,1,1,NULL),
    ('143','0','132','warehousing:voucher:admin','仓单管理','typcn typcn-document-text','/warehousing/voucher/index','','_self',4,0,1,1,NULL),
    ('144','0','143','warehousing:voucher:index','仓单','typcn typcn-document-text','/warehousing/voucher/index','','_self',0,0,1,1,NULL),
    ('145','0','133','warehousing:instorageapply:index','入库单申请','','/warehousing/instorageapply/index','','_self',0,0,1,1,NULL),
    ('146','0','145','warehousing:instorageapply:edit','编辑入库单','','/warehousing/instorageapply/edit','','_self',0,0,1,1,NULL),
    ('147','0','132','warhousing:customer','客户管理','typcn typcn-arrow-down-thick','/warhousing/customer','','_self',0,0,1,1,NULL),
    ('148','0','147','warehousing:customer:index','客户信息','','/warehousing/customer/index','','_self',0,0,1,0,NULL),
    ('149','de713937f2e3487ebe54b8863bb1a1b8','4','shortcut:warehousing:customer:index','客户信息','','/warehousing/customer/index','','_self',0,0,1,1,NULL),
    ('15','0','6','admin:log:index','系统日志','','/admin/log/index','','_self',8,1,1,1,NULL),
    ('150','0','148','warehousing:customer:edit','编辑客户信息','','/warehousing/customer/edit','','_self',0,0,1,1,NULL),
    ('16','0','6','admin:annex:index','附件管理','','/admin/annex/index','','_self',7,1,0,1,NULL),
    ('17','0','8','admin:module:index','模块管理','','/admin/module/index','','_self',1,1,1,1,NULL),
    ('18','0','8','admin:plugins:admin','插件管理','','/admin/plugins/index','','_self',2,1,1,1,NULL),
    ('19','0','8','admin:hook:index','钩子管理','','/admin/hook/index','','_self',3,1,1,1,NULL),
    ('2','0','0','admin:system','系统','','/admin/system','','_self',10,1,1,1,NULL),
    ('20','0','7','admin:member:level','会员等级','','/admin/member/level','','_self',1,1,1,1,NULL),
    ('21','0','7','admin:member:index','会员列表','','/admin/member/index','','_self',2,1,1,1,NULL),
    ('22','0','9','admin:develop:lists','[示例]列表模板','','/admin/develop/lists','','_self',1,1,1,1,NULL),
    ('23','0','9','admin:develop:edit','[示例]编辑模板','','/admin/develop/edit','','_self',2,1,1,1,NULL),
    ('24','0','4','admin:index:index','后台首页','','/admin/index/index','','_self',3,1,0,1,NULL),
    ('25','0','4','admin:index:clear','清空缓存','','/admin/index/clear','','_self',5,1,0,0,NULL),
    ('26','0','12','admin:menu:add','添加菜单','','/admin/menu/add','','_self',1,1,1,1,NULL),
    ('27','0','12','admin:menu:edit','修改菜单','','/admin/menu/edit','','_self',2,1,1,1,NULL),
    ('28','0','12','admin:menu:del','删除菜单','','/admin/menu/del','','_self',3,1,1,1,NULL),
    ('29','0','12','admin:menu:status','状态设置','','/admin/menu/status','','_self',4,1,1,1,NULL),
    ('3','0','0','admin:plugins','插件','aicon ai-shezhi','/admin/plugins','','_self',12,1,1,0,NULL),
    ('30','0','12','admin:menu:sort','排序设置','','/admin/menu/sort','','_self',5,1,1,1,NULL),
    ('31','0','12','admin:menu:quick','添加快捷菜单','','/admin/menu/quick','','_self',6,1,1,1,NULL),
    ('32','0','12','admin:menu:export','导出菜单','','/admin/menu/export','','_self',7,1,1,1,NULL),
    ('33','0','13','admin:user:addrole','添加角色','','/admin/user/addrole','','_self',1,1,1,1,NULL),
    ('34','0','13','admin:user:editrole','修改角色','','/admin/user/editrole','','_self',2,1,1,1,NULL),
    ('35','0','13','admin:user:delrole','删除角色','','/admin/user/delrole','','_self',3,1,1,1,NULL),
    ('36','0','13','admin:user:status','状态设置','','/admin/user/status','','_self',4,1,1,1,NULL),
    ('37','0','14','admin:user:adduser','添加管理员','','/admin/user/adduser','','_self',1,1,1,1,NULL),
    ('38','0','14','admin:user:edituser','修改管理员','','/admin/user/edituser','','_self',2,1,1,1,NULL),
    ('39','0','14','admin:user:deluser','删除管理员','','/admin/user/deluser','','_self',3,1,1,1,NULL),
    ('4','0','1','admin:quick','快捷菜单','aicon ai-shezhi','/admin/quick','','_self',1,1,1,1,NULL),
    ('40','0','14','admin:user:status2','状态设置','','/admin/user/status','','_self',4,1,1,1,NULL),
    ('41','0','14','admin:user:info','个人信息设置','','/admin/user/info','','_self',5,1,1,1,NULL),
    ('42','0','18','admin:plugins:install','安装插件','','/admin/plugins/install','','_self',1,1,1,1,NULL),
    ('43','0','18','admin:plugins:uninstall','卸载插件','','/admin/plugins/uninstall','','_self',2,1,1,1,NULL),
    ('44','0','18','admin:plugins:del','删除插件','','/admin/plugins/del','','_self',3,1,1,1,NULL),
    ('45','0','18','admin:plugins:status','状态设置','','/admin/plugins/status','','_self',4,1,1,1,NULL),
    ('46','0','18','admin:plugins:design','设计插件','','/admin/plugins/design','','_self',5,1,1,1,NULL),
    ('47','0','18','admin:plugins:run','运行插件','','/admin/plugins/run','','_self',6,1,1,1,NULL),
    ('48','0','18','admin:plugins:update','更新插件','','/admin/plugins/update','','_self',7,1,1,1,NULL),
    ('49','0','18','admin:plugins:setting','插件配置','','/admin/plugins/setting','','_self',8,1,1,1,NULL),
    ('5','0','3','admin:plugins:index','插件列表','aicon ai-shezhi','/admin/plugins','','_self',0,1,1,1,NULL),
    ('50','0','19','admin:hook:add','添加钩子','','/admin/hook/add','','_self',1,1,1,1,NULL),
    ('51','0','19','admin:hook:edit','修改钩子','','/admin/hook/edit','','_self',2,1,1,1,NULL),
    ('52','0','19','admin:hook:del','删除钩子','','/admin/hook/del','','_self',3,1,1,1,NULL),
    ('53','0','19','admin:hook:status','状态设置','','/admin/hook/status','','_self',4,1,1,1,NULL),
    ('54','0','19','admin:hook:sort','插件排序','','/admin/hook/sort','','_self',5,1,1,1,NULL),
    ('55','0','11','admin:config:add','添加配置','','/admin/config/add','','_self',1,1,1,1,NULL),
    ('56','0','11','admin:config:edit','修改配置','','/admin/config/edit','','_self',2,1,1,1,NULL),
    ('57','0','11','admin:config:del','删除配置','','/admin/config/del','','_self',3,1,1,1,NULL),
    ('58','0','11','admin:config:status','状态设置','','/admin/config/status','','_self',4,1,1,1,NULL),
    ('59','0','11','admin:config:sort','排序设置','','/admin/config/sort','','_self',5,1,1,1,NULL),
    ('6','0','2','admin:system:function','系统功能','aicon ai-shezhi','/admin/system','','_self',1,1,1,1,NULL),
    ('60','0','10','admin:system:base','基础配置','','/admin/system/index','group=base','_self',1,1,1,1,NULL),
    ('61','0','10','admin:system:config','系统配置','','/admin/system/index','group=sys','_self',2,1,1,1,NULL),
    ('62','0','10','admin:system:index','上传配置','','/admin/system/index','group=upload','_self',3,1,1,1,NULL),
    ('63','0','10','admin:system:dev','开发配置','','/admin/system/index','group=develop','_self',4,1,1,1,NULL),
    ('64','0','17','admin:module:design','设计模块','','/admin/module/design','','_self',6,1,1,1,NULL),
    ('65','0','17','admin:module:install','安装模块','','/admin/module/install','','_self',1,1,1,1,NULL),
    ('66','0','17','admin:module:uninstall','卸载模块','','/admin/module/uninstall','','_self',2,1,1,1,NULL),
    ('67','0','17','admin:module:status','状态设置','','/admin/module/status','','_self',3,1,1,1,NULL),
    ('68','0','17','admin:module:setdefault','设置默认模块','','/admin/module/setdefault','','_self',4,1,1,1,NULL),
    ('69','0','17','admin:module:del','删除模块','','/admin/module/del','','_self',5,1,1,1,NULL),
    ('7','0','2','admin:member','会员管理','aicon ai-shezhi','/admin/member','','_self',2,1,1,1,NULL),
    ('70','0','21','admin:member:add','添加会员','','/admin/member/add','','_self',1,1,1,1,NULL),
    ('71','0','21','admin:member:edit','修改会员','','/admin/member/edit','','_self',2,1,1,1,NULL),
    ('72','0','21','admin:member:del','删除会员','','/admin/member/del','table=admin_member','_self',3,1,1,1,NULL),
    ('73','0','21','admin:member:status','状态设置','','/admin/member/status','','_self',4,1,1,1,NULL),
    ('74','0','21','admin:member:pop','[弹窗]会员选择','','/admin/member/pop','','_self',5,1,1,1,NULL),
    ('75','0','20','admin:member:addlevel','添加会员等级','','/admin/member/addlevel','','_self',0,1,1,1,NULL),
    ('76','0','20','admin:member:editlevel','修改会员等级','','/admin/member/editlevel','','_self',0,1,1,1,NULL),
    ('77','0','20','admin:member:dellevel','删除会员等级','','/admin/member/dellevel','','_self',0,1,1,1,NULL),
    ('78','0','16','admin:annex:upload','附件上传','','/admin/annex/upload','','_self',1,1,1,1,NULL),
    ('79','0','16','admin:annex:del','删除附件','','/admin/annex/del','','_self',2,1,1,1,NULL),
    ('8','0','2','admin:extend','系统扩展','aicon ai-shezhi','/admin/extend','','_self',3,1,1,1,NULL),
    ('80','0','8','admin:upgrade:index','在线升级','','/admin/upgrade/index','','_self',4,1,1,1,NULL),
    ('81','0','80','admin:upgrade:lists','获取升级列表','','/admin/upgrade/lists','','_self',0,1,1,1,NULL),
    ('82','0','80','admin:upgrade:install','安装升级包','','/admin/upgrade/install','','_self',0,1,1,1,NULL),
    ('83','0','80','admin:upgrade:download','下载升级包','','/admin/upgrade/download','','_self',0,1,1,1,NULL),
    ('84','0','6','admin:role:index','角色管理','','/admin/role/index','','_self',6,1,1,1,NULL),
    ('85','0','84','admin:database:export','备份数据库','','/admin/database/export','','_self',0,1,1,1,NULL),
    ('86','0','84','admin:database:import','恢复数据库','','/admin/database/import','','_self',0,1,1,1,NULL),
    ('87','0','84','admin:database:optimize','优化数据库','','/admin/database/optimize','','_self',0,1,1,1,NULL),
    ('88','0','84','admin:database:del','删除备份','','/admin/database/del','','_self',0,1,1,1,NULL),
    ('89','0','84','admin:database:repair','修复数据库','','/admin/database/repair','','_self',0,1,1,1,NULL),
    ('9','0','2','admin:develop','开发专用','aicon ai-shezhi','/admin/develop','','_self',4,1,1,1,NULL),
    ('90','0','21','admin:member:setdefault','设置默认等级','','/admin/member/setdefault','','_self',0,1,1,1,NULL),
    ('91','0','10','admin:system:db','数据库配置','','/admin/system/index','group=databases','_self',5,1,1,1,NULL),
    ('92','0','17','admin:module:package','模块打包','','/admin/module/package','','_self',7,1,1,1,NULL),
    ('93','0','18','admin:plugins:package','插件打包','','/admin/plugins/package','','_self',0,1,1,1,NULL),
    ('94','0','17','admin:module:theme','主题管理','','/admin/module/theme','','_self',8,1,1,1,NULL),
    ('95','0','17','admin:module:setdefaulttheme','设置默认主题','','/admin/module/setdefaulttheme','','_self',9,1,1,1,NULL),
    ('96','0','17','admin:module:deltheme','删除主题','','/admin/module/deltheme','','_self',10,1,1,1,NULL),
    ('97','0','6','admin:language:index','语言包管理','','/admin/language/index','','_self',11,1,0,1,NULL),
    ('98','0','97','admin:language:add','添加语言包','','/admin/language/add','','_self',100,1,0,1,NULL),
    ('99','0','97','admin:language:edit','修改语言包','','/admin/language/edit','','_self',100,1,0,1,NULL);

/*!40000 ALTER TABLE `sys_admin_menu` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table sys_admin_role
# ------------------------------------------------------------

DROP TABLE IF EXISTS `sys_admin_role`;

CREATE TABLE `sys_admin_role` (
  `uuid` varchar(32) NOT NULL DEFAULT '' COMMENT '主键',
  `rolename` varchar(40) DEFAULT NULL COMMENT '角色名称',
  `permission` text COMMENT '角色权限（存储菜单uuid，以json格式存储）',
  `sort` int(10) DEFAULT '20' COMMENT '排序',
  `status` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '状态:( 0 禁用；1 启用, 默认1)',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  PRIMARY KEY (`uuid`),
  UNIQUE KEY `uq_name` (`rolename`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='后台用户角色表';

LOCK TABLES `sys_admin_role` WRITE;
/*!40000 ALTER TABLE `sys_admin_role` DISABLE KEYS */;

INSERT INTO `sys_admin_role` (`uuid`, `rolename`, `permission`, `sort`, `status`, `utc_created_at`)
VALUES
    ('4215728977424fe9bb67b93892c55a54','财务组','[\"admin:main\", \"admin:quick\", \"admin:index:clear\", \"admin:index:index\", \"admin:index:welcome\", \"admin:user:iframe\"]',12,1,'2018-04-17 06:19:33.967168'),
    ('6b0642103a1749949a07f4139574ead9','默认角色','[\"admin:main\", \"admin:quick\", \"admin:user:iframe\", \"admin:index:index\", \"admin:index:welcome\"]',20,1,NULL),
    ('79e88acd2ee048dcb03968026d0779e7','风控组','',20,1,'2018-05-02 02:22:47.143951'),
    ('960245d0d12540918825ecd42553fd39','超级管理员','[\"admin:main\", \"admin:quick\", \"admin:user:iframe\", \"admin:index:index\", \"admin:index:welcome\", \"warehousing:index\", \"warhousing:customer\", \"warehousing:instorage:admin\", \"warehousing:instorageapply:index\", \"warehousing:instorage:index\", \"warehousing:outstorage:admin\", \"warehousing:outstorage:index\", \"warehousing:storage:admin\", \"warehousing:storage:index\", \"warehousing:voucher:admin\", \"warehousing:voucher:index\", \"admin:system\", \"admin:system:function\", \"admin:system:setting\", \"admin:config:index\", \"admin:menu:index\", \"admin:user:role\", \"admin:user:index\", \"admin:role:index\", \"admin:annex:index\", \"admin:log:index\", \"admin:language:index\", \"admin:member\", \"admin:member:level\", \"admin:member:index\", \"admin:extend\", \"admin:module:index\", \"admin:plugins:admin\", \"admin:hook:index\", \"admin:upgrade:index\", \"admin:develop\", \"admin:develop:lists\", \"admin:develop:edit\"]',1,1,'2018-03-05 07:27:44.537284');

/*!40000 ALTER TABLE `sys_admin_role` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table sys_admin_user
# ------------------------------------------------------------

DROP TABLE IF EXISTS `sys_admin_user`;

CREATE TABLE `sys_admin_user` (
  `uuid` char(32) NOT NULL DEFAULT '' COMMENT '主键',
  `role_id` char(32) DEFAULT NULL,
  `password` varchar(128) NOT NULL,
  `username` varchar(40) DEFAULT NULL,
  `mobile` varchar(11) DEFAULT NULL,
  `email` varchar(80) DEFAULT NULL,
  `permission` text COMMENT '用户权限（存储菜单uuid，以json格式存储，最终权限是用户和角色权限的交集）',
  `login_count` int(10) DEFAULT '0' COMMENT '登录次数',
  `utc_last_login_at` datetime(6) DEFAULT NULL COMMENT '最后登录UTC时间',
  `status` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '状态:( 0 禁用；1 启用, 默认1)',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  PRIMARY KEY (`uuid`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `mobile` (`mobile`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='后台管用户表';

LOCK TABLES `sys_admin_user` WRITE;
/*!40000 ALTER TABLE `sys_admin_user` DISABLE KEYS */;

INSERT INTO `sys_admin_user` (`uuid`, `role_id`, `password`, `username`, `mobile`, `email`, `permission`, `login_count`, `utc_last_login_at`, `status`, `utc_created_at`)
VALUES
    ('a85844f06ce74eb88c12f2d25e29282f','6b0642103a1749949a07f4139574ead9','pbkdf2_sha256$100000$0RAcdxzlsMjsDwxE$WXPx6LTlPYoLfQXIrVOxE+3Qg6EI007d6P8Iu/t9ats=','ces2',NULL,NULL,'[\"admin:main\", \"admin:quick\", \"admin:user:iframe\", \"admin:index:index\", \"admin:index:welcome\"]',0,NULL,1,'2018-05-02 03:43:38.918080'),
    ('de713937f2e3487ebe54b8863bb1a1b7','960245d0d12540918825ecd42553fd39','pbkdf2_sha256$100000$VeYBgw06FjOgFThY$9F9IzDbqOHjdc4GPdHN8TFTwyYQ9LMYvxrs355i65a0=','leeyi',NULL,NULL,'[\"admin:main\", \"admin:quick\", \"admin:user:iframe\", \"admin:index:index\", \"admin:index:welcome\", \"admin:system\", \"admin:system:function\", \"admin:system:setting\", \"admin:config:index\", \"admin:menu:index\", \"admin:user:role\", \"admin:user:index\", \"admin:role:index\", \"admin:annex:index\", \"admin:log:index\", \"admin:language:index\", \"admin:member\", \"admin:member:level\", \"admin:member:index\", \"admin:extend\", \"admin:module:index\", \"admin:plugins:admin\", \"admin:hook:index\", \"admin:upgrade:index\", \"warehousing:index\", \"warhousing:customer\", \"warehousing:instorage:admin\", \"warehousing:instorageapply:index\", \"warehousing:instorage:index\", \"warehousing:outstorage:admin\", \"warehousing:outstorage:index\", \"warehousing:storage:admin\", \"warehousing:storage:index\", \"warehousing:voucher:admin\", \"warehousing:voucher:index\"]',NULL,NULL,1,'2018-02-28 09:15:10.012341'),
    ('de713937f2e3487ebe54b8863bb1a1b8','6b0642103a1749949a07f4139574ead9','pbkdf2_sha256$100000$NP4LtrgwwP14HqMl$ISbZV4pRsfGaI9ZY0r7rx50D5Ya5aFFyPh12xKZWVVA=','admin','','','[]',NULL,'2018-02-28 09:15:10.012341',1,'2018-02-28 09:15:10.012341');

/*!40000 ALTER TABLE `sys_admin_user` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table sys_admin_user_login_log
# ------------------------------------------------------------

DROP TABLE IF EXISTS `sys_admin_user_login_log`;

CREATE TABLE `sys_admin_user_login_log` (
  `uuid` varchar(32) NOT NULL DEFAULT '' COMMENT '主键',
  `user_id` varchar(32) NOT NULL DEFAULT '' COMMENT '用户唯一标示',
  `login_at` datetime(6) DEFAULT NULL COMMENT '登录UTC时间',
  `ip` varchar(40) DEFAULT NULL COMMENT '登录IP',
  `client` varchar(20) DEFAULT NULL COMMENT '客户端：web wechat android ios ',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  PRIMARY KEY (`uuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='后台用户登录日志';



# Dump of table sys_address
# ------------------------------------------------------------

DROP TABLE IF EXISTS `sys_address`;

CREATE TABLE `sys_address` (
  `uuid` char(32) NOT NULL DEFAULT '' COMMENT '主键',
  `country` varchar(4) NOT NULL DEFAULT '中国' COMMENT '所属国家',
  `address` varchar(200) DEFAULT NULL COMMENT '详细地址 街道门牌号',
  `longitude` decimal(12,8) NOT NULL DEFAULT '0.00000000' COMMENT '位置经度',
  `latitude` decimal(12,8) NOT NULL DEFAULT '0.00000000' COMMENT '位置纬度',
  `province_id` varchar(8) NOT NULL DEFAULT '' COMMENT '省编码',
  `city_id` varchar(8) NOT NULL DEFAULT '' COMMENT '市编码',
  `area_id` varchar(8) NOT NULL DEFAULT '' COMMENT '区编码',
  `status` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '状态:( 0 禁用；1 启用, 默认1)',
  `deleted` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '已删除的 1 是 0 否 默认 0',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='联系地址信息表';



# Dump of table sys_config
# ------------------------------------------------------------

DROP TABLE IF EXISTS `sys_config`;

CREATE TABLE `sys_config` (
  `key` varchar(40) NOT NULL DEFAULT '' COMMENT '主键',
  `value` text,
  `remark` varchar(128) NOT NULL,
  `status` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '状态:(0 无效, 1正常, 默认1)',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  PRIMARY KEY (`key`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='系统配置';

LOCK TABLES `sys_config` WRITE;
/*!40000 ALTER TABLE `sys_config` DISABLE KEYS */;

INSERT INTO `sys_config` (`key`, `value`, `remark`, `status`, `utc_created_at`)
VALUES
    ('login_pwd_rsa_encrypt','1','系统登录开启RSA加密',1,'2018-02-27 12:21:28.000000'),
    ('sys_login_rsa_pub_key','-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDxKL1RrEcd4szM8Df4HqsJdOvK\nrSQO7BBvBVsvXKfpWrM+8XGL1SP7nsQd6alhntotPSDezaHnFvhnP/sr8bwzzorr\n1dWoBVabqDFZgZ2awB7iTk4k/3RN1TEPoD08kaJQ0xBHZ14395q8bVh22Uh10eCO\n/xtHnso3I6penSvRawIDAQAB\n-----END PUBLIC KEY-----\n','系统登录RSA加密公钥',1,'2018-02-27 06:34:50.196969'),
    ('sys_login_rsa_priv_key','-----BEGIN RSA PRIVATE KEY-----\nMIICXQIBAAKBgQDxKL1RrEcd4szM8Df4HqsJdOvKrSQO7BBvBVsvXKfpWrM+8XGL\n1SP7nsQd6alhntotPSDezaHnFvhnP/sr8bwzzorr1dWoBVabqDFZgZ2awB7iTk4k\n/3RN1TEPoD08kaJQ0xBHZ14395q8bVh22Uh10eCO/xtHnso3I6penSvRawIDAQAB\nAoGAQKctalIHlumRAnh8aNa///8KoAGfIykCluEWuzHaCmO4nm1YhaaUyQadiW91\na6iM0YgL4e+7MhskaXnrurJKRAweJP49OHz2JbLwyE7N7FWlY++1RVwWE32645CT\nt8hkAyFBBBR0J1by8HdGnPa69sJ6wwBYoh3SeCM8R92cfsECQQD+TbbYV/lw9KQD\nju+18bWpAyQeMBdx11OfgN3fBkRwrl9M0DHzwFKwDY7zFxPuYKD5I39wNeSbYYHJ\n9my6/JybAkEA8sST9CmwLgCoRwciUdxH4hOW8uAdGC9T2VYSo/BbO/geF09c+Ggx\nSoyEFIoAUMDC53Yj4dXgks0gnwWygRyjcQJBAN/P59+qNbgLJ5qWHzTDYX05bX1A\nGDIyL7/Ou/bAXlXJscg55+y+VEfr9ubNZdZDpwj+C/fnBqcV/xOP1QwQrYcCQQC+\ncO0rxaQ6gjN//J20n9wYAowQnTTVqxLY1Ies6Tl40swwNwbUq0+3joFyZ0uWDZEX\n5/qAB7qzDo1/kgWU+TVRAkAwAdK+p5ippKmp2efsdqRjb/71n+EX9adpo/Wh5Ece\nVp+MQkKMwNsQCkEthc/jEv4eG/urmWkLxaISAJRNegN2\n-----END RSA PRIVATE KEY-----\n','系统登录RSA加密私钥',1,'2018-02-27 06:34:50.196969'),
    ('front_end_title','前端标题','前端标题',1,'2018-02-27 06:34:50.196969'),
    ('super_admin','de713937f2e3487ebe54b8863bb1a1b8,','超级管理员列表,多个使用半角逗号分隔',1,'2018-03-15 17:43:26.000000');

/*!40000 ALTER TABLE `sys_config` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table sys_member
# ------------------------------------------------------------

DROP TABLE IF EXISTS `sys_member`;

CREATE TABLE `sys_member` (
  `uuid` char(32) NOT NULL DEFAULT '' COMMENT '主键',
  `level_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '会员等级ID',
  `password` varchar(128) NOT NULL,
  `username` varchar(40) DEFAULT NULL,
  `mobile` varchar(11) DEFAULT NULL,
  `email` varchar(80) DEFAULT NULL,
  `exper` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '经验值',
  `integral` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '积分',
  `frozen_integral` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '冻结积分',
  `sex` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '性别(1男，0女)',
  `avatar` varchar(255) NOT NULL DEFAULT '' COMMENT '头像',
  `login_count` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '登陆次数',
  `utc_expire_time` datetime(6) DEFAULT NULL COMMENT '到期UTC时间(NULL永久)',
  `last_login_ip` varchar(128) NOT NULL DEFAULT '' COMMENT '最后登陆IP',
  `utc_last_login_at` datetime(6) DEFAULT NULL COMMENT '最后登录UTC时间',
  `status` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '状态:(0 锁定, 1正常, 默认1)',
  `deleted` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '已删除的 1 是 0 否 默认 0',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='会员表';



# Dump of table sys_member_login_log
# ------------------------------------------------------------

DROP TABLE IF EXISTS `sys_member_login_log`;

CREATE TABLE `sys_member_login_log` (
  `uuid` varchar(32) NOT NULL DEFAULT '' COMMENT '主键',
  `user_id` varchar(32) NOT NULL DEFAULT '' COMMENT '用户唯一标示',
  `login_at` datetime(6) DEFAULT NULL COMMENT '登录UTC时间',
  `ip` varchar(40) DEFAULT NULL COMMENT '登录IP',
  `client` varchar(20) DEFAULT NULL COMMENT '客户端：web wechat android ios ',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  PRIMARY KEY (`uuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='用户登录日志';




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
