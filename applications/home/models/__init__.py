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
    __tablename__ = 'member_operation_log'

    uuid = Column(String(32), primary_key=True, nullable=False, default=Func.uuid32())
    user_id = Column(String(32), ForeignKey('member.uuid'))
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
    __tablename__ = 'member_login_log'

    uuid = Column(String(32), primary_key=True, nullable=False, default=Func.uuid32())
    user_id = Column(String(32), ForeignKey('member.uuid'))
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
    __tablename__ = 'member'

    uuid = Column(String(32), primary_key=True, nullable=False, default=Func.uuid32())
    password = Column(String(128), nullable=False, default='')
    username = Column(String(40), nullable=False)
    mobile = Column(String(11), nullable=True)
    email = Column(String(80), nullable=True)
    level_id = Column(Integer, nullable=False, default=0)
    # 经验值
    experience = Column(Integer, nullable=False, default=0)
    # 性别(男 male ，女 female 隐藏 hide)
    sex = Column(String(10), nullable=False, default='hide')
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
        query = "select count(*) from member_operation_log where user_id='%s' and account='%s' and action='activate_email'" % (user_id, email)
        # print("query: ", query)
        value = Member.session.execute(query).scalar()
        return True if value>0 else False

    @staticmethod
    def _friend_list(user_id, where=''):
        query = "select m.uuid as user_id,m.username,m.avatar,m.sign,f.group_id from member m left join member_friend f on m.uuid=f.to_user_id where f.from_user_id='%s' and m.status=1 and f.status=1 %s" % (user_id, where)
        rows = Member.session.execute(query).fetchall()
        items = []
        if rows:
            for row in rows:
                items.append(dict(row))
        return items

    @staticmethod
    def friends_no_grouping(user_id):
        where = " and f.group_id='0'"
        return Member._friend_list(user_id, where)

    @staticmethod
    def friends_by_group(user_id, static_url):
        """
        按分组获取好友
        """
        _friend_list = Member._friend_list(user_id)
        # print('_friend_list: ', _friend_list)
        query = "select uuid, groupname from member_friendgroup where owner_user_id='%s'" % user_id
        grows = Member.session.execute(query).fetchall()
        grows = grows if grows else []
        # print("grows: ", type(grows), grows)
        f_g_li = []
        try:
            if len(grows)>0:
                f_g_li += [{
                    'id': group_id,
                    'groupname': groupname,
                    'list':[{
                        'id':fnd.get('user_id'),
                        'username':fnd.get('username'),
                        'status': Online.get_online(fnd.get('user_id')),
                        'sign':fnd.get('sign'),
                        'avatar':fnd.get('avatar')
                    } for fnd in _friend_list if fnd.get('group_id')==group_id
                ]} for (group_id, groupname) in grows]

            # Member.friends_no_grouping(user_id)
            f_g_li += [{'id': '0', 'groupname': '未分组', 'list':[{
                'id':fnd.get('user_id'),
                'username':fnd.get('username'),
                'status': Online.get_online(fnd.get('user_id')),
                'sign':fnd.get('sign'),
                'avatar':static_url(fnd.get('avatar'))
            } for fnd in Member.friends_no_grouping(user_id)]}]
        except Exception as e:
            raise e

        return f_g_li

    @staticmethod
    def login_success(member, handler, client='web'):
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
            'client': client,
            'ip': handler.request.remote_ip,
        }
        log = MemberLoginLog(**params2)
        MemberLoginLog.session.add(log)

        MemberLoginLog.session.commit()

    @staticmethod
    def remove_avator(user_id, mavatar):
        try:
            query = "SELECT `file_md5` FROM `sys_attach_related` WHERE `related_table`='member' and `related_id`='%s';" % (user_id)
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



class MemberFriend(BaseModel):
    """
    user model
    """
    __tablename__ = 'member_friend'

    uuid = Column(String(32), primary_key=True, nullable=False, default=Func.uuid32())
    user_id = Column(String(32), ForeignKey('member.uuid'))
    ip = Column(String(40), nullable=False)
    client = Column(String(20), nullable=True, default='web')
    utc_created_at = Column(TIMESTAMP, default=Func.utc_now)

    @property
    def created_at(self):
        return Func.dt_to_timezone(self.utc_created_at)

class Online:
    cache_key = 'member_online:%s'

    @classmethod
    def get_online(cls, user_id):
        """
        获取用户在线状态
        """
        # state = redis_conn.get(cls.cache_key % (str(user_id),))
        # return state.decode() if state else 'offline'
        return 'online'

    @classmethod
    def set_online(cls, user_id, state):
        """
        设置用户在线状态
        state : [hide|online|offline]
        """
        # return redis_conn.set(cls.cache_key % (str(user_id),), state)
        return True