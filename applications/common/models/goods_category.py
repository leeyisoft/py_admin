#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT

from trest.db import Model as Base


class GoodsCategory(Base):
    __tablename__ = 'goods_category'

    id = Column(BIGINT(20), primary_key=True)
    name = Column(String(40), comment='唯一标识')
    title = Column(String(80), nullable=False, server_default=text("''"), comment='分类名称')
    status = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='状态:( 0 禁用；1 启用, 默认1 删除 -1)')
