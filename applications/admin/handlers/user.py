#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""User控制器
"""
from trest.router import get
from trest.router import put
from trest.router import post
from trest.router import delete
from trest.exception import JsonError

from applications.admin.utils import required_permissions
from applications.admin.utils import admin_required_login

from applications.admin.services.user import UserService

from .common import CommonHandler


class UserHandler(CommonHandler):

    @post('user')
    @admin_required_login
    @required_permissions()
    def user_post(self, *args, **kwargs):
        param = self.params()
        UserService.insert(param)
        return self.success()

    @get('user/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def user_get(self, id):
        """获取单个记录
        """
        obj = UserService.get(id)
        data = obj.as_dict() if obj else {}
        return self.success(data = data)

    @get(['user','user/?(?P<category>[a-zA-Z0-9_]*)'])
    @admin_required_login
    @required_permissions()
    def user_list_get(self, category = '', *args, **kwargs):
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

        pagelist_obj = UserService.data_list(param, page, per_page)
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

    @put('user/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def user_put(self, id, *args, **kwargs):
        param = self.params()
        UserService.update(id, param)
        return self.success(data = param)

    @delete('user/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def user_delete(self, id, *args, **kwargs):
        param = {
            'status':-1
        }
        UserService.update(id, param)
        return self.success()
