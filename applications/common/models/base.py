#!/usr/bin/env python
# -*- coding: utf-8  -*-
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.types import TEXT
from sqlalchemy.types import VARCHAR
from sqlalchemy.types import TIMESTAMP
from sqlalchemy_utils import ChoiceType

from applications.common import const
from trest.utils import utime
from trest.settings_manager import settings
from trest.db import Model as BaseModel


class Config(BaseModel):
    """
    sys_config model
    """
    __tablename__ = 'sys_config'

    key = Column(String(40), primary_key=True, nullable=False)
    value = Column(String(400), nullable=False)
    title = Column(String(40), nullable=False)
    remark = Column(String(128), nullable=False, default='')
    sort = Column(Integer, nullable=False, default=20)
    system = Column(Integer, nullable=False, default=0)
    # 状态:( 0 禁用；1 启用, 默认1)
    status = Column(Integer, nullable=False, default=1)
    created_at = Column(TIMESTAMP, default=utime.timestamp)


class Advertising(BaseModel):
    """
        advertising 广告列表
    """
    __tablename__ = 'sys_advertising'

    id = Column(Integer, primary_key=True, nullable=False)
    # 客户端语言：cn 简体中文 en 英语 id 印尼语 ph 菲律宾语
    lang = Column(String(10), nullable=True, default='en')
    title = Column(String(80), nullable=False)  # 标题
    start_at = Column(Integer, nullable=False, default=0)  # 投放开始时间
    end_at = Column(Integer, nullable=False, default=-1)  # 投放结束时间
    created_at = Column(Integer, nullable=False, default=utime.timestamp)  # 创建时间
    type = Column(Integer, nullable=False, default=1)  # 广告类型 1. 内接 2.外链
    client = Column(String(20), nullable=False)  # 投放的客户端
    img = Column(String(255), nullable=False)  # 图片链接
    link = Column(String(255), nullable=False)  # 跳转链接
    effects = Column(String(20), nullable=False)  # 特效
    category_id = Column(Integer, nullable=False)  # 分类id
    status = Column(Integer, nullable=False, default=1)


class AdvertisingCategory(BaseModel):
    """
        advertising_category 广告分类
    """
    __tablename__ = 'sys_advertising_category'

    id = Column(Integer, primary_key=True, nullable=False)
    # 客户端语言：cn 简体中文 en 英语 id 印尼语 ph 菲律宾语
    lang = Column(ChoiceType(const.LANG_TYPE), nullable=True, default='en')
    name = Column(String(80), nullable=False)
    status = Column(ChoiceType(const.COMMON_STATUS2), default=1)


class AdvertisingLog(BaseModel):
    """
        advertising_log 广告记录
    """
    __tablename__ = 'sys_advertising_log'

    id = Column(Integer, primary_key=True, nullable=False)
    ad_id = Column(Integer, nullable=False)
    uid = Column(Integer, nullable=False)
    created_at = Column(Integer, default=1)
    ip = Column(String(20), nullable=True)


