#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advertising控制器
"""
from trest.router import get
from trest.router import put
from trest.router import post
from trest.router import delete
from trest.exception import JsonError

from applications.admin.utils import required_permissions
from applications.admin.utils import admin_required_login

from applications.admin.services.advertising import AdvertisingService

from .common import CommonHandler


class AdvertisingHandler(CommonHandler):

    @post('advertising')
    @admin_required_login
    @required_permissions()
    def advertising_post(self, *args, **kwargs):
        param = self.params()
        AdvertisingService.insert(param)
        return self.success()

    @get('advertising/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def advertising_get(self, id):
        """获取单个记录
        """
        resp_data = AdvertisingService.get(id)
        return self.success(data=resp_data)

    @get(['advertising','advertising/(?P<category>[a-zA-Z0-9_]*)'])
    @admin_required_login
    @required_permissions()
    def advertising_list_get(self, category = '', *args, **kwargs):
        """列表、搜索记录
        """
        page = int(self.get_argument('page', 1))
        per_page = int(self.get_argument('limit', 10))
        id = self.get_argument('id', None)
        title = self.get_argument('title', None)
        status = self.get_argument('status', None)
        category_id = self.get_argument('category_id', None)
        param = {}
        if category:
            param['category'] = category
        if id:
            param['id'] = id
        if title:
            param['title'] = title
        if status:
            param['status'] = status
        if category_id:
            param['category_id'] = category_id

        resp_data = AdvertisingService.page_list(param, page, per_page)
        return self.success(data=resp_data)

    @put('advertising/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def advertising_put(self, id, *args, **kwargs):
        param = self.params()
        AdvertisingService.update(id, param)
        return self.success(data=param)

    @delete('advertising/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def advertising_delete(self, id, *args, **kwargs):
        param = {
            'status':-1
        }
        AdvertisingService.update(id, param)
        return self.success()
