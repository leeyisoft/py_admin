#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""AdminUserLoginLog控制器
"""
from trest.router import get
from trest.router import put
from trest.router import post
from trest.router import delete
from trest.exception import JsonError

from applications.admin.utils import required_permissions
from applications.admin.utils import admin_required_login

from applications.admin.services.admin_user_login_log import AdminUserLoginLogService

from .common import CommonHandler


class AdminUserLoginLogHandler(CommonHandler):

    @post('admin_user_login_log')
    @admin_required_login
    @required_permissions()
    def admin_user_login_log_post(self, *args, **kwargs):
        param = self.params()
        AdminUserLoginLogService.insert(param)
        return self.success()

    @get('admin_user_login_log/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def admin_user_login_log_get(self, id):
        """获取单个记录
        """
        resp_data = AdminUserLoginLogService.get(id)
        return self.success(data=resp_data)

    @delete('admin_user_login_log/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def admin_user_login_log_delete(self, id, *args, **kwargs):
        param = {
            'status':-1
        }
        AdminUserLoginLogService.update(id, param)
        return self.success()
