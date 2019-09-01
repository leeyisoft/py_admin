#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from ast import literal_eval

from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.types import Text
from sqlalchemy.types import Enum
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy_utils import ChoiceType
from trest.settings_manager import settings
from trest.utils import utime
from trest.db import Model as BaseModel

from applications.common import const


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


class MessageTemplate(BaseModel):
    """
    消息模板表
    """
    __tablename__ = 'sys_message_template'
    id = Column(Integer, primary_key=True, nullable=False, default=None)
    category = Column(String(20))  # 模板类型
    content = Column(String(400))  # 内容
    # 状态:( 0 禁用；1 启用, 默认1 删除 -1)
    status = Column(ChoiceType(const.COMMON_STATUS), default=1)
    updated_at = Column(Integer, default=None)
    created_at = Column(Integer, default=utime.timestamp(3))


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

    type_options = dict(const.TAG_TYPE)


class BankChannel(BaseModel):
    """
    银行渠道表
    """
    __tablename__ = 'sys_bank_channel'
    id = Column(Integer, primary_key=True, nullable=False, default=None)
    bank_code = Column(String(50), nullable=True, default='')
    bank_name = Column(String(50), nullable=True, default='')
    channel = Column(String(50), nullable=True, default='')
    type = Column(ChoiceType(const.BANK_TYPE))
    score = Column(Integer, default=0)
    # 状态:( 0 禁用；1 启用, 默认1)
    status = Column(ChoiceType(const.COMMON_STATUS), default=1)
    is_bank = Column(Integer, default=1)


class Page(BaseModel):
    """
    详情页面配置表
    """
    __tablename__ = 'sys_page'
    id = Column(Integer, primary_key=True, nullable=False, default=None)
    type = Column(ChoiceType(const.PAGE_TYPE), nullable=True, default='')
    tab = Column(ChoiceType(const.PAGE_TAB), nullable=True, default='')
    module = Column(Text)
    sort = Column(Integer, default=0)
    # 状态:( 0 禁用；1 启用, 默认1)
    status = Column(ChoiceType(const.COMMON_STATUS), default=1)

    type_options = dict(const.PAGE_TYPE)
    tab_options = dict(const.PAGE_TAB)
