#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from ast import literal_eval

from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.types import Text
from sqlalchemy import Column, Enum
from sqlalchemy import ForeignKey

from trest.utils import utime
from applications.common.utils import mysqldb
from trest.db import Model as BaseModel
from applications.common import const


class Role(BaseModel):
    """
    系统管理员角色表
    """
    __tablename__ = 'sys_admin_role'

    id = Column(Integer, primary_key=True, nullable=False, default=None)
    rolename = Column(String(40), nullable=False)
    description = Column(String(100), nullable=False, default='')
    permission = Column(Text, default='')
    sort = Column(Integer, nullable=False, default=20)
    status = Column(Integer, nullable=False, default=1)  # 状态:( 0 禁用；1 启用, 默认1)
    category = Column(Integer, nullable=False, default=0)
    company_id = Column(Integer, nullable=False, default=1)
    created_at = Column(Integer, default=utime.timestamp(3))

    @classmethod
    def option_html(cls, role_id=None):
        query   = cls.session.query(Role)
        query   = query.filter(Role.status == 1)
        rows    = query.order_by(Role.sort.asc()).all()
        option_str = ''
        for row in rows:
            selected = 'selected' if role_id==row.id else ''
            option_str += '<option value="%s" %s>%s</option>' % (row.id, selected, row.rolename)
        return option_str

    status_options = {
        '1': '激活',
        '0': '待激活'
    }


class AdminUser(BaseModel):
    """
    系统管理员表
    """
    __tablename__ = 'sys_admin_user'

    id = Column(Integer, primary_key=True, nullable=False, default=None)
    role_id       = Column(Integer, ForeignKey('sys_admin_role.id'))
    password      = Column(String(128), nullable=False, default='')
    username      = Column(String(40), nullable=False)
    mobile        = Column(String(11), nullable=True)
    email         = Column(String(80), nullable=True)
    permission    = Column(Text, default='')
    login_count   = Column(Integer, nullable=False, default=0)
    last_login_ip = Column(String(128), nullable=False, default='')
    status        = Column(Integer, nullable=False, default=1)  # 用户状态:(0 锁定, 1正常, 默认1)
    last_login_at = Column(Integer, nullable=True)
    created_at    = Column(Integer, default=utime.timestamp(3))
    lang          = Column(String(2), nullable=False, default='')  # 默认语言

    @property
    def role_permission(self):
        query = "select permission from sys_admin_role where id='%s'" % self.role_id
        permission = AdminUser.session.execute(query).scalar()
        try:
            p2 = json.loads(permission) if permission else []
            return p2 if type(p2)==list else literal_eval(p2)
        except Exception as e:
            pass
            # raise e
        return []

    @property
    def user_permission(self):
        try:
            p2 = json.loads(self.permission)
            return p2 if type(p2)==list else literal_eval(p2)
        except Exception as e:
            pass
            # raise e
        return []


class AdminUserLoginLog(BaseModel):
    """
    系统管理员登录日志表
    """
    __tablename__ = 'sys_admin_user_login_log'

    id          = Column(Integer, primary_key=True, nullable=False, default=None)
    user_id     = Column(Integer, ForeignKey('sys_admin_user.id'))
    ip          = Column(String(40), nullable=False)
    client      = Column(String(20), nullable=True)
    created_at  = Column(Integer, default=utime.timestamp(3))


class AdminMenu(BaseModel):
    """
    后台菜单表
    """
    __tablename__ = 'sys_admin_menu'

    id          = Column(Integer, primary_key=True, nullable=False, default=None)
    user_id     = Column(Integer, ForeignKey('sys_admin_user.id'), nullable=False, default='0')
    parent_id   = Column(Integer, nullable=False, default=0)
    code        = Column(String(64), nullable=True)
    title       = Column(String(20), nullable=False)
    icon        = Column(String(20), nullable=False)
    path        = Column(String(200), nullable=False)
    param       = Column(String(200), nullable=False)
    target      = Column(String(20), nullable=False, default='_self')
    nav         = Column(Integer, nullable=False)
    sort        = Column(Integer, nullable=False, default=20)
    system      = Column(Integer, nullable=False)
    status      = Column(Integer, nullable=False)
    created_at  = Column(Integer, default=utime.timestamp(3))
