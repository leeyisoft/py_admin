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
from sqlalchemy.types import String
from sqlalchemy.types import Text
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

from ..db.dbalchemy import Connector
from ..utils import Func
from ..settings_manager import settings


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
    def Q(cls):
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
            datetime_tuple = (datetime.datetime, datetime.date)
            if isinstance(val, datetime_tuple):
                tz = 'UTC' if column.name[0:4]=='utc_' else None
                val = Func.dt_to_timezone(val, tz)
                val = str(val)
            elif isinstance(val, Decimal):
                val = str(val)
            if type(filds)==list and len(filds)>0:
                if column.name in filds:
                    items[column.name] = val
            else :
                items[column.name] = val
        return items


class Sequence(BaseModel):
    """
    sys_config model
    """
    __tablename__ = 'sys_sequence'

    key = Column(String(40), primary_key=True, nullable=False)
    value = Column(Integer, nullable=False)

    @staticmethod
    def insert(key='increment', value=0):
        seq = Sequence(key=key, value=value)
        Sequence.session.merge(seq)
        Sequence.session.commit()
        return True

    @staticmethod
    def currval(name='increment'):
        query = "select currval('%s') " % name
        # print("query: ", query)
        return Sequence.session.execute(query).scalar()

    @staticmethod
    def nextval(name='increment', increment=1):
        query = "select nextval('%s', %d);" % (name, increment)
        val = Sequence.session.execute(query).scalar()
        Sequence.session.commit()
        if val==0:
            val = increment
            Sequence.insert(name, increment)
        return val

    @staticmethod
    def order_no(prefix='NO'):
        """生成格式化的订单号"""
        con = time.strftime("%y%m%d", time.localtime())
        name = '%s%s' % (prefix, con)
        sequ_num = Sequence.nextval(name=name)
        return '%s%s%04d' %(prefix, con, sequ_num)


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
    utc_created_at = Column(TIMESTAMP, default=Func.utc_now)

    @property
    def created_at(self):
        return Func.dt_to_timezone(self.utc_created_at)


class Attach(BaseModel):
    """
    user model
    """
    __tablename__ = 'sys_attach'

    file_md5 = Column(String(32), primary_key=True, nullable=False, default='')
    file_ext = Column(String(20), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_mimetype = Column(String(40), nullable=False)
    origin_name = Column(String(80), nullable=False)
    path_file = Column(String(200), nullable=False)
    user_id = Column(Integer, ForeignKey('member.id'))
    ip = Column(String(40), nullable=False)
    utc_created_at = Column(TIMESTAMP, default=Func.utc_now)

    @property
    def created_at(self):
        return Func.dt_to_timezone(self.utc_created_at)

    @staticmethod
    def remove(file_md5, path_file='', table=''):
        query = "SELECT count(*) FROM `sys_attach_related` WHERE `file_md5`='%s';" % (file_md5)
        count = Attach.session.execute(query).scalar()
        try:
            if not(count>1):
                delq = "DELETE FROM `sys_attach_related` WHERE `file_md5`='%s';"
                Attach.session.execute(delq % (file_md5))

                delq = "DELETE FROM `sys_attach` WHERE `file_md5`='%s';"
                Attach.session.execute(delq % file_md5)

                path_file2 = settings.STATIC_PATH + '/' + path_file
                if os.path.isfile(path_file2):
                    os.remove(path_file2)
            else:
                delq = "DELETE FROM `sys_attach_related` WHERE `file_md5`='%s' AND `related_table`='%s';"
                Attach.session.execute(delq % (file_md5, table))
        except Exception as e:
            raise e
        return True

    @staticmethod
    def remove_avatar(user_id, mavatar):
        try:
            query = "SELECT `file_md5` FROM `sys_attach_related` WHERE `related_table`='member' and `related_id`='%s';" % (user_id)
            file_md5 = Attach.session.execute(query).scalar()
            if file_md5:
                Attach.remove(file_md5, mavatar, 'member')
        except Exception as e:
            raise e
        return True


class Message(BaseModel):
    """
    sys_message model
    """
    __tablename__ = 'sys_message'

    id = Column(Integer, primary_key=True, nullable=False, default=None)
    # 消息类型 'apply_friend','accept_friend','system'
    msgtype = Column(String(40), nullable=False)
    related_id = Column(Integer, nullable=False, default=0)
    message = Column(String(200), nullable=False, default=0)
    # Member 用户ID 消息发送者 0表示为系统消息
    from_user_id = Column(Integer, ForeignKey('member.id'), nullable=False, default=0)
    # 消息接收者 Member 用户ID
    to_user_id = Column(Integer, ForeignKey('member.id'), nullable=False, default=0)

    utc_read_at = Column(TIMESTAMP, nullable=True)
    # 状态:( 0 未读；1 已读, 默认0)
    status = Column(Integer, nullable=False, default=0)
    utc_created_at = Column(TIMESTAMP, default=Func.utc_now)

    @property
    def read_at(self):
        return Func.dt_to_timezone(self.utc_read_at)

    @property
    def created_at(self):
        return Func.dt_to_timezone(self.utc_created_at)

