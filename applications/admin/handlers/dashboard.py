#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""
import tornado

from applications.core.settings_manager import settings
from applications.core.logger.client import SysLogger
from applications.core.utils.hasher import make_password
from applications.core.decorators import required_permissions

from ..models import AdminMenu

from .common import CommonHandler


class MainHandler(CommonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        """后台首页
        """
        path = self.request.path
        path_set = ['admin', 'admin/index']
        if self.request.path.strip('/') in path_set:
            path = '/admin/main/'

        c_menu = AdminMenu.info(path=path)
        if not c_menu:
            msg = '节点不存在或者已禁用！'
            return self.error(code=404, msg=msg);

        _bread_crumbs = AdminMenu.brand_crumbs(c_menu['id'])
        _admin_menu_parents = _bread_crumbs[0] if len(_bread_crumbs) else {'parent_id':'1'}
        _admin_menu = AdminMenu.main_menu()

        params = {
            '_admin_menu': _admin_menu,
            '_admin_menu_parents': _admin_menu_parents,
            '_bread_crumbs': _bread_crumbs,
        }
        self.render('dashboard/main.html', **params)

class WelcomeHandler(CommonHandler):
    @tornado.web.authenticated
    @required_permissions('admin:welcome')
    def get(self, *args, **kwargs):
        """后台首页
        """
        # menu = AdminMenu.main_menu()
        # print('menu ', menu)
        # self.show('abc')
        params = {
        }
        self.render('dashboard/welcome.html', **params)
