#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, JSON, String, text
from sqlalchemy.dialects.mysql import BIGINT, LONGTEXT, TINYINT

from trest.db import Model as Base


class Goods(Base):
    __tablename__ = 'goods'

    id = Column(BIGINT(20), primary_key=True, comment='主键')
    category_id = Column(BIGINT(20), nullable=False, comment='分类')
    title = Column(String(200), nullable=False, comment='标题')
    thumb = Column(String(255), nullable=False, server_default=text("''"), comment='缩略图')
    album = Column(JSON, comment='相册，["image_url",...]')
    external_url = Column(String(255), nullable=False, server_default=text("''"), comment='外链地址')
    keyword = Column(String(255), nullable=False, server_default=text("''"), comment='SEO关键词')
    description = Column(String(255), nullable=False, server_default=text("''"), comment='SEO描述')
    hits = Column(BIGINT(20), server_default=text("'0'"), comment='点击数量')
    importance = Column(TINYINT(4), server_default=text("'0'"), comment='价值')
    market_price = Column(BIGINT(20), nullable=False, server_default=text("'0'"), comment='市场价格，单位分')
    price = Column(BIGINT(20), nullable=False, server_default=text("'0'"), comment='销售价格，单位分')
    inventory_quantity = Column(BIGINT(20), nullable=False, server_default=text("'0'"), comment='库存数量')
    sales_quantity = Column(BIGINT(20), nullable=False, server_default=text("'0'"), comment='销售数量')
    extra = Column(JSON, comment='额外信息，例如商品的尺寸、颜色、其他规格等')
    detail = Column(LONGTEXT, comment='详情')
    status = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='状态:( 0 禁用；1 启用, 默认1 删除 -1)')
    created_at = Column(BIGINT(13), nullable=False, server_default=text("'0'"), comment='创建记录Unix时间戳毫秒单位')
