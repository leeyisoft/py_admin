#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Goods控制器
"""
from trest.router import get
from trest.router import put
from trest.router import post
from trest.router import delete
from trest.exception import JsonError

from applications.admin.utils import required_permissions
from applications.admin.utils import admin_required_login

from applications.admin.services.goods import GoodsService

from .common import CommonHandler


class GoodsHandler(CommonHandler):

    @post('goods')
    @admin_required_login
    @required_permissions()
    def goods_post(self, *args, **kwargs):
        param = self.params()
        GoodsService.insert(param)
        return self.success()

    @get('goods/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def goods_get(self, id):
        """获取单个记录
        """
        resp_data = GoodsService.get(id)
        return self.success(data=resp_data)

    @put('goods/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def goods_put(self, id, *args, **kwargs):
        param = self.params()
        GoodsService.update(id, param)
        return self.success(data=param)

    @delete('goods/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def goods_delete(self, id, *args, **kwargs):
        param = {
            'status':-1
        }
        GoodsService.update(id, param)
        return self.success()


class GoodsListHandler(CommonHandler):
    @get(['goods','goods/(?P<category>[a-zA-Z0-9_]*)'])
    @admin_required_login
    @required_permissions()
    def goods_list_get(self, category = '', *args, **kwargs):
        """列表、搜索记录
        """
        page = int(self.get_argument('page', 1))
        per_page = int(self.get_argument('limit', 10))
        id = self.get_argument('id', None)
        title = self.get_argument('title', None)
        status = self.get_argument('status', None)

        param = {}
        if category:
            param['category'] = category
        if id:
            param['id'] = id
        if title:
            param['title'] = title
        if status:
            param['status'] = status

        resp_data = GoodsService.page_list(param, page, per_page)
        return self.success(data=resp_data)
