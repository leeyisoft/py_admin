#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Text, text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT

from trest.db import Model as Base


class AdminUser(Base):
    __tablename__ = 'admin_user'

    id = Column(BIGINT(20), primary_key=True, comment='主键')
    role_id = Column(BIGINT(20), comment='角色ID')
    password = Column(String(128), nullable=False)
    username = Column(String(40))
    mobile = Column(String(11))
    email = Column(String(80))
    permission = Column(Text, comment='用户权限（存储菜单uuid，以json格式存储，最终权限是用户和角色权限的交集）')
    login_count = Column(BIGINT(20), server_default=text('0'), comment='登录次数')
    last_login_ip = Column(String(40), comment='最后登陆IP')
    last_login_at = Column(BIGINT(13), comment='最后登录Unix时间戳毫秒单位')
    status = Column(TINYINT(1), nullable=False, server_default=text('1'), comment='状态:( 0 禁用；1 启用, 默认1 删除 -1)')
    created_at = Column(BIGINT(13), nullable=False, server_default=text('0'), comment='创建记录Unix时间戳毫秒单位')
    lang = Column(String(20), nullable=False, server_default=text(''), comment='默认客户端语言')
