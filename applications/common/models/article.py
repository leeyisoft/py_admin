#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT, LONGTEXT, TINYINT

from trest.db import Model as Base


class Article(Base):
    __tablename__ = 'article'

    id = Column(BIGINT(20), primary_key=True)
    category_id = Column(BIGINT(20), comment='文章分类ID')
    lang = Column(String(10), server_default=text('cn'), comment='默认语言：cn zh-CN中文(简体) id d-ID 印度尼西亚语 en en-US 英语(美国) en-PH 英语(菲律宾)')
    user_id = Column(BIGINT(20), nullable=False, server_default=text('0'), comment='发布用户')
    title = Column(String(80), nullable=False, server_default=text(''), comment='文章标题')
    author = Column(String(20), nullable=False, server_default=text(''), comment='作者')
    source = Column(String(20), nullable=False, server_default=text(''), comment='来源')
    external_url = Column(String(255), nullable=False, server_default=text(''), comment='外链地址')
    thumb = Column(String(255), nullable=False, server_default=text(''), comment='缩略图')
    keyword = Column(String(255), nullable=False, server_default=text(''), comment='SEO关键词')
    description = Column(String(255), nullable=False, server_default=text(''), comment='文章摘要 SEO描述')
    publish_date = Column(BIGINT(13), nullable=False, comment='发布日期Unix时间戳毫秒单位')
    hits = Column(BIGINT(20), server_default=text('0'), comment='点击数量')
    content = Column(LONGTEXT, comment='文章内容（如果是产品的话，为json格式数据）')
    ip = Column(String(40), comment='添加记录的IP地址')
    updated_at = Column(BIGINT(13), nullable=False, server_default=text('0'), comment='更新记录Unix时间戳毫秒单位')
    created_at = Column(BIGINT(13), nullable=False, server_default=text('0'), comment='创建记录Unix时间戳毫秒单位')
    status = Column(TINYINT(1), nullable=False, server_default=text('1'), comment='状态:( 0 禁用；1 启用, 默认1)')
