#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""AdminRole控制器
"""
from trest.router import get
from trest.router import put
from trest.router import post
from trest.router import delete
from trest.exception import JsonError

from applications.admin.utils import required_permissions
from applications.admin.utils import admin_required_login

from applications.admin.services.admin_role import AdminRoleService

from .common import CommonHandler


class AdminRoleHandler(CommonHandler):

    @post('admin_role')
    @admin_required_login
    @required_permissions()
    def admin_role_post(self, *args, **kwargs):
        param = self.params()
        AdminRoleService.insert(param)
        return self.success()

    @get('admin_role/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def admin_role_get(self, id):
        """获取单个记录
        """
        resp_data = AdminRoleService.get(id)
        return self.success(data=resp_data)

    @get('admin_role')
    @admin_required_login
    @required_permissions()
    def admin_role_list_get(self, *args, **kwargs):
        """列表、搜索记录
        """
        page = int(self.get_argument('page', 1))
        per_page = int(self.get_argument('limit', 10))
        title = self.get_argument('title', None)
        status = self.get_argument('status', None)

        param = {}
        if title:
            param['title'] = title
        if status:
            param['status'] = status

        resp_data = AdminRoleService.page_list(param, page, per_page)
        return self.success(data=resp_data)

    @put('admin_role/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def admin_role_put(self, id, *args, **kwargs):
        param = self.params()
        AdminRoleService.update(id, param)
        return self.success(data=param)

    @delete('admin_role/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def admin_role_delete(self, id, *args, **kwargs):
        param = {
            'status': -1
        }
        AdminRoleService.update(id, param)
        return self.success()

    @get('valid_role')
    def valid_role_get(self):
        """获取有效的角色"""
        resp_data = AdminRoleService.valid_list()
        return self.success(data=resp_data)
