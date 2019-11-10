#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT

from trest.db import Model as Base


class Config(Base):
    __tablename__ = 'config'

    tab = Column(String(20), comment='配置选项，便于后台分类浏览')
    key = Column(String(40), primary_key=True, server_default=text(''), comment='主键')
    value = Column(String(2000), server_default=text(''))
    title = Column(String(40), comment='标题')
    sort = Column(BIGINT(20), nullable=False, server_default=text('20'), comment='排序 降序排序，大的值在前面')
    remark = Column(String(128), nullable=False)
    system = Column(TINYINT(1), nullable=False, server_default=text('0'), comment='是否为系统配置，系统配置不可删除')
    status = Column(TINYINT(1), nullable=False, server_default=text('1'), comment='状态:( 0 禁用；1 启用, 默认1 删除 -1)')
    created_at = Column(BIGINT(13), nullable=False, server_default=text('0'), comment='创建记录Unix时间戳毫秒单位')
    updated_at = Column(BIGINT(13), nullable=False, server_default=text('0'), comment='更新记录Unix时间戳毫秒单位')
