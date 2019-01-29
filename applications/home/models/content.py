#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json
import os

from tornado.escape import json_decode

from applications.core.settings_manager import settings
from applications.core.cache import cache

from applications.core.logger.client import SysLogger
from applications.core.utils import Func
from applications.core.models import BaseModel

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


class Article(BaseModel):
    """
    user model
    """
    __tablename__ = 'home_article'

    id = Column(Integer, primary_key=True)
    category = Column(VARCHAR(20), nullable=True, default='')
    user_id = Column(Integer, ForeignKey('member.id'))
    title = Column(VARCHAR(80), nullable=False, default='')
    author = Column(VARCHAR(20), nullable=True, default='')
    source = Column(VARCHAR(20), nullable=True, default='')
    external_url = Column(VARCHAR(255), nullable=True, default='')
    thumb = Column(VARCHAR(255), nullable=True, default='')
    keyword = Column(VARCHAR(255), nullable=True, default='')
    description = Column(VARCHAR(255), nullable=True, default='')
    publish_date = Column(DATETIME, nullable=True, default='')
    hits = Column(Integer, nullable=False, default=0)
    content = Column(Text, nullable=True, default='')
    ip = Column(VARCHAR(40), nullable=False)
    # 用户状态:(0 锁定, 1正常, 默认1)
    status = Column(Integer, nullable=False, default=1)
    utc_updated_at = Column(TIMESTAMP, default=None)
    utc_created_at = Column(TIMESTAMP, default=Func.utc_now)

    @property
    def created_at(self):
        return Func.dt_to_timezone(self.utc_created_at)

    @property
    def updated_at(self):
        return Func.dt_to_timezone(self.utc_updated_at)

    category_options = {
        'activity': '新闻活动',
        'regulation': '政策法规',
        'product': '产品展示',
    }

    @property
    def category_option(self):
        return self.category_options.get(self.category, '')

    @staticmethod
    def category_option_html(category=''):
        html = '<option value="">请选择分类</option>'
        option = '<option value="%s" %s>%s</option>'
        for key in Article.category_options:
            selected = 'selected="true"' if category==key else ''
            html += option % (key, selected, Article.category_options[key])
        # print("html", sex, html)
        return html

    @staticmethod
    def populars(limit=8):
        now = Func.utc_now()
        today = '%d-%d-%d' % (now.year, now.month, now.day)
        query = Article.Q
        query = query.filter(Article.status==1)
        query = query.filter(Article.publish_date<=today)
        query = query.order_by(Article.hits.desc())
        return query.limit(limit).all()

    @staticmethod
    def detail(aid):
        now = Func.utc_now()
        today = '%d-%d-%d' % (now.year, now.month, now.day)
        query = Article.Q
        query = query.filter(Article.status==1)
        query = query.filter(Article.publish_date<=today)
        query = query.filter(Article.id==aid)
        arc = query.one()
        return arc.as_dict()

    @staticmethod
    def lists(option):
        per_page = option.get('per_page', 12)
        page = option.get('page', 1)
        category = option.get('category', '')
        now = Func.utc_now()
        today = '%d-%d-%d' % (now.year, now.month, now.day)
        query = Article.Q
        query = query.filter(Article.status==1)
        if category:
            query = query.filter(Article.category==category)
        query = query.filter(Article.publish_date<=today)
        query = query.order_by(Article.publish_date.desc())
        pagelist_obj = query.paginate(page=page, per_page=per_page)
        return pagelist_obj

class Contact(BaseModel):
    """
    Contact model
    """
    __tablename__ = 'home_contact'

    id = Column(Integer, primary_key=True)
    real_name = Column(VARCHAR(20), nullable=True, default='')
    phone = Column(VARCHAR(20), nullable=True, default='')
    message = Column(VARCHAR(400), nullable=True, default='')
    ip = Column(VARCHAR(40), nullable=False)
    # 用户状态:(0 锁定, 1正常, 默认1)
    status = Column(Integer, nullable=False, default=1)
    utc_created_at = Column(TIMESTAMP, default=Func.utc_now)


class Team(BaseModel):
    """
    Team model
    """
    __tablename__ = 'home_team'

    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(160), nullable=True, default='')
    description = Column(VARCHAR(400), nullable=True, default='')
    name = Column(VARCHAR(20), nullable=True, default='')
    avatar = Column(VARCHAR(255), nullable=True, default='')
    order = Column(Integer, nullable=False, default=20)
    # 用户状态:(0 锁定, 1正常, 默认1)
    status = Column(Integer, nullable=False, default=1)
    utc_created_at = Column(TIMESTAMP, default=Func.utc_now)
