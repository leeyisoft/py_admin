#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""公共URL处理器

[description]
"""
import json

from applications.core.models import User
from applications.core.logger.client import SysLogger
from applications.acl import admin_top_menus
from applications.acl import admin_left_menus

from applications.core.handler import WebHandler

class BaseHandler(WebHandler):
    user_session_key = 'userlogged'
    # session = handler.sersion
    # current_user = None

    def _info(self, msg, code, **args):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        data_dict = {
            'code': code,
            'msg': msg,
        }
        data_dict.update(args)

        self.write(json.dumps(data_dict))
        self.finish()
        return

    def res(self, data):
        self.write(str(data))
        self.finish()
        return

    def error(self, msg='error', code=990000):
        return self._info(msg, code)
    def success(self, **args):
        return self._info(msg='success', code=0, **args)

    def admin_menus(self):
        from applications.acl import children_urls
        from applications.acl import get_acl_id

        user = self.session[self.user_session_key]
        menus = {}
        top_menus = []
        left_menus = []
        # 处理选中菜单
        for menu in admin_top_menus():
            urls = children_urls(menu['id'])
            menu['layui_this'] = 'layui-this' if self.request.uri in urls else ''
            top_menus.insert(10, menu)
        # print("top_menus >> ", top_menus)

        # 处理选中菜单
        for menu in admin_left_menus(get_acl_id(self.request.uri)):
            menu['layui_this'] = 'layui-this' if self.request.uri==menu['url'] else ''
            if len(menu['children']):
                children = []
                # 处理选中子菜单
                for child in menu['children']:
                    child['layui_this'] = 'layui-this' if self.request.uri==child['url'] else ''
                    children.insert(10, child)
                menu['children'] = children
            left_menus.insert(10, menu)
        # print("left_menus >> ", left_menus)

        menus['top_menus'] = top_menus
        menus['left_menus'] = left_menus
        # print("menus >> ", menus)
        menus['top_right'] = [
            {'url':'', 'name':user.username, 'img':'http://t.cn/RCzsdCq',
                'children': [
                    {'url':'', 'name':'基本资料'},
                    {'url':'', 'name':'安全设置'},
                ]
            },
            {'url':'/admin/logout.html', 'name':'退了'},
        ]

        menus['curent_uri'] = self.request.uri

        return menus
