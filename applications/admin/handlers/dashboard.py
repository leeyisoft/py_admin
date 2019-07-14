#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""
import tornado

from trest.exception import JsonError
from trest.router import get
from trest.router import post

from trest.settings_manager import settings
from trest.logger.client import SysLogger
from trest.utils.hasher import make_password
from applications.admin.utils import required_permissions
from trest.exception import JsonError

from applications.admin.services.menu import AdminMenuService
from ..models import AdminMenu
from ..models import AdminUser

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

        _admin_menu = AdminMenuService.menu_list(self.current_user.get('id'))
        _admin_menu_parents = {
            'name': ''
        }

        params = {
            '_admin_menu': _admin_menu,
            '_admin_menu_parents': _admin_menu_parents,
            '_bread_crumbs': '',
        }
        self.render('dashboard/main.html', **params)

class WelcomeHandler(CommonHandler):
    @get('welcome')
    @required_permissions()
    @tornado.web.authenticated
    async def welcome_get(self, *args, **kwargs):
        """后台首页
        """
        # menu = AdminMenu.main_menu()
        # print('menu ', menu)
        # self.show('abc')
        params = {
        }
        self.render('dashboard/welcome.html', **params)

    @get('welcome2')
    async def welcome_get2(self, *args, **kwargs):
        """后台首页
        """
        self.success(data=['welcome2'])

    @get('/welcome3')
    async def welcome_get3(self, *args, **kwargs):
        """后台首页
        """
        self.success(data=['welcome3'])

    @post('welcome4')
    async def welcome_post(self, *args, **kwargs):
        """后台首页
        """
        self.success(data=['welcome3'])
