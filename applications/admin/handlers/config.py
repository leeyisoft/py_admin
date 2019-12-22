#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Config控制器
"""
from trest.router import get
from trest.router import put
from trest.router import post
from trest.router import delete
from trest.exception import JsonError

from applications.admin.utils import required_permissions
from applications.admin.utils import admin_required_login

from applications.admin.services.config import ConfigService

from .common import CommonHandler


class ConfigHandler(CommonHandler):

    @post('config')
    @admin_required_login
    @required_permissions()
    def config_post(self, *args, **kwargs):
        param = self.params()
        ConfigService.insert(param)
        return self.success()

    @get('config/(?P<key>[a-zA-Z0-9_]+)')
    @admin_required_login
    @required_permissions()
    def config_get(self, key):
        """获取单个记录
        """
        resp_data = ConfigService.get(key)
        return self.success(data=resp_data)

    @get('config')
    @admin_required_login
    @required_permissions()
    def config_list_get(self, *args, **kwargs):
        """列表、搜索记录
        """
        page = int(self.get_argument('page', 1))
        per_page = int(self.get_argument('limit', 10))
        key = self.get_argument('key', None)
        status = self.get_argument('status', None)

        param = {}

        if key:
            param['key'] = key
        if status:
            param['status'] = status

        resp_data = ConfigService.page_list(param, page, per_page)
        return self.success(data=resp_data)

    @put('config/(?P<key>[a-zA-Z0-9_]+)')
    @admin_required_login
    @required_permissions()
    def config_put(self, key, *args, **kwargs):
        param = self.params()
        ConfigService.update(key, param)
        return self.success(data=param)

    @delete('config/(?P<key>[a-zA-Z0-9_]+)')
    @admin_required_login
    @required_permissions()
    def config_delete(self, key, *args, **kwargs):
        param = {
            'status':-1
        }
        ConfigService.update(key, param)
        return self.success()
