
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
-- Dumping data for table `member_friendgroup`
--

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
-- Dumping data for table `member_level`
--

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
-- Dumping data for table `sys_address`
--

LOCK TABLES `sys_address` WRITE;
/*!40000 ALTER TABLE `sys_address` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_address` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='管理菜单';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_admin_menu`
--

LOCK TABLES `sys_admin_menu` WRITE;
/*!40000 ALTER TABLE `sys_admin_menu` DISABLE KEYS */;
INSERT INTO `sys_admin_menu` VALUES ('1','0','0','admin:main','首页','','/admin/main','','_self',0,1,1,1,NULL),
('10','0','6','admin:system:setting','系统设置','aicon ai-icon01','/admin/system/index','','_self',1,1,1,0,NULL),
('100','0','97','admin:language:del','删除语言包','','/admin/language/del','','_self',100,1,0,1,NULL),
('101','0','97','admin:language:sort','排序设置','','/admin/language/sort','','_self',100,1,0,1,NULL),
('102','0','97','admin:language:status','状态设置','','/admin/language/status','','_self',100,1,0,1,NULL),
('105','0','4','admin:welcome','欢迎页面','fa fa-smile-o','/admin/welcome','','_self',4,1,1,1,NULL),
('106','0','4','admin:user:iframe','布局切换','','/admin/user/iframe','','_self',1,1,0,1,NULL),
('107','0','15','admin:log:del','删除日志','','/admin/log/del','table=admin_log','_self',100,1,0,1,NULL),
('108','0','15','admin:log:clear','清空日志','','/admin/log/clear','','_self',100,1,0,1,NULL),
('11','0','6','admin:config:index','配置管理','aicon ai-peizhiguanli','/admin/config/index','','_self',2,1,1,1,NULL),
('12','0','6','admin:menu:index','系统菜单','aicon ai-xitongrizhi-tiaoshi','/admin/menu/index','','_self',3,1,1,1,NULL),
('13','0','6','admin:user:role','管理员角色','aicon ai-huiyuandengji','/admin/user/role','','_self',4,1,0,1,NULL),
('14','0','6','admin:user:index','系统管理员','aicon ai-tubiao05','/admin/user/index','','_self',5,1,1,1,NULL),
('141','0','4','shortcut:admin:user:info','个人信息设置','','/admin/user/info','','_self',6,0,1,1,NULL),
('15','0','6','admin:log:index','系统日志','aicon ai-xitongrizhi-tiaoshi','/admin/log/index','','_self',8,1,1,0,NULL),
('2','0','0','admin:system','系统','','/admin/system','','_self',10,1,1,1,NULL),
('20','0','7','admin:member:level','会员等级','aicon ai-huiyuandengji','/admin/member/level','','_self',1,1,1,0,NULL),
('21','0','7','admin:member:index','会员列表','aicon ai-huiyuanliebiao','/admin/member/index','','_self',2,1,1,1,NULL),
('24','0','4','admin:index:index','后台首页','aicon ai-shouyeshouye','/admin/index/index','','_self',2,1,0,1,NULL),
('25','0','4','admin:index:clear','清空缓存','','/admin/index/clear','','_self',5,1,0,1,NULL),
('26','0','12','admin:menu:add','添加菜单','','/admin/menu/add','','_self',1,1,1,1,NULL),
('27','0','12','admin:menu:edit','修改菜单','','/admin/menu/edit','','_self',2,1,1,1,NULL),
('28','0','12','admin:menu:del','删除菜单','','/admin/menu/del','','_self',3,1,1,1,NULL),
('29','0','12','admin:menu:status','状态设置','','/admin/menu/status','','_self',4,1,1,1,NULL),
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
('4','0','1','admin:quick','快捷菜单','fa fa-motorcycle','/admin/quick','','_self',1,1,1,1,NULL),
('40','0','14','admin:user:status2','状态设置','','/admin/user/status','','_self',4,1,1,1,NULL),
('41','0','14','admin:user:info','个人信息设置','','/admin/user/info','','_self',5,1,1,1,NULL),
('42','0','7','admin:member:authorize','会员认证','aicon ai-huiyuandengji','/admin/member/authorize','','_self',20,1,1,1,'2018-06-05 07:27:27.497084'),
('55','0','11','admin:config:add','添加配置','','/admin/config/add','','_self',1,1,1,1,NULL),
('56','0','11','admin:config:edit','修改配置','','/admin/config/edit','','_self',2,1,1,1,NULL),
('57','0','11','admin:config:del','删除配置','','/admin/config/del','','_self',3,1,1,1,NULL),
('58','0','11','admin:config:status','状态设置','','/admin/config/status','','_self',4,1,1,1,NULL),
('59','0','11','admin:config:sort','排序设置','','/admin/config/sort','','_self',5,1,1,1,NULL),
('6','0','2','admin:system:function','系统功能','aicon ai-shezhi','/admin/system','','_self',1,1,1,1,NULL),
('60','0','10','admin:system:base','基础配置','','/admin/system/index','group=base','_self',1,1,1,1,NULL),
('61','0','10','admin:system:config','系统配置','','/admin/system/index','group=sys','_self',2,1,1,1,NULL),
('62','0','10','admin:system:index','上传配置','','/admin/system/index','group=upload','_self',3,1,1,1,NULL),
('7','0','2','admin:member','会员管理','aicon ai-huiyuanliebiao','/admin/member','','_self',2,1,1,1,NULL),
('70','0','21','admin:member:add','添加会员','','/admin/member/add','','_self',1,1,1,1,NULL),
('71','0','21','admin:member:edit','修改会员','','/admin/member/edit','','_self',2,1,1,1,NULL),
('72','0','21','admin:member:del','删除会员','','/admin/member/del','table=admin_member','_self',3,1,1,1,NULL),
('73','0','21','admin:member:status','状态设置','','/admin/member/status','','_self',4,1,1,1,NULL),
('74','0','21','admin:member:pop','[弹窗]会员选择','','/admin/member/pop','','_self',5,1,1,1,NULL),
('75','0','20','admin:member:addlevel','添加会员等级','','/admin/member/addlevel','','_self',0,1,1,1,NULL),
('76','0','20','admin:member:editlevel','修改会员等级','','/admin/member/editlevel','','_self',0,1,1,1,NULL),
('77','0','20','admin:member:dellevel','删除会员等级','','/admin/member/dellevel','','_self',0,1,1,1,NULL),
('84','0','6','admin:role:index','角色管理','fa fa-users','/admin/role/index','','_self',6,1,1,1,NULL);

/*!40000 ALTER TABLE `sys_admin_menu` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='后台用户角色表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_admin_role`
--

LOCK TABLES `sys_admin_role` WRITE;
/*!40000 ALTER TABLE `sys_admin_role` DISABLE KEYS */;
INSERT INTO `sys_admin_role` VALUES ('1','默认角色','[\"admin:main\", \"admin:quick\", \"admin:user:iframe\", \"admin:index:index\", \"admin:index:welcome\"]',20,1,NULL),
('2','风控组','',20,1,'2018-05-02 02:22:47.143951'),
('0','超级管理员','[\"admin:main\", \"admin:quick\", \"admin:user:iframe\", \"admin:index:index\", \"admin:index:welcome\", \"warehousing:index\", \"warhousing:customer\", \"warehousing:instorage:admin\", \"warehousing:instorageapply:index\", \"warehousing:instorage:index\", \"warehousing:outstorage:admin\", \"warehousing:outstorage:index\", \"warehousing:storage:admin\", \"warehousing:storage:index\", \"warehousing:voucher:admin\", \"warehousing:voucher:index\", \"admin:system\", \"admin:system:function\", \"admin:system:setting\", \"admin:config:index\", \"admin:menu:index\", \"admin:user:role\", \"admin:user:index\", \"admin:role:index\", \"admin:annex:index\", \"admin:log:index\", \"admin:language:index\", \"admin:member\", \"admin:member:level\", \"admin:member:index\", \"admin:extend\", \"admin:module:index\", \"admin:plugins:admin\", \"admin:hook:index\", \"admin:upgrade:index\", \"admin:develop\", \"admin:develop:lists\", \"admin:develop:edit\"]',1,1,'2018-03-05 07:27:44.537284');
/*!40000 ALTER TABLE `sys_admin_role` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='后台管用户表';
/*!40101 SET character_set_client = @saved_cs_client */;


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
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='后台用户登录日志';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_admin_user_login_log`
--

LOCK TABLES `sys_admin_user_login_log` WRITE;
/*!40000 ALTER TABLE `sys_admin_user_login_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_admin_user_login_log` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `sys_config`
--

LOCK TABLES `sys_config` WRITE;
/*!40000 ALTER TABLE `sys_config` DISABLE KEYS */;
INSERT INTO `sys_config` VALUES ('login_pwd_rsa_encrypt','1','登录密码使用RSA算法加密',1,'系统登录开启RSA加密',1,1,'2018-02-27 12:21:28.000000'),
('sys_login_rsa_priv_key','-----BEGIN RSA PRIVATE KEY-----\nMIICXQIBAAKBgQDxKL1RrEcd4szM8Df4HqsJdOvKrSQO7BBvBVsvXKfpWrM+8XGL\n1SP7nsQd6alhntotPSDezaHnFvhnP/sr8bwzzorr1dWoBVabqDFZgZ2awB7iTk4k\n/3RN1TEPoD08kaJQ0xBHZ14395q8bVh22Uh10eCO/xtHnso3I6penSvRawIDAQAB\nAoGAQKctalIHlumRAnh8aNa///8KoAGfIykCluEWuzHaCmO4nm1YhaaUyQadiW91\na6iM0YgL4e+7MhskaXnrurJKRAweJP49OHz2JbLwyE7N7FWlY++1RVwWE32645CT\nt8hkAyFBBBR0J1by8HdGnPa69sJ6wwBYoh3SeCM8R92cfsECQQD+TbbYV/lw9KQD\nju+18bWpAyQeMBdx11OfgN3fBkRwrl9M0DHzwFKwDY7zFxPuYKD5I39wNeSbYYHJ\n9my6/JybAkEA8sST9CmwLgCoRwciUdxH4hOW8uAdGC9T2VYSo/BbO/geF09c+Ggx\nSoyEFIoAUMDC53Yj4dXgks0gnwWygRyjcQJBAN/P59+qNbgLJ5qWHzTDYX05bX1A\nGDIyL7/Ou/bAXlXJscg55+y+VEfr9ubNZdZDpwj+C/fnBqcV/xOP1QwQrYcCQQC+\ncO0rxaQ6gjN//J20n9wYAowQnTTVqxLY1Ies6Tl40swwNwbUq0+3joFyZ0uWDZEX\n5/qAB7qzDo1/kgWU+TVRAkAwAdK+p5ippKmp2efsdqRjb/71n+EX9adpo/Wh5Ece\nVp+MQkKMwNsQCkEthc/jEv4eG/urmWkLxaISAJRNegN2\n-----END RSA PRIVATE KEY-----','登录RSA算法加密私钥',3,'',1,1,'2018-05-04 15:19:45.205311'),
('site_name','LeeyiSoft','前端站点名称',20,'',1,1,'2018-05-07 07:27:48.849993'),
('sys_login_rsa_pub_key','-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDxKL1RrEcd4szM8Df4HqsJdOvK\nrSQO7BBvBVsvXKfpWrM+8XGL1SP7nsQd6alhntotPSDezaHnFvhnP/sr8bwzzorr\n1dWoBVabqDFZgZ2awB7iTk4k/3RN1TEPoD08kaJQ0xBHZ14395q8bVh22Uh10eCO\n/xtHnso3I6penSvRawIDAQAB\n-----END PUBLIC KEY-----','登录RSA算法加密公钥',2,'系统登录RSA加密公钥',1,1,'2018-02-27 06:34:50.196969'),
('system.name','LeeSoft','系统名称',20,'',1,1,'2018-05-06 00:56:16.890503'),
('system.version','vsn1.0.1','软件版本',20,'',1,1,'2018-05-06 00:57:44.192517'),
('site_url','http://localhost:5080','前台站点网址',20,'注意不要以 / 结尾',1,1,'2018-05-04 16:05:59.184771'),
('register_protocol','<div class=\"protocol\">\n   <h3 align=\"center\">用户注册协议</h3>\n   <p>\n    </p><h4>一、总则</h4>\n    1.1  XX网的所有权和运营权归XXXXXX有限公司所有。 <br>\n1.2  用户在注册之前，应当仔细阅读本协议，并同意遵守本协议后方可成为注册用户。一旦注册成功，则用户与XX网之间自动形成协议关系，用户应当受本协议的约束。用户在使用特殊的服务或产品时，应当同意接受相关协议后方能使用。  <br>\n1.3 本协议则可由XX网随时更新，用户应当及时关注并同意本站不承担通知义务。本站的通知、公告、声明或其它类似内容是本协议的一部分。  \n   <p></p>\n   <p>\n   </p><h4>二、服务内容</h4>\n   2.1 XX网的具体内容由本站根据实际情况提供。 <br>\n2.2 本站仅提供相关的网络服务，除此之外与相关网络服务有关的设备(如个人电脑、手机、及其他与接入互联网或移动网有关的装置)及所需的费用(如为接入互联网而支付的电话费及上网费、为使用移动网而支付的手机费)均应由用户自行负担。\n   <p></p>\n   <p>\n    </p><h4>三、用户帐号</h4>\n    3.1 经本站注册系统完成注册程序并通过身份认证的用户即成为正式用户，可以获得本站规定用户所应享有的一切权限；未经认证仅享有本站规定的部分会员权限。XX网有权对会员的权限设计进行变更。 <br>\n3.2 用户只能按照注册要求使用真实姓名，及身份证号注册。用户有义务保证密码和帐号的安全，用户利用该密码和帐号所进行的一切活动引起的任何损失或损害，由用户自行承担全部责任，本站不承担任何责任。如用户发现帐号遭到未授权的使用或发生其他任何安全问题，应立即修改帐号密码并妥善保管，如有必要，请通知本站。因黑客行为或用户的保管疏忽导致帐号非法使用，本站不承担任何责任。 \n   <p></p>\n   <p>\n    </p><h4>四、使用规则</h4>\n    4.1 遵守中华人民共和国相关法律法规，包括但不限于《中华人民共和国计算机信息系统安全保护条例》、《计算机软件保护条例》、《最高人民法院关于审理涉及计算机网络著作权纠纷案件适用法律若干问题的解释(法释[2004]1号)》、《全国人大常委会关于维护互联网安全的决定》、《互联网电子公告服务管理规定》、《互联网新闻信息服务管理规定》、《互联网著作权行政保护办法》和《信息网络传播权保护条例》等有关计算机互联网规定和知识产权的法律和法规、实施办法。 <br> \n4.2  用户对其自行发表、上传或传送的内容负全部责任，所有用户不得在本站任何页面发布、转载、传送含有下列内容之一的信息，否则本站有权自行处理并不通知用户：<br> \n<span>(1)违反宪法确定的基本原则的； <br> \n(2)危害国家安全，泄漏国家机密，颠覆国家政权，破坏国家统一的； <br> \n(3)损害国家荣誉和利益的； <br> \n(4)煽动民族仇恨、民族歧视，破坏民族团结的； <br> \n(5)破坏国家宗教政策，宣扬邪教和封建迷信的； <br> \n(6)散布谣言，扰乱社会秩序，破坏社会稳定的；<br>  \n(7)散布淫秽、色情、赌博、暴力、恐怖或者教唆犯罪的； <br> \n(8)侮辱或者诽谤他人，侵害他人合法权益的； <br> \n(9)煽动非法集会、结社、游行、示威、聚众扰乱社会秩序的； <br> \n(10)以非法民间组织名义活动的；<br>\n(11)含有法律、行政法规禁止的其他内容的。\n</span>\n4.3 用户承诺对其发表或者上传于本站的所有信息(即属于《中华人民共和国著作权法》规定的作品，包括但不限于文字、图片、音乐、电影、表演和录音录像制品和电脑程序等)均享有完整的知识产权，或者已经得到相关权利人的合法授权；如用户违反本条规定造成本站被第三人索赔的，用户应全额补偿本站一切费用(包括但不限于各种赔偿费、诉讼代理费及为此支出的其它合理费用)；  <br>\n4.4 当第三方认为用户发表或者上传于本站的信息侵犯其权利，并根据《信息网络传播权保护条例》或者相关法律规定向本站发送权利通知书时，用户同意本站可以自行判断决定删除涉嫌侵权信息，除非用户提交书面证据材料排除侵权的可能性，本站将不会自动恢复上述删除的信息； \n<span>\n (1)不得为任何非法目的而使用网络服务系统； <br>\n(2)遵守所有与网络服务有关的网络协议、规定和程序； \n(3)不得利用本站进行任何可能对互联网的正常运转造成不利影响的行为； <br>\n(4)不得利用本站进行任何不利于本站的行为。\n</span>\n4.5 如用户在使用网络服务时违反上述任何规定，本站有权要求用户改正或直接采取一切必要的措施(包括但不限于删除用户张贴的内容、暂停或终止用户使用网络服务的权利)以减轻用户不当行为而造成的影响。\n   <p></p><p>\n   </p><h4>五、隐私保护</h4>\n   5.1 本站不对外公开或向第三方提供单个用户的注册资料及用户在使用网络服务时存储在本站的非公开内容，但下列情况除外：\n   <span>\n    (1)事先获得用户的明确授权； <br>\n(2)根据有关的法律法规要求；<br> \n(3)按照相关政府主管部门的要求；<br> \n(4)为维护社会公众的利益。\n   </span>\n   5.2  本站可能会与第三方合作向用户提供相关的网络服务，在此情况下，如该第三方同意承担与本站同等的保护用户隐私的责任，则本站有权将用户的注册资料等提供给该第三方。<br> \n5.3 在不透露单个用户隐私资料的前提下，本站有权对整个用户数据库进行分析并对用户数据库进行商业上的利用。<p></p>\n<p>\n</p><h4>六、版权声明</h4>\n6.1 本站的文字、图片、音频、视频等版权均归永兴元科技有限公司享有或与作者共同享有，未经本站许可，不得任意转载。 <br> \n6.2 本站特有的标识、版面设计、编排方式等版权均属永兴元科技有限公司享有，未经本站许可，不得任意复制或转载。  <br> \n6.3 使用本站的任何内容均应注明“来源于XX网”及署上作者姓名，按法律规定需要支付稿酬的，应当通知本站及作者及支付稿酬，并独立承担一切法律责任。<br>   \n6.4 本站享有所有作品用于其它用途的优先权，包括但不限于网站、电子杂志、平面出版等，但在使用前会通知作者，并按同行业的标准支付稿酬。<br>   \n6.5 本站所有内容仅代表作者自己的立场和观点，与本站无关，由作者本人承担一切法律责任。 <br> \n6.6 恶意转载本站内容的，本站保留将其诉诸法律的权利。\n<p></p>\n<p>\n</p><h4>七、责任声明</h4>\n7.1 用户明确同意其使用本站网络服务所存在的风险及一切后果将完全由用户本人承担，XX网对此不承担任何责任。 <br> \n7.2 本站无法保证网络服务一定能满足用户的要求，也不保证网络服务的及时性、安全性、准确性。 <br>  \n7.3 本站不保证为方便用户而设置的外部链接的准确性和完整性，同时，对于该等外部链接指向的不由本站实际控制的任何网页上的内容，本站不承担任何责任。<br>   \n7.4 对于因不可抗力或本站不能控制的原因造成的网络服务中断或其它缺陷，本站不承担任何责任，但将尽力减少因此而给用户造成的损失和影响。<br>   \n7.5 对于站向用户提供的下列产品或者服务的质量缺陷本身及其引发的任何损失，本站无需承担任何责任：\n<span>\n (1)本站向用户免费提供的各项网络服务； <br>   \n(2)本站向用户赠送的任何产品或者服务。 \n</span>\n7.6 本站有权于任何时间暂时或永久修改或终止本服务(或其任何部分)，而无论其通知与否，本站对用户和任何第三人均无需承担任何责任。<p></p>\n<p>\n</p><h4>八、附则</h4>\n8.1  本协议的订立、执行和解释及争议的解决均应适用中华人民共和国法律。  <br>  \n8.2  如本协议中的任何条款无论因何种原因完全或部分无效或不具有执行力，本协议的其余条款仍应有效并且有约束力。<br>    \n8.3  本协议解释权及修订权归XXXXX有限公司所有。\n\n<p></p>\n  </div>','会员注册协议',20,'',0,1,'2018-05-12 01:41:21.218692');
/*!40000 ALTER TABLE `sys_config` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `sys_message`
--

LOCK TABLES `sys_message` WRITE;
/*!40000 ALTER TABLE `sys_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_message` ENABLE KEYS */;
UNLOCK TABLES;

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

--
-- Dumping data for table `sys_sequence`

DELIMITER $$
DROP FUNCTION IF EXISTS `currval`$$
CREATE DEFINER=`root`@`%` FUNCTION `currval`(seq_name VARCHAR(40)) RETURNS INT(11)
BEGIN
DECLARE ret_value INTEGER;
SET ret_value=0;
SELECT `value` INTO ret_value
FROM sys_sequence
WHERE `key`=seq_name;
RETURN ret_value;
END$$
DELIMITER ;

DELIMITER $$
DROP FUNCTION IF EXISTS `nextval`$$
CREATE DEFINER=`root`@`%` FUNCTION `nextval`(seq_name varchar(40), incr int(11)) RETURNS int(11)
BEGIN
UPDATE `sys_sequence`
SET `value` = `value` + incr
where `key`=seq_name;
return currval(seq_name);
END$$
