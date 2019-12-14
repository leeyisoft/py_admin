#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT

from trest.db import Model as Base


class ArticleCategory(Base):
    __tablename__ = 'article_category'

    id = Column(BIGINT(20), primary_key=True)
    lang = Column(String(10), server_default=text("'cn'"), comment='默认语言：cn zh-CN中文(简体) id d-ID 印度尼西亚语 en en-US 英语(美国) en-PH 英语(菲律宾)')
    title = Column(String(64), comment='分类名称')
    name = Column(String(40), comment='分类唯一标示')
    status = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='状态:( 0 禁用；1 启用, 默认1)')
