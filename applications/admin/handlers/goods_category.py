#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""GoodsCategory控制器
"""
from trest.router import get
from trest.router import put
from trest.router import post
from trest.router import delete
from trest.exception import JsonError

from applications.admin.utils import required_permissions
from applications.admin.utils import admin_required_login

from applications.admin.services.goods_category import GoodsCategoryService

from .common import CommonHandler


class GoodsCategoryHandler(CommonHandler):

    @post('goods_category')
    @admin_required_login
    @required_permissions()
    def goods_category_post(self, *args, **kwargs):
        param = self.params()
        GoodsCategoryService.insert(param)
        return self.success()

    @get('goods_category/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def goods_category_get(self, id):
        """获取单个记录
        """
        obj = GoodsCategoryService.get(id)
        data = obj.as_dict() if obj else {}
        return self.success(data = data)

    @get(['goods_category','goods_category/?(?P<category>[a-zA-Z0-9_]*)'])
    @admin_required_login
    @required_permissions()
    def goods_category_list_get(self, category = '', *args, **kwargs):
        """列表、搜索记录
        """
        page = int(self.get_argument('page', 1))
        per_page = int(self.get_argument('limit', 10))
        title = self.get_argument('title', None)
        status = self.get_argument('status', None)

        param = {}
        if category:
            param['category'] = category
        if title:
            param['title'] = title
        if status:
            param['status'] = status

        pagelist_obj = GoodsCategoryService.data_list(param, page, per_page)
        items = []
        for val in pagelist_obj.items:
            data = val.as_dict()
            items.append(data)
        resp = {
            'page':page,
            'per_page':per_page,
            'total':pagelist_obj.total,
            'items':items,
        }
        return self.success(data = resp)

    @put('goods_category/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def goods_category_put(self, id, *args, **kwargs):
        param = self.params()
        GoodsCategoryService.update(id, param)
        return self.success(data = param)

    @delete('goods_category/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def goods_category_delete(self, id, *args, **kwargs):
        param = {
            'status':-1
        }
        GoodsCategoryService.update(id, param)
        return self.success()
