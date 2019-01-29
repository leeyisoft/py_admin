#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json

from applications.core.settings_manager import settings

from applications.core.models import BaseModel
from applications.core.models import Message
from applications.core.models import Sequence
from applications.core.logger.client import SysLogger

from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.types import Text
from sqlalchemy.types import TIMESTAMP
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import PrimaryKeyConstraint

from applications.core.utils import Func

from applications.home.models.content import Article
from applications.home.models.content import Team
from applications.home.models import Member
from applications.home.models import MemberCertification


class Role(BaseModel):
    """
    user model
    """
    __tablename__ = 'sys_admin_role'

    id = Column(Integer, primary_key=True, nullable=False, default=None)
    rolename = Column(String(40), nullable=False)
    permission = Column(Text, default='')
    sort = Column(Integer, nullable=False, default=20)
    # 状态:( 0 禁用；1 启用, 默认1)
    status = Column(Integer, nullable=False, default=1)
    utc_created_at = Column(TIMESTAMP, default=Func.utc_now)

    @property
    def created_at(self):
        return Func.dt_to_timezone(self.utc_created_at)

    @classmethod
    def option_html(cls, role_id=None):
        query = cls.session.query(Role)
        query = query.filter(Role.status == 1)
        rows = query.order_by(Role.sort.asc()).all()
        # SysLogger.debug(query.statement)
        option_str = ''
        for row in rows:
            selected = 'selected' if role_id==row.id else ''
            option_str += '<option value="%s" %s>%s</option>' % (row.id, selected, row.rolename)
        # SysLogger.debug('option_str: %s' % option_str)
        return option_str

    @classmethod
    def get_permission(cls, role_id):
        query = cls.session.query('permission')
        query = query.filter(Role.id == role_id)
        return query.scalar()


class User(BaseModel):
    """
    user model
    """
    __tablename__ = 'sys_admin_user'

    id = Column(Integer, primary_key=True, nullable=False, default=None)
    role_id = Column(Integer, ForeignKey('sys_admin_role.id'))
    password = Column(String(128), nullable=False, default='')
    username = Column(String(40), nullable=False)
    mobile = Column(String(11), nullable=True)
    email = Column(String(80), nullable=True)
    permission = Column(Text, default='')
    login_count = Column(Integer, nullable=False, default=0)
    last_login_ip = Column(String(128), nullable=False, default='')
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
    def role_permission(self):
        query = "select permission from sys_admin_role where id='%s'" % self.role_id
        permission = User.session.execute(query).scalar()
        try:
            return json.loads(permission)
        except Exception as e:
            pass
            # raise e
        return []

    @classmethod
    def get_permission(cls):
        try:
            return json.loads(cls.permission)
        except Exception as e:
            pass
            # raise e
        return []

    @staticmethod
    def login_success(user, handler):
        # 设置登录用户cookie信息
        handler.set_curent_user(user)

        user_id = user.id
        login_count = user.login_count if user.login_count else 0
        params = {
            'login_count': login_count + 1,
            'utc_last_login_at': Func.utc_now(),
            'last_login_ip': handler.request.remote_ip,
        }
        User.Q.filter(User.id==user_id).update(params)

        params = {
            'id': 0,
            'user_id': user.id,
            'client': 'web',
            'ip': handler.request.remote_ip,
        }
        log = UserLoginLog(**params)
        UserLoginLog.session.add(log)
        UserLoginLog.session.commit()
        return True


class UserLoginLog(BaseModel):
    """
    user model
    """
    __tablename__ = 'sys_admin_user_login_log'

    id = Column(Integer, primary_key=True, nullable=False, default=None)
    user_id = Column(Integer, ForeignKey('sys_admin_user.id'))
    ip = Column(String(40), nullable=False)
    client = Column(String(20), nullable=True)
    utc_created_at = Column(TIMESTAMP, default=Func.utc_now)

    @property
    def created_at(self):
        return Func.dt_to_timezone(self.utc_created_at)


class AdminMenu(BaseModel):
    """
    user group map model
    """
    __tablename__ = 'sys_admin_menu'

    id = Column(Integer, primary_key=True, nullable=False, default=None)
    user_id = Column(Integer, ForeignKey('sys_admin_user.id'), nullable=False, default='0')
    parent_id = Column(Integer, nullable=False, default=0)
    code = Column(String(64), nullable=True)
    title = Column(String(20), nullable=False)
    icon = Column(String(20), nullable=False)
    path = Column(String(200), nullable=False)
    param = Column(String(200), nullable=False)
    target = Column(String(20), nullable=False, default='_self')
    nav = Column(Integer, nullable=False)
    sort = Column(Integer, nullable=False, default=20)
    system = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    utc_created_at = Column(TIMESTAMP, default=Func.utc_now)

    @property
    def created_at(self):
        return Func.dt_to_timezone(self.utc_created_at)

    @classmethod
    def info(cls, id=None, path=None):
        """获取当前访问节点信息

        [description]

        Keyword Arguments:
            id {str} -- [description] (default: {''})

        Returns:
            [type] -- [description]
        """
        query = cls.session.query(AdminMenu)
        if id:
            query = query.filter(AdminMenu.id == id)
        if path:
            path = path.split('?')[0]
            if path[-1:]=='/':
                path = path[0:-1]
            if path[-5:]=='.html':
                path = path[0:-5]

            query = query.filter(AdminMenu.path == path)

        row = query.first()
        row = row.as_dict() if row else None
        # SysLogger.debug(query.statement)
        return row

    @classmethod
    def brand_crumbs(cls, id):
        """获取当前节点的面包屑

        [description]

        Arguments:
            id {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        menu = []
        row = cls.info(id=id)
        if row['parent_id']>0:
            menu.append(row)
            child = cls.brand_crumbs(row['parent_id'])
            if len(child):
                menu.extend(child)
        return menu


    @classmethod
    def main_menu(cls, parent_id=0, status=1, level=0):
        """获取后台主菜单(一级 > 二级 > 三级)
            后台顶部和左侧使用

            Keyword Arguments:
                parent_id {str} -- 父ID (default: {'0'})
                level {number} -- 层级数 (default: {0})
            Returns:
                [type] -- [description]
        """
        trees = []
        if not len(trees):
            filds = ['id', 'code', 'parent_id', 'title', 'path', 'param', 'target', 'icon']
            query = cls.session.query(AdminMenu)
            if status is not None:
                query = query.filter(AdminMenu.status == status)
            query = query.filter(AdminMenu.nav == 1)
            rows = query.order_by(AdminMenu.sort.asc()).all()
            # print('query.statement: ', query.statement)
            for row in rows:
                row = row.as_dict(filds)
                if row.get('parent_id')!=parent_id:
                    continue

                if level==5:
                    return trees

                # 过滤没访问权限的节点
                # if (!RoleModel::checkAuth($v['id'])) {
                #     unset($data[$k]);
                #     continue;
                # }
                row['children'] = cls.main_menu(row.get('id'), status, level+1)
                trees.append(row)
        return trees


    @staticmethod
    def children(parent_id=0, status=None, level=0, user_id=0):
        """获取指定节点下的所有子节点(不含快捷收藏的菜单)
        """
        trees = []
        if not len(trees):
            filds = ['id', 'code', 'parent_id', 'title', 'path', 'param', 'target', 'icon', 'sort', 'status']
            query = AdminMenu.session.query(AdminMenu)
            if user_id>0:
                query = query.filter(AdminMenu.user_id == user_id)
            query = query.filter(AdminMenu.parent_id == parent_id)
            if status in [1,0]:
                query = query.filter(AdminMenu.status == status)
            rows = query.order_by(AdminMenu.sort.asc()).all()
            data = []
            for row in rows:
                if level==5:
                    return trees
                row = row.as_dict(filds)

                # 过滤没访问权限的节点
                # if (!RoleModel::checkAuth($v['id'])) {
                #     unset($data[$k]);
                #     continue;
                # }
                row['children'] = AdminMenu.children(row.get('id'), status, level+1)
                trees.append(row)
        return trees

    @staticmethod
    def menu_option(id=''):
        """菜单选项"""
        menus = AdminMenu.main_menu(status=None)
        if not len(menus)>0:
            return ''
        option1 = '<option level="1" value="%s" %s>— %s</option>'
        option2 = '<option level="2" value="%s" %s>—— %s</option>'
        option3 = '<option level="3" value="%s" %s>——— %s</option>'
        html = ''
        for menu in menus:
            selected = 'selected' if id==menu.get('id', '') else ''
            title1 = menu.get('title', '')
            children1 = menu.get('children', [])
            html += option1 % (menu.get('id', ''), selected, title1)
            if not len(children1)>0:
                continue
            for menu2 in children1:
                selected2 = 'selected' if id==menu2.get('id', '') else ''
                title2 = menu2.get('title', '')
                children2 = menu2.get('children', [])
                html += option2 % (menu2.get('id', ''), selected2, title2)
                if not len(children2)>0:
                    continue
                for menu3 in children2:
                    selected3 = 'selected' if id==menu3.get('id', '') else ''
                    title3 = menu3.get('title', '')
                    html += option3 % (menu3.get('id', ''), selected3, title3)
        return html
