#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""

import json
import tornado

from applications.core.settings_manager import settings
from applications.core.logger.client import SysLogger
from applications.core.cache import sys_config
from applications.core.decorators import required_permissions

from applications.admin.models.system import Role
from applications.admin.models.system import AdminMenu

from .common import CommonHandler


class RoleHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    @required_permissions('admin:role:index')
    def get(self, *args, **kwargs):
        params = {
        }
        self.render('role/index.html', **params)

    @tornado.web.authenticated
    @required_permissions('admin:role:delete')
    def delete(self, *args, **kwargs):
        """删除角色
        """
        uuid = self.get_argument('uuid', None)

        # 超级管理员角色 默认角色
        user_role_li = [settings.SUPER_ROLE_ID,'6b0642103a1749949a07f4139574ead9']
        if uuid in user_role_li:
            return self.error('角色不允许删除')

        Role.Q.filter(Role.uuid==uuid).delete()
        Role.session.commit()
        return self.success()

class RoleListHandler(CommonHandler):
    """用户组列表"""
    @tornado.web.authenticated
    @required_permissions('admin:role:index')
    def get(self, *args, **kwargs):
        limit = self.get_argument('limit', 10)
        page = self.get_argument('page', 1)
        pagelist_obj = Role.Q.filter().paginate(page=page, per_page=limit)
        if pagelist_obj is None:
            return self.error('暂无数据')

        total = pagelist_obj.total
        page = pagelist_obj.page
        items = pagelist_obj.items

        params = {
            'count': total,
            'uri': self.request.uri,
            'path': self.request.path,
            'data': [role.as_dict() for role in items],
        }
        return self.success(**params)

class RoleAddHandler(CommonHandler):
    """用户组添加功能"""

    @tornado.web.authenticated
    @required_permissions('admin:role:add')
    def post(self, *args, **kwargs):
        rolename = self.get_argument('rolename', None)
        uuid = self.get_argument('uuid', None)
        status = self.get_argument('status', 1)
        if not rolename:
            return self.error('分组名称不能为空')

        res = Role.Q.filter(Role.rolename==rolename).count()
        if res>0:
            return self.error('名称已被占用')

        role = {
            'rolename':rolename,
            'status': status,
        }
        role = Role(**role)
        Role.session.add(role)
        Role.session.commit()
        return self.success()

class RoleEditHandler(CommonHandler):
    """用户组增删查改功能"""
    @tornado.web.authenticated
    @required_permissions('admin:role:edit')
    def get(self, *args, **kwargs):
        uuid = self.get_argument('uuid', None)
        role = Role.Q.filter(Role.uuid==uuid).first()

        menu_list = AdminMenu.children(status=1)

        data_info = role.as_dict()
        try:
            data_info['permission'] = json.loads(role.permission)
        except Exception as e:
            data_info['permission'] = []
        params = {
            'role': role,
            'menu_list': menu_list,
            'data_info': data_info,
        }
        self.render('role/edit.html', **params)


    @tornado.web.authenticated
    @required_permissions('admin:role:edit')
    def post(self, *args, **kwargs):
        rolename = self.get_argument('rolename', None)
        uuid = self.get_argument('uuid', None)
        sort = self.get_argument('sort', None)
        status = self.get_argument('status', 0)
        permission = self.get_body_arguments('permission[]')

        role = {
            'status': status,
        }

        if rolename:
            role['rolename'] = rolename
            res = Role.Q.filter(Role.uuid!=uuid).filter(Role.rolename==rolename).count()
            if res>0:
                return self.error('名称已被占用')

        if sort:
            role['sort'] = sort

        if permission:
            role['permission'] = json.dumps(permission)

        Role.Q.filter(Role.uuid==uuid).update(role)
        Role.session.commit()
        return self.success(data=role)
