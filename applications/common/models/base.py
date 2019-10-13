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
from sqlalchemy.types import Enum

from sqlalchemy_utils import ChoiceType

from trest.utils import utime
from trest.config import settings
from trest.db import Model as BaseModel

from applications.common import const


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
    created_at = Column(TIMESTAMP, default=utime.timestamp(3))


class Advertising(BaseModel):
    """
        advertising 广告列表
    """
    __tablename__ = 'sys_advertising'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(80), nullable=False)  # 标题
    start_at = Column(Integer, nullable=False, default=0)  # 投放开始时间
    end_at = Column(Integer, nullable=False, default=-1)  # 投放结束时间
    created_at = Column(Integer, nullable=False, default=utime.timestamp(3))  # 创建时间
    type = Column(Integer, nullable=False, default=1)  # 广告类型 1. 内接 2.外链
    client = Column(String(20), nullable=False)  # 投放的客户端
    img = Column(String(255), nullable=False)  # 图片链接
    link = Column(String(255), nullable=False)  # 跳转链接
    category_id = Column(Integer, nullable=False)  # 分类id
    status = Column(Integer, nullable=False, default=1)


class AdvertisingCategory(BaseModel):
    """
        advertising_category 广告分类
    """
    __tablename__ = 'sys_advertising_category'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(40), nullable=False)
    title = Column(String(80), nullable=False)
    status = Column(Integer, nullable=False, default=1)


class Company(BaseModel):
    """
    公司表
    """
    __tablename__ = 'sys_company'
    id = Column(Integer, primary_key=True, nullable=False, default=None)
    company_name = Column(String(50), nullable=True, default='')
    description = Column(String(50), nullable=True, default='')
    type = Column(ChoiceType(const.COMPANY_TYPE))  # 类型：（外部委派；内部)
    status = Column(ChoiceType(const.COMMON_STATUS), default=1)  # 状态:( 0 待激活；1 激活)
    module = Column(ChoiceType(const.COMPANY_MODULE))  # 业务：（审批；催收；管理；客服）
    created_at = Column(Integer, default=utime.timestamp(3))

    status_options = dict(const.COMMON_STATUS2)
    type_options = dict(const.COMPANY_TYPE)
    module_options = dict(const.COMPANY_MODULE)


class BlackList(BaseModel):
    """
    黑名单表
    """
    __tablename__ = 'sys_blacklist'
    id = Column(Integer, primary_key=True, nullable=False, default=None)
    admin_id = Column(Integer)  # 管理员id
    loan_order_id = Column(Integer)  # 贷款编号
    type = Column(Enum('ktp', 'mobile', 'full_name', 'company_name', 'company_phone'))  # 类型
    value = Column(String(100), nullable=True, default='')
    reason = Column(String(100), nullable=True, default='')
    status = Column(Integer, default=1)  # 0 禁用；1 启用, 默认1 删除 -1
    created_at = Column(Integer, default=utime.timestamp(3))

    status_options = {
        '1': '激活',
        '0': '待激活'
    }

    type_options = {
        'ktp': '身份证',
        'mobile': '手机号',
        'full_name': '姓名',
        'company_name': '公司名',
        'company_phone': '公司电话'
    }


class Tag(BaseModel):
    """
    标签表
    """
    __tablename__ = 'sys_tag'
    id = Column(Integer, primary_key=True, nullable=False, default=None)
    name = Column(String(50), nullable=True, default='')
    description = Column(String(100), nullable=True, default='')
    type = Column(ChoiceType(const.TAG_TYPE))  # 类型
    # 状态:( 0 禁用；1 启用, 默认1 删除 -1)
    status = Column(ChoiceType(const.COMMON_STATUS), default=1)
    created_at = Column(Integer, default=utime.timestamp(3))
    updated_at = Column(Integer, default=None)
