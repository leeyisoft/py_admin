#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT

from trest.db import Model as Base


class Advertising(Base):
    __tablename__ = 'advertising'

    id = Column(BIGINT(20), primary_key=True)
    title = Column(String(80), nullable=False, server_default=text("''"), comment='标题')
    description = Column(String(255), comment='描述')
    start_at = Column(BIGINT(13), comment='投放开始Unix时间戳毫秒单位')
    end_at = Column(BIGINT(13), nullable=False, server_default=text("'0'"), comment='投放结束Unix时间戳毫秒单位0 为无限')
    created_at = Column(BIGINT(13), nullable=False, comment='创建记录Unix时间戳毫秒单位')
    type = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='广告类型 1 内部网页 2外部网页')
    client = Column(String(40), nullable=False, server_default=text("''"), comment='客户端：web wechat android ios 同时支持多个的话，用半角逗号分隔 ')
    img = Column(String(255), nullable=False, comment='图片链接')
    link = Column(String(255), comment='跳转地址链接')
    category_id = Column(BIGINT(20), nullable=False, comment='广告分类 投放位置')
    status = Column(TINYINT(1), server_default=text("'1'"), comment='状态:( 0 禁用；1 启用, 默认1 删除 -1)')
