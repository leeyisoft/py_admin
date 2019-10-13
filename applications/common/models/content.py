#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json
import os

from tornado.escape import json_decode

from trest.config import settings
from trest.cache import cache

from trest.logger.client import SysLogger
from trest.utils import utime
from trest.db import Model as BaseModel

from sqlalchemy.types import Integer
from sqlalchemy.types import Numeric
from sqlalchemy.types import VARCHAR
from sqlalchemy.types import VARCHAR
from sqlalchemy.types import Text
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.types import DATETIME
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import PrimaryKeyConstraint


class ArticleCategory(BaseModel):
    """
    sys_article_category model
    """
    __tablename__ = 'sys_article_category'

    id = Column(Integer, primary_key=True)
    lang = Column(VARCHAR(10), nullable=True, default='')
    title = Column(VARCHAR(20), nullable=True, default='')
    name = Column(VARCHAR(80), nullable=False, default='')

class Article(BaseModel):
    """
    sys_article model
    """
    __tablename__ = 'sys_article'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('sys_article_category.id'))
    lang = Column(VARCHAR(10), nullable=True, default='')
    user_id = Column(Integer, ForeignKey('sys_admin_user.id'))
    title = Column(VARCHAR(80), nullable=False, default='')
    author = Column(VARCHAR(20), nullable=True, default='')
    source = Column(VARCHAR(20), nullable=True, default='')
    external_url = Column(VARCHAR(255), nullable=True, default='')
    thumb = Column(VARCHAR(255), nullable=True, default='')
    keyword = Column(VARCHAR(255), nullable=True, default='')
    description = Column(VARCHAR(255), nullable=True, default='')
    publish_date = Column(Integer, nullable=True, default=0)
    hits = Column(Integer, nullable=False, default=0)
    content = Column(Text, nullable=True, default='')
    ip = Column(VARCHAR(40), nullable=False)
    # 用户状态:(0 锁定, 1正常, 默认1)
    status = Column(Integer, nullable=False, default=1)
    updated_at = Column(TIMESTAMP, default=None)
    created_at = Column(TIMESTAMP, default=utime.timestamp(3))
