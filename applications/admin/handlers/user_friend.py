#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""UserFriend控制器
"""
from trest.router import get
from trest.router import put
from trest.router import post
from trest.router import delete
from trest.exception import JsonError

from applications.admin.utils import required_permissions
from applications.admin.utils import admin_required_login

from applications.admin.services.user_friend import UserFriendService

from .common import CommonHandler


class UserFriendHandler(CommonHandler):

    @post('user_friend')
    @admin_required_login
    @required_permissions()
    def user_friend_post(self, *args, **kwargs):
        param = self.params()
        UserFriendService.insert(param)
        return self.success()

    @get('user_friend/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def user_friend_get(self, id):
        """获取单个记录
        """
        resp_data = UserFriendService.get(id)
        return self.success(data=resp_data)

    @get(['user_friend','user_friend/(?P<category>[a-zA-Z0-9_]*)'])
    @admin_required_login
    @required_permissions()
    def user_friend_list_get(self, category = '', *args, **kwargs):
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

        resp_data = UserFriendService.page_list(param, page, per_page)
        return self.success(data=resp_data)

    @put('user_friend/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def user_friend_put(self, id, *args, **kwargs):
        param = self.params()
        UserFriendService.update(id, param)
        return self.success(data=param)

    @delete('user_friend/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def user_friend_delete(self, id, *args, **kwargs):
        param = {
            'status':-1
        }
        UserFriendService.update(id, param)
        return self.success()
