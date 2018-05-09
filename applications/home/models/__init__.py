#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import uuid
import json
import os

from applications.core.settings_manager import settings

from applications.core.logger.client import SysLogger
from applications.core.utils import Func
from applications.core.db.dbalchemy import BaseModel

from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.types import Text
from sqlalchemy.types import TIMESTAMP
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import PrimaryKeyConstraint

class MemberOperationLog(BaseModel):
    """
    user model
    """
    __tablename__ = 'sys_member_operation_log'

    uuid = Column(String(32), primary_key=True, nullable=False, default=Func.uuid32())
    user_id = Column(String(32), ForeignKey('sys_member.uuid'))
    # 用户账号： email or mobile or username
    account = Column(String(80), nullable=False)
    # 会员操作类型： email_reset_pwd mobile_reset_pwd username_reset_pwd activate_email
    action = Column(String(20), nullable=False)
    ip = Column(String(40), nullable=False)
    client = Column(String(20), nullable=True, default='web')
    utc_created_at = Column(TIMESTAMP, default=Func.utc_now)

    @property
    def created_at(self):
        return Func.dt_to_timezone(self.utc_created_at)

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

    uuid = Column(String(32), primary_key=True, nullable=False, default=Func.uuid32())
    user_id = Column(String(32), ForeignKey('sys_member.uuid'))
    ip = Column(String(40), nullable=False)
    client = Column(String(20), nullable=True, default='web')
    utc_created_at = Column(TIMESTAMP, default=Func.utc_now)

    @property
    def created_at(self):
        return Func.dt_to_timezone(self.utc_created_at)

class Member(BaseModel):
    """
    user model
    """
    __tablename__ = 'sys_member'

    uuid = Column(String(32), primary_key=True, nullable=False, default=Func.uuid32())
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
    utc_created_at = Column(TIMESTAMP, default=Func.utc_now)

    @property
    def last_login_at(self):
        return Func.dt_to_timezone(self.utc_last_login_at)

    @property
    def created_at(self):
        return Func.dt_to_timezone(self.utc_created_at)

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
        # 设置登录用户cookiex信息
        handler.set_curent_user(member)

        user_id = member.uuid
        login_count = member.login_count if member.login_count else 0
        params = {
            'login_count': login_count+1,
            'utc_last_login_at': Func.utc_now(),
            'last_login_ip': handler.request.remote_ip,
        }
        Member.Q.filter(Member.uuid==user_id).update(params)

        # 写登录日志
        params2 = {
            'uuid': Func.uuid32(),
            'user_id': user_id,
            'client': 'web',
            'ip': handler.request.remote_ip,
        }
        log = MemberLoginLog(**params2)
        MemberLoginLog.session.add(log)

        MemberLoginLog.session.commit()

    @staticmethod
    def remove_avator(user_id, mavatar):
        try:
            query = "SELECT `file_md5` FROM `sys_attach_related` WHERE `related_table`='sys_member' and `related_id`='%s';" % (user_id)
            old_file_md5 = Member.session.execute(query).scalar()
            if old_file_md5:
                pass
                delq = "DELETE FROM `sys_attach_related` WHERE `file_md5`='%s';"
                Member.session.execute(delq % old_file_md5)
                delq = "DELETE FROM `sys_attach` WHERE `file_md5`='%s';"
                Member.session.execute(delq % old_file_md5)
                old_avatar = settings.STATIC_PATH + '/' + mavatar
                os.remove(old_avatar)
        except Exception as e:
            raise e
        return True

