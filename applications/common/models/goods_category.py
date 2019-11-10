#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT

from trest.db import Model as Base


class GoodsCategory(Base):
    __tablename__ = 'goods_category'

    id = Column(BIGINT(20), primary_key=True)
    title = Column(String(64), comment='分类名称')
    name = Column(String(40), comment='分类唯一标示')
