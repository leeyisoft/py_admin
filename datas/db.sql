CREATE TABLE `wms_stockin` (
  `uuid` char(36) NOT NULL COMMENT '主键',
  `number` varchar(40) NOT NULL COMMENT '入库单编号',
  `quantity` int(11) NOT NULL DEFAULT '1' COMMENT '物品数量，单位：件',
  `stevedorage` decimal(12,2) NOT NULL,
  `sitefee` decimal(12,2) NOT NULL,
  `healthfee` decimal(12,2) NOT NULL,
  `remark` varchar(255) DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `order` int(10) unsigned NOT NULL,
  `admin_id` int(11) DEFAULT NULL,
  `borrower_id` int(11) DEFAULT NULL,
  `contract_id` int(11) DEFAULT NULL,
  `location_id` int(11) NOT NULL,
  `salesman_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`uuid`),
  UNIQUE KEY `uk_number` (`number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='入库单表 wms(warehouse management system)';

wms_stockin_godds_map

CREATE TABLE `wms_goods` (
  `uuid` char(36) NOT NULL COMMENT '主键',
  `name` varchar(80) NOT NULL COMMENT '物品名称',
  `quantity` int(11) NOT NULL DEFAULT '1' COMMENT '物品数量，单位：件',
  `weight` decimal(11,3) NOT NULL DEFAULT '1' COMMENT '重量，单位：千克',
  `volume` decimal(11,3) NOT NULL DEFAULT '1' COMMENT '体积，单位：立方米',
  `length` decimal(11,3) NOT NULL DEFAULT '1' COMMENT '长度，单位：米',
  `width` decimal(11,3) NOT NULL DEFAULT '1' COMMENT '宽度，单位：米',
  `height` decimal(11,3) NOT NULL DEFAULT '1' COMMENT '高度，单位：米',
  `age` varchar(40) DEFAULT '' COMMENT '物品年份',
  `origin` varchar(40) DEFAULT '' COMMENT '物品产地',
  `log_grade` varchar(40) DEFAULT '' COMMENT '原木等级',
  `status` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '状态:( 0 禁用；1 启用, 默认1)',
  `deleted` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '已删除的 1 是 0 否 默认 0',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='入库物品表 wms(warehouse management system)';

CREATE TABLE `sys_config` (
  `key` varchar(40) NOT NULL COMMENT '主键',
  `value` text,
  `remark` varchar(128) NOT NULL,
  `status` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '状态:(0 无效, 1正常, 默认1)',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  PRIMARY KEY (`key`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='系统配置';

CREATE TABLE `user` (
  `uuid` char(36) NOT NULL COMMENT '主键',
  `password` varchar(128) NOT NULL,
  `username` varchar(40) DEFAULT NULL,
  `mobile` varchar(11) DEFAULT NULL,
  `email` varchar(80) DEFAULT NULL,
  `status` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '用户状态:(0 锁定, 1正常, 默认1)',
  `utc_last_login_at` datetime(6) DEFAULT NULL COMMENT '最后登录UTC时间',
  `deleted` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '已删除的 1 是 0 否 默认 0',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  PRIMARY KEY (`uuid`),
  UNIQUE KEY `uk_username` (`username`),
  UNIQUE KEY `uk_mobile` (`mobile`),
  UNIQUE KEY `uk_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户基础信息表';

CREATE TABLE `user_group` (
  `uuid` char(36) NOT NULL COMMENT '主键',
  `groupname` varchar(40) DEFAULT NULL COMMENT '分组名称',
  `permission` text COMMENT '用户组权限（存储的是授权节点的url，以半角逗号分隔、结尾）',
  `status` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '状态:( 0 禁用；1 启用, 默认1)',
  `deleted` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '已删除的 1 是 0 否 默认 0',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  PRIMARY KEY (`uuid`),
  UNIQUE KEY `uk_name` (`groupname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户分组表';

CREATE TABLE `user_group_map` (
  `user_id` varchar(32) NOT NULL COMMENT '用户唯一标示',
  `group_id` varchar(32) NOT NULL COMMENT '用户组ID',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  UNIQUE KEY `uk_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户分组表';

CREATE TABLE `user_login_log` (
  `uuid` char(36) NOT NULL COMMENT '主键',
  `user_id` char(36) NOT NULL DEFAULT '' COMMENT '用户唯一标示',
  `login_at` datetime(6) DEFAULT NULL COMMENT '登录UTC时间',
  `ip` varchar(40) DEFAULT NULL COMMENT '登录IP',
  `client` varchar(20) DEFAULT NULL COMMENT '客户端：web wechat android ios ',
  `utc_created_at` datetime(6) DEFAULT NULL COMMENT '创建记录UTC时间',
  PRIMARY KEY (`uuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='用户登录日志';


INSERT INTO `sys_config` (`key`, `value`, `remark`, `status`, `utc_created_at`)
VALUES
  ('login_pwd_rsa_encrypt', '1', '系统登录开启RSA加密', 1, '2018-02-27 12:21:28.000000'),
  ('sys_login_rsa_pub_key', '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDxKL1RrEcd4szM8Df4HqsJdOvK\nrSQO7BBvBVsvXKfpWrM+8XGL1SP7nsQd6alhntotPSDezaHnFvhnP/sr8bwzzorr\n1dWoBVabqDFZgZ2awB7iTk4k/3RN1TEPoD08kaJQ0xBHZ14395q8bVh22Uh10eCO\n/xtHnso3I6penSvRawIDAQAB\n-----END PUBLIC KEY-----\n', '系统登录RSA加密公钥', 1, '2018-02-27 06:34:50.196969'),
  ('sys_login_rsa_priv_key', '-----BEGIN RSA PRIVATE KEY-----\nMIICXQIBAAKBgQDxKL1RrEcd4szM8Df4HqsJdOvKrSQO7BBvBVsvXKfpWrM+8XGL\n1SP7nsQd6alhntotPSDezaHnFvhnP/sr8bwzzorr1dWoBVabqDFZgZ2awB7iTk4k\n/3RN1TEPoD08kaJQ0xBHZ14395q8bVh22Uh10eCO/xtHnso3I6penSvRawIDAQAB\nAoGAQKctalIHlumRAnh8aNa///8KoAGfIykCluEWuzHaCmO4nm1YhaaUyQadiW91\na6iM0YgL4e+7MhskaXnrurJKRAweJP49OHz2JbLwyE7N7FWlY++1RVwWE32645CT\nt8hkAyFBBBR0J1by8HdGnPa69sJ6wwBYoh3SeCM8R92cfsECQQD+TbbYV/lw9KQD\nju+18bWpAyQeMBdx11OfgN3fBkRwrl9M0DHzwFKwDY7zFxPuYKD5I39wNeSbYYHJ\n9my6/JybAkEA8sST9CmwLgCoRwciUdxH4hOW8uAdGC9T2VYSo/BbO/geF09c+Ggx\nSoyEFIoAUMDC53Yj4dXgks0gnwWygRyjcQJBAN/P59+qNbgLJ5qWHzTDYX05bX1A\nGDIyL7/Ou/bAXlXJscg55+y+VEfr9ubNZdZDpwj+C/fnBqcV/xOP1QwQrYcCQQC+\ncO0rxaQ6gjN//J20n9wYAowQnTTVqxLY1Ies6Tl40swwNwbUq0+3joFyZ0uWDZEX\n5/qAB7qzDo1/kgWU+TVRAkAwAdK+p5ippKmp2efsdqRjb/71n+EX9adpo/Wh5Ece\nVp+MQkKMwNsQCkEthc/jEv4eG/urmWkLxaISAJRNegN2\n-----END RSA PRIVATE KEY-----\n', '系统登录RSA加密私钥', 1, '2018-02-27 06:34:50.196969'),
  ('front_end_title', '前端标题', '前端标题', 1, '2018-02-27 06:34:50.196969');

