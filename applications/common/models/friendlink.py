#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Enum, String, text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT

from trest.db import Model as Base


class Friendlink(Base):
    __tablename__ = 'friendlink'

    id = Column(BIGINT(20), primary_key=True)
    title = Column(String(80), nullable=False, server_default=text("''"), comment='链接标题')
    logo = Column(String(255), nullable=False, server_default=text("''"), comment='链接图标')
    url = Column(String(255), nullable=False, server_default=text("''"), comment='链接地址')
    target = Column(Enum('_blank', '_self', ''), nullable=False, server_default=text("''"), comment='链接跳转方式')
    sort = Column(BIGINT(20), nullable=False, server_default=text("'20'"), comment='排序 降序排序，大的值在前面')
    status = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='状态:( 0 禁用；1 启用, 默认1 删除 -1)')
    updated_at = Column(BIGINT(13), nullable=False, server_default=text("'0'"), comment='更新记录Unix时间戳毫秒单位')
    created_at = Column(BIGINT(13), nullable=False, server_default=text("'0'"), comment='创建记录Unix时间戳毫秒单位')
