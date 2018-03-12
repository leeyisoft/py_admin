#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import uuid

from applications.core.db.dbalchemy import Model
from applications.core.utils import datetimezone
from applications.core.logger.client import SysLogger

from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.types import Text
from sqlalchemy.types import TIMESTAMP
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import PrimaryKeyConstraint

from .utils import utc_to_timezone

class BaseModel(Model):
    __abstract__ = True
    __connection_name__ = 'default'


class Config(BaseModel):
    """
    sys_config model
    """
    __tablename__ = 'sys_config'

    key = Column(String(40), primary_key=True, nullable=False)
    value = Column(String(80), nullable=False)
    remark = Column(String(128), nullable=False)
    # 状态:(0 无效, 1正常, 默认1)
    status = Column(Integer, nullable=False, default=1)
    created_at = Column(TIMESTAMP, default=datetimezone)

class User(BaseModel):
    """
    user model
    """
    __tablename__ = 'users'

    uuid = Column(String(36), primary_key=True, nullable=False, default=uuid.uuid4())
    password = Column(String(128), nullable=False, default='')
    username = Column(String(40), nullable=False)
    mobile = Column(String(11), nullable=True)
    email = Column(String(80), nullable=True)
    # 用户状态:(0 锁定, 1正常, 默认1)
    status = Column(Integer, nullable=False, default=1)
    last_login_at = Column(TIMESTAMP, default=datetimezone)
    # 已删除的 1 是 0 否 默认 0
    deleted = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, default=datetimezone)

    @property
    def group_id(self):
        query = "select group_id from user_group_map where user_id='%s'" % self.uuid
        group_id = User.session.execute(query).scalar()
        # print('group_id', type(group_id), group_id)
        return group_id

class UserGroup(BaseModel):
    """
    user model
    """
    __tablename__ = 'user_groups'

    uuid = Column(String(36), primary_key=True, nullable=False, default=uuid.uuid4())
    groupname = Column(String(40), nullable=False)
    permission = Column(Text, default='')
    # 状态:( 0 禁用；1 启用, 默认1)
    status = Column(Integer, nullable=False, default=1)
    # 已删除的 1 是 0 否 默认 0
    deleted = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, default=datetimezone)

class UserGroupMap(BaseModel):
    """
    user group map model
    """
    __tablename__ = 'user_group_map'

    group_id = Column(String(36), ForeignKey('user_groups.uuid'))
    user_id = Column(String(36), primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP, default=datetimezone)

