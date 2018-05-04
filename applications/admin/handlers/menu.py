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
        # print('AdminMenu', dir(AdminMenu))
        uuid = self.get_argument('uuid', None)
        if not uuid:
            return self.error('UUID为空')

        data_info = AdminMenu.info(uuid)

        params = {
            'menu_option': self._menu_option(uuid),
            'menu_tab': self.get_argument('menu_tab', 1),
            'data_info': data_info,
        }
        self.render('menu/edit.html', **params)

    def _menu_option(self, uuid=''):
        #
        menus = AdminMenu.main_menu()
        if not len(menus)>0:
            return ''
        option1 = '<option level="1" value="%s" %s>— %s</option>'
        option2 = '<option level="2" value="%s" %s>—— %s</option>'
        option3 = '<option level="3" value="%s" %s>——— %s</option>'
        html = ''
        for menu in menus:
            selected = 'selected' if uuid==menu.get('uuid', '') else ''
            title1 = menu.get('title', '')
            children1 = menu.get('children', [])
            html += option1 % (menu.get('uuid', ''), selected, title1)
            if not len(children1)>0:
                continue
            for menu2 in children1:
                selected2 = 'selected' if uuid==menu2.get('uuid', '') else ''
                title2 = menu2.get('title', '')
                html += option2 % (menu2.get('uuid', ''), selected2, title2)
                children2 = menu.get('children', [])
                if not len(children2)>0:
                    continue
                for menu3 in children2:
                    selected3 = 'selected' if uuid==menu3.get('uuid', '') else ''
                    title3 = menu3.get('title', '')
                    html += option3 % (menu3.get('uuid', ''), selected3, title3)

        return html

    @tornado.web.authenticated
    @required_permissions('admin:role:edit')
    def post(self, *args, **kwargs):
        uuid = self.get_argument('uuid', None)
        menu_tab = self.get_argument('menu_tab', None)
        if not uuid:
            return self.error('UUID为空')

        menu = self.params()

        menu.pop('menu_tab')
        menu.pop('_xsrf')

        path = menu.get('path', None)
        if path[0:4]!='http' and path[0:1]!='/':
            menu['path'] = '/' + path

        AdminMenu.Q.filter(AdminMenu.uuid==uuid).update(menu)
        AdminMenu.session.commit()
        self.redirect('/admin/menu/index?#menu_tab=%s'%menu_tab)


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
