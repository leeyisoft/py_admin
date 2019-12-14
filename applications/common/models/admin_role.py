#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Text, text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT

from trest.db import Model as Base


class AdminRole(Base):
    __tablename__ = 'admin_role'

    id = Column(BIGINT(20), primary_key=True, comment='主键')
    rolename = Column(String(40), comment='角色名称')
    permission = Column(Text, comment='角色权限（存储菜单uuid，以json格式存储）')
    sort = Column(BIGINT(20), nullable=False, server_default=text("'20'"), comment='排序 降序排序，大的值在前面')
    status = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='状态:( 0 禁用；1 启用, 默认1 删除 -1)')
    created_at = Column(BIGINT(13), nullable=False, server_default=text("'0'"), comment='创建记录Unix时间戳毫秒单位')
    description = Column(String(100), nullable=False, comment='描述')
