#!/usr/bin/env python
# -*- coding: utf-8  -*-
import os
import time
import datetime
from decimal import Decimal

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.types import Integer
from sqlalchemy.types import String,TEXT
from sqlalchemy.types import VARCHAR
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

from applications.core.db.dbalchemy import Connector
from applications.core.utils import utime
from applications.core.settings_manager import settings
from applications.core.db.dbalchemy import Query

MetaBaseModel = declarative_base()


class BaseModel(MetaBaseModel):
    __abstract__ = True
    __tablename__ = ''
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    __connection_name__ = 'default'

    @declared_attr
    def Q(cls) -> Query:
        return Connector.get_conn(cls.__connection_name__).query()

    @declared_attr
    def session(cls):
        slave = Connector.get_session(cls.__connection_name__)['slave']

        slave.using_master = lambda: \
            Connector.get_session(cls.__connection_name__)['master']
        return slave


    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def as_dict(self, filds=[]):
        items = {}
        for column in self.__table__.columns:
            val = getattr(self, column.name)
            val = '' if val is None else val
            if column.name.endswith('_at'):
                items['dt_%s'%column.name] = utime.ts_to_str(int(val), to_tz=None) if val else ''
            datetime_tuple = (datetime.datetime, datetime.date)
            if isinstance(val, datetime_tuple):
                val = str(val)
            elif isinstance(val, Decimal):
                val = str(val)
            if type(filds)==list and len(filds)>0:
                if column.name in filds:
                    items[column.name] = val
            else :
                items[column.name] = val
        return items


class Config(BaseModel):
    """
    sys_config model
    """
    __tablename__ = 'sys_config'

    key = Column(String(40), primary_key=True, nullable=False)
    value = Column(String(400), nullable=False)
    title = Column(String(40), nullable=False)
    subtitle = Column(String(160), nullable=False)
    remark = Column(String(128), nullable=False, default='')
    sort = Column(Integer, nullable=False, default=20)
    system = Column(Integer, nullable=False, default=0)
    # 状态:( 0 禁用；1 启用, 默认1)
    status = Column(Integer, nullable=False, default=1)
    created_at = Column(TIMESTAMP, default=utime.timestamp)


class Message(BaseModel):
    """
    sys_message model
    """
    __tablename__ = 'sys_message'

    id = Column(Integer, primary_key=True, nullable=False, default=None)
    # 消息类型 'apply_friend','accept_friend','system'
    msgtype = Column(String(40), nullable=False)
    # related_id = Column(Integer, nullable=False, default=0)
    message = Column(String(200), nullable=False, default=0)
    # Member 用户ID 消息发送者 0表示为系统消息
    from_user_id = Column(Integer, ForeignKey('user.id'), nullable=False, default=0)
    # 消息接收者 Member 用户ID
    to_user_id = Column(Integer, ForeignKey('user.id'), nullable=False, default=0)

    read_at = Column(TIMESTAMP, nullable=True)
    # 状态:( 0 未读；1 已读, 默认0)
    status = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, default=utime.timestamp)

class ApiVsn(BaseModel):
    """
    sys_message model
    """
    __tablename__ = 'sys_api_vsn'

    id = Column(Integer, primary_key=True, nullable=False, default=None)
    # 当前版本格式如 X.Y.Z
    master_vsn = Column(String(8), nullable=False)
    # 子版本号 ['X.Y.Z', 'X.Y.Z1']
    sub_vsn = Column(String(400), nullable=False)
    # 服务器公钥
    pubkeyser = Column(String(400), nullable=False, default='')
    # 服务器私钥
    prikeyser = Column(String(1200), nullable=False, default='')
    remark = Column(String(400), nullable=False, default='')
    # 状态:( 0 未读；1 已读, 默认0)
    status = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, default=utime.timestamp)

class ClientVsn(BaseModel):
    """
    sys_message model
    """
    __tablename__ = 'sys_client_vsn'

    id = Column(Integer, primary_key=True, nullable=False, default=None)
    client = Column(String(20), nullable=False)
    # 当前版本格式如 X.Y.Z
    vsn = Column(String(8), nullable=False)
    # 签名key
    signkey = Column(String(32), nullable=False, default='')
    # 客服端公钥
    pubkeycli = Column(String(400), nullable=False, default='')
    remark = Column(String(400), nullable=False, default='')
    # 状态:( 0 未读；1 已读, 默认0)
    status = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, default=utime.timestamp)
    apk_url = Column(VARCHAR(255), nullable=False, default='')


class Advertising(BaseModel):
    """
        advertising 广告列表
    """
    __tablename__ = 'sys_advertising'

    id          = Column(Integer, primary_key=True, nullable=False)
    #客户端语言：cn 简体中文 en 英语 id 印尼语 ph 菲律宾语
    lang        =Column(String(10),nullable=True,default='en')
    title       = Column(String(50), nullable=False)            # 标题
    start_at    = Column(Integer, nullable=False, default=0)    # 投放开始时间
    end_at      = Column(Integer, nullable=False, default=-1)   # 投放结束时间
    created_at   = Column(Integer, nullable=False, default=utime.timestamp)    # 创建时间
    type        = Column(Integer, nullable=False, default=1)    # 广告类型 1.链接 2.外链
    client      = Column(String(20), nullable=False)            # 投放的客户端
    img         = Column(String(255), nullable=False)           # 图片链接
    link        = Column(String(255), nullable=False)           # 跳转链接
    effects     = Column(String(20), nullable=False)            # 特效
    category    = Column(Integer, nullable=False)               # 分类id
    status      = Column(Integer,nullable=False,default=1)


class AdvertisingCategory(BaseModel):
    """
        advertising_category 广告分类
    """
    __tablename__ = 'sys_advertising_category'

    id     = Column(Integer, primary_key=True, nullable=False)
    #客户端语言：cn 简体中文 en 英语 id 印尼语 ph 菲律宾语
    lang   =Column(String(10),nullable=True,default='en')
    name   = Column(String(50), nullable=False)
    status = Column(Integer, default=1)


class AdvertisingLog(BaseModel):
    """
        advertising_log 广告记录
    """
    __tablename__ = 'sys_advertising_log'

    id          = Column(Integer, primary_key=True, nullable=False)
    ad_id       = Column(Integer, nullable=False)
    uid         = Column(Integer, nullable=False)
    created_at   = Column(Integer, default=1)
    ip          = Column(String(20),nullable=True)



class Notice(BaseModel):
    """
    sys_notice
    """
    __tablename__ = 'sys_notice'
    id= Column(Integer, primary_key=True, nullable=False)
    title=Column(String(30),nullable=False)
    content=Column(TEXT,nullable=False)
    sort=Column(Integer)
    status=Column(Integer,default=1)
    created_at=Column(Integer,default=utime.timestamp)
    updated_at=Column(Integer,default=utime.timestamp)
    operate_id=Column(Integer,nullable=False)
    lang=Column(String(30),default='cn')


class Contract(BaseModel):
    """
    sys_contract
    """
    __tablename__ ='sys_contract'
    id= Column(Integer, primary_key=True, nullable=False)
    name=Column(String(30),nullable=False)
    content=Column(TEXT,nullable=False)
    type=Column(Integer,default=1)#类型（1contract，2agreement，3privacy，4account_fee）
    status=Column(Integer,default=1)
    created_at=Column(Integer,default=utime.timestamp)
    updated_at=Column(Integer,default=utime.timestamp)
    operate_id=Column(Integer,nullable=False)
    lang=Column(String(30),default='cn')

class Bank(BaseModel):
    """
    支持银行
    """
    __tablename__ = 'sys_bank'
    id = Column(Integer, primary_key=True, nullable=False, default=None)
    region = Column(String(2), nullable=False, default='')  # 区域码
    bank = Column(String(25), nullable=False ,default='')  # 银行标识符
    bank_name = Column(String(40), nullable=False, default='')  # 银行名称
    bank_logo = Column(String(100), nullable=False, default='')  # 银行logo
    created_at = Column(Integer, default=utime.timestamp)  # 创建时间
    status = Column(Integer, default=1)  # 状态:( 0 禁用；1 启用； 删除 -1)
