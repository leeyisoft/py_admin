#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""

import tornado

from applications.core.settings_manager import settings
from applications.core.logger.client import SysLogger
from applications.core.decorators import required_permissions
from applications.core.utils import Func

from ..models import AdminMenu

from .common import CommonHandler


class MenuHandler(CommonHandler):
    """docstring for AdminMenu"""
    @tornado.web.authenticated
    @required_permissions('admin:menu:index')
    def get(self, *args, **kwargs):
        if not self.super_role():
            user_id = user_id = self.current_user.get('uuid')
        else:
            user_id = False

        menu_list = AdminMenu.children(user_id=user_id)
        tab_data = []
        for menu in menu_list:
            tab_data.append({'title': menu.get('title')})

        tab_data.append({'title': '模块排序'})
        params = {
            'menu_list': menu_list,
            'tab_data': tab_data,
        }
        # print('tab_data ', tab_data)
        self.render('menu/index.html', **params)

    """docstring for AdminMenu"""
    @tornado.web.authenticated
    @required_permissions('admin:menu:delete')
    def delete(self, *args, **kwargs):
        """删除菜单
        """
        uuid = self.get_argument('uuid', None)
        menu_tab = self.get_argument('menu_tab', None)

        menu = AdminMenu.Q.filter(AdminMenu.uuid==uuid).first()
        if (not self.super_role()) and menu.system==1:
            return self.error('系统菜单，无法删除')

        count = AdminMenu.Q.filter(AdminMenu.parent_id==uuid).count()
        if count>0:
            return self.error('请先删除子菜单')

        AdminMenu.Q.filter(AdminMenu.uuid==uuid).delete()
        AdminMenu.session.commit()
        return self.success()


class MenuEditHandler(CommonHandler):
    """docstring for AdminMenu"""
    @tornado.web.authenticated
    @required_permissions('admin:menu:edit')
    def get(self, *args, **kwargs):
        uuid = self.get_argument('uuid', None)
        if not uuid:
            return self.error('UUID为空')

        data_info = AdminMenu.info(uuid)

        params = {
            'menu_option': AdminMenu.menu_option(uuid),
            'menu_tab': self.get_argument('menu_tab', 1),
            'data_info': data_info,
        }
        self.render('menu/edit.html', **params)

    @tornado.web.authenticated
    @required_permissions('admin:role:edit')
    def post(self, *args, **kwargs):
        uuid = self.get_argument('uuid', None)
        menu_tab = self.get_argument('menu_tab', 1)
        if not uuid:
            return self.error('UUID为空')

        params = self.params()
        params.pop('uuid', None)
        params.pop('user_id', None)
        params.pop('menu_tab', None)
        params.pop('_xsrf', None)

        path = params.get('path', None)
        if path[0:4]!='http' and path[0:1]!='/':
            params['path'] = '/' + path

        # print('params ', type(params), params)
        AdminMenu.Q.filter(AdminMenu.uuid==uuid).update(params)
        AdminMenu.session.commit()
        self.redirect('/admin/menu/index?#menu_tab=%s'%menu_tab)


class MenuAddHandler(CommonHandler):
    """docstring for AdminMenu"""
    @tornado.web.authenticated
    @required_permissions('admin:menu:add')
    def get(self, *args, **kwargs):
        parent_id = self.get_argument('parent_id', None)
        uuid = ''
        menu = AdminMenu(parent_id=parent_id)
        data_info = menu.as_dict()

        params = {
            'menu_option': AdminMenu.menu_option(uuid),
            'menu_tab': self.get_argument('menu_tab', 1),
            'data_info': data_info,
        }
        self.render('menu/edit.html', **params)

    @tornado.web.authenticated
    @required_permissions('admin:role:add')
    def post(self, *args, **kwargs):
        menu_tab = self.get_argument('menu_tab', 1)

        params = self.params()
        params['uuid'] = Func.uuid32()
        params.pop('user_id', None)
        params.pop('menu_tab', None)
        params.pop('_xsrf', None)

        path = params.get('path', None)
        if path[0:4]!='http' and path[0:1]!='/':
            params['path'] = '/' + path

        user_id = self.current_user.get('uuid')
        role_id = self.current_user.get('role_id')
        if not self.super_role():
            params['user_id'] = user_id

        menu = AdminMenu(**params)
        AdminMenu.session.add(menu)
        AdminMenu.session.commit()

        self.redirect('/admin/menu/index?#menu_tab=%s'%menu_tab)


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


class MenuIconHandler(CommonHandler):
    """docstring for AdminMenu"""
    @tornado.web.authenticated
    @required_permissions('admin:menu:icon')
    def get(self, *args, **kwargs):

        params = {
            'input': self.get_argument('input', 'input-icon'),
            'show': self.get_argument('show', 'form-icon-preview'),
        }
        self.render('menu/icon.html', **params)
