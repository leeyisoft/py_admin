#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""AdvertisingCategory控制器
"""
from trest.router import get
from trest.router import put
from trest.router import post
from trest.router import delete
from trest.exception import JsonError

from applications.admin.utils import required_permissions
from applications.admin.utils import admin_required_login

from applications.admin.services.advertising_category import AdvertisingCategoryService

from .common import CommonHandler


class AdvertisingCategoryHandler(CommonHandler):

    @post('advertising_category')
    @admin_required_login
    @required_permissions()
    def advertising_category_post(self, *args, **kwargs):
        param = self.params()
        AdvertisingCategoryService.insert(param)
        return self.success()

    @get('advertising_category/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def advertising_category_get(self, id):
        """获取单个记录
        """
        resp_data = AdvertisingCategoryService.get(id)
        return self.success(data=resp_data)

    @get('advertising_category')
    @admin_required_login
    @required_permissions()
    def advertising_category_list_get(self, *args, **kwargs):
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

        resp_data = AdvertisingCategoryService.page_list(param, page, per_page)
        return self.success(data=resp_data)

    @put('advertising_category/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def advertising_category_put(self, id, *args, **kwargs):
        param = self.params()
        AdvertisingCategoryService.update(id, param)
        return self.success(data=param)

    @delete('advertising_category/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def advertising_category_delete(self, id, *args, **kwargs):
        param = {
            'status':-1
        }
        AdvertisingCategoryService.update(id, param)
        return self.success()

    @get('advertising_category/valid')
    @admin_required_login
    # @required_permissions()
    def advertising_category_valid_get(self):
        """
        有效的分类列表
        :return:
        """
        data = AdvertisingCategoryService.data_list_valid()
        return self.success(data=data)
