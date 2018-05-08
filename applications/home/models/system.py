#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import uuid
import json

from applications.core.settings_manager import settings

from applications.core.db.dbalchemy import Model
from applications.core.utils import utc_now
from applications.core.logger.client import SysLogger

from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.types import Text
from sqlalchemy.types import TIMESTAMP
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import PrimaryKeyConstraint

from applications.core.utils import dt_to_timezone
from applications.core.utils import utc_now
from applications.core.utils import uuid32

class BaseModel(Model):
    __abstract__ = True
    __connection_name__ = 'default'

class MemberOperationLog(BaseModel):
    """
    user model
    """
    __tablename__ = 'sys_member_operation_log'

    uuid = Column(String(32), primary_key=True, nullable=False, default=uuid32())
    user_id = Column(String(32), ForeignKey('sys_member.uuid'))
    # 用户账号： email or mobile or username
    account = Column(String(80), nullable=False)
    # 会员操作类型： email_reset_pwd mobile_reset_pwd username_reset_pwd activate_email
    action = Column(String(20), nullable=False)
    ip = Column(String(40), nullable=False)
    client = Column(String(20), nullable=True, default='web')
    utc_created_at = Column(TIMESTAMP, default=utc_now)

    @property
    def created_at(self):
        return dt_to_timezone(self.utc_created_at)

    @staticmethod
    def add_log(params):
        """激活邮件

        [description]

        Arguments:
            params {[type]} -- [description]
        """
        log = MemberOperationLog(**params)
        MemberOperationLog.session.add(log)
        MemberOperationLog.session.commit()

class MemberLoginLog(BaseModel):
    """
    user model
    """
    __tablename__ = 'sys_member_login_log'

    uuid = Column(String(32), primary_key=True, nullable=False, default=uuid32())
    user_id = Column(String(32), ForeignKey('sys_member.uuid'))
    ip = Column(String(40), nullable=False)
    client = Column(String(20), nullable=True, default='web')
    utc_created_at = Column(TIMESTAMP, default=utc_now)

    @property
    def created_at(self):
        return dt_to_timezone(self.utc_created_at)

class Member(BaseModel):
    """
    user model
    """
    __tablename__ = 'sys_member'

    uuid = Column(String(32), primary_key=True, nullable=False, default=uuid32())
    password = Column(String(128), nullable=False, default='')
    username = Column(String(40), nullable=False)
    mobile = Column(String(11), nullable=True)
    email = Column(String(80), nullable=True)
    level_id = Column(Integer, nullable=False, default=0)
    exper = Column(Integer, nullable=False, default=0)
    integral = Column(Integer, nullable=False, default=0)
    frozen_integral = Column(Integer, nullable=False, default=0)
    # 性别 man woman hide
    sex = Column(String(10), nullable=False, default='HIDE')
    # 头像
    avatar = Column(String(255), nullable=True, default='')
    # 签名
    sign = Column(String(255), nullable=True, default='')
    login_count = Column(Integer, nullable=False, default=0)
    last_login_ip = Column(String(128), nullable=False, default='')
    deleted = Column(Integer, nullable=False, default=0)
    # 用户状态:(0 锁定, 1正常, 默认1)
    status = Column(Integer, nullable=False, default=1)
    utc_last_login_at = Column(TIMESTAMP, nullable=True)
    utc_created_at = Column(TIMESTAMP, default=utc_now)

    @property
    def last_login_at(self):
        return dt_to_timezone(self.utc_last_login_at)

    @property
    def created_at(self):
        return dt_to_timezone(self.utc_created_at)

    @property
    def email_activated(self):
        return self.check_email_activated(self.uuid, self.email)

    @staticmethod
    def check_email_activated(user_id, email):
        query = "select count(*) from sys_member_operation_log where user_id='%s' and account='%s' and action='activate_email'" % (user_id, email)
        # print("query: ", query)
        value = Member.session.execute(query).scalar()
        return True if value>0 else False

    @staticmethod
    def login_success(member, handler):
        user_fileds = ['uuid', 'username']
        user_str = str(member.as_dict(user_fileds))
        handler.set_secure_cookie(handler.user_session_key, user_str, expires_days=1)

        user_id = member.uuid
        params = {
            'login_count': member.login_count+1,
            'utc_last_login_at': utc_now(),
            'last_login_ip': handler.request.remote_ip,
        }
        Member.Q.filter(Member.uuid==user_id).update(params)

        # 写登录日志
        params2 = {
            'user_id': user_id,
            'client': 'web',
            'ip': handler.request.remote_ip,
        }
        log = MemberLoginLog(**params2)
        MemberLoginLog.session.add(log)

        MemberLoginLog.session.commit()
