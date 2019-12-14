#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, DECIMAL, String, text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT

from trest.db import Model as Base


class Address(Base):
    __tablename__ = 'address'

    id = Column(BIGINT(20), primary_key=True, comment='主键')
    region = Column(String(8), nullable=False, server_default=text("'86'"), comment='所属区域码 CN')
    address = Column(String(200), comment='详细地址 街道门牌号')
    longitude = Column(DECIMAL(12, 9), nullable=False, server_default=text("'0.000000000'"), comment='位置经度')
    latitude = Column(DECIMAL(12, 9), nullable=False, server_default=text("'0.000000000'"), comment='位置纬度')
    province_id = Column(String(8), nullable=False, server_default=text("''"), comment='省编码')
    city_id = Column(String(8), nullable=False, server_default=text("''"), comment='市编码')
    county_id = Column(String(8), nullable=False, server_default=text("''"), comment='区编码')
    status = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='状态:( 0 禁用；1 启用, 默认1 删除 -1)')
    created_at = Column(BIGINT(13), nullable=False, server_default=text("'0'"), comment='创建记录Unix时间戳毫秒单位')
