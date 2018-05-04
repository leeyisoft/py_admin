#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""

import tornado

from applications.core.settings_manager import settings
from applications.core.logger.client import SysLogger
from applications.core.utils import utc_to_timezone
from applications.core.decorators import required_permissions

from applications.admin.models.system import AdminMenu

from .common import CommonHandler


class MenuHandler(CommonHandler):
    """docstring for AdminMenu"""
    @tornado.web.authenticated
    @required_permissions('admin:menu:index')
    def get(self, *args, **kwargs):
        menu_list = AdminMenu.children()
        tab_data = []
        for menu in menu_list:
            tab_data.append({'title': menu.get('title')})

        tab_data.append({'title': '模块排序'})
        params = {
            'menu_list': menu_list,
            'tab_data': tab_data,
        }
        print('request ', self.request)
        self.render('menu/index.html', **params)

    """docstring for AdminMenu"""
    @tornado.web.authenticated
    @required_permissions('admin:menu:delete')
    def delete(self, *args, **kwargs):
        return self.success()


class MenuEditHandler(CommonHandler):
    """docstring for AdminMenu"""
    @tornado.web.authenticated
    @required_permissions('admin:menu:edit')
    def get(self, *args, **kwargs):
        uuid = self.get_argument('uuid', None)
        if not uuid:
            return self.error('UUID为空')

        params = {
            'menu_option': self._menu_option,
            'menu_tab': self.get_argument('menu_tab', 1),
        }
        self.render('menu/edit.html', **params)

    def _menu_option(id=''):

        menus = AdminMenu.main_menu()
        for menu in menus:
            pass


class MenuAddHandler(CommonHandler):
    """docstring for AdminMenu"""
    @tornado.web.authenticated
    @required_permissions('admin:menu:add')
    def get(self, *args, **kwargs):
        menu_list = AdminMenu.children()
        tab_data = []
        for menu in menu_list:
            tab_data.append({'title': menu.get('title')})

        tab_data.append({'title': '模块排序'})
        params = {
            'menu_list': menu_list,
            'tab_data': tab_data,
        }
        self.render('menu/add.html', **params)

class MenuSortHandler(CommonHandler):
    """docstring for AdminMenu"""
    @tornado.web.authenticated
    @required_permissions('admin:menu:sort')
    def post(self, *args, **kwargs):
        ids = self.get_argument('ids', None)
        val = self.get_argument('val', 20)
        menu = {
            'sort':val,
        }
        AdminMenu.Q.filter(AdminMenu.uuid==ids).update(menu)
        AdminMenu.session.commit()
        return self.success(data=menu)

class MenuStatusHandler(CommonHandler):
    """docstring for AdminMenu"""
    @tornado.web.authenticated
    @required_permissions('admin:menu:status')
    def get(self, *args, **kwargs):
        ids = self.get_argument('ids', None)
        val = self.get_argument('val', 1)
        menu = {
            'status':val,
        }
        AdminMenu.Q.filter(AdminMenu.uuid==ids).update(menu)
        AdminMenu.session.commit()
        return self.success(data=menu)
