#!/usr/bin/env python
# -*- coding: utf-8  -*-
import datetime

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
            if isinstance(val, datetime.datetime):
                if settings.DB_DATETIME_IS_UTC:
                    val = Func.dt_to_timezone(val)
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
    value = Column(String(80), nullable=False)
    title = Column(String(40), nullable=False)
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

    file_md5 = Column(String(32), primary_key=True, nullable=False, default=Func.uuid32())
    file_ext = Column(String(20), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_mimetype = Column(String(40), nullable=False)
    origin_name = Column(String(80), nullable=False)
    path_file = Column(String(200), nullable=False)
    user_id = Column(String(32), ForeignKey('member.uuid'))
    ip = Column(String(40), nullable=False)
    utc_created_at = Column(TIMESTAMP, default=Func.utc_now)

    @property
    def created_at(self):
        return Func.dt_to_timezone(self.utc_created_at)
