#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""
import tornado

from pyrestful import mediatypes
from trest.router import get

from trest.settings_manager import settings
from trest.logger.client import SysLogger
from trest.utils.hasher import make_password
from applications.admin.utils import required_permissions

from ..models import AdminMenu

from .common import CommonHandler


class IndexHandler(CommonHandler):
    @get(_path='/admin/main'
        ,_produces=mediatypes.TEXT_XML)
    @tornado.web.authenticated
    def main(self, *args, **kwargs):
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

        user = AdminUser.Q.filter(AdminUser.id==self.current_user.get("id")).first()
        _bread_crumbs = AdminMenu.brand_crumbs(c_menu['id'])
        _admin_menu_parents = _bread_crumbs[0] if len(_bread_crumbs) else {'parent_id':'1'}
        _admin_menu = AdminMenu.main_menu(user=user)

        params = {
            '_admin_menu': _admin_menu,
            '_admin_menu_parents': _admin_menu_parents,
            '_bread_crumbs': _bread_crumbs,
        }
        self.render('dashboard/main.html', **params)

    @get(_path='/admin/system/index',_produces=mediatypes.APPLICATION_JSON)
    def index(self, *args, **kwargs):
        """
        """
        data = {
            '_xsrf': self.xsrf_token.decode("utf-8"),
        }
        return self.success(data=data)

    @get(_path='/admin/system/menu',_produces=mediatypes.APPLICATION_JSON)
    # @tornado.web.authenticated
    def menu(self, *args, **kwargs):
        """后台首页
        """
        user = AdminUser.Q.filter(AdminUser.id==self.current_user.get("id")).first()
        _admin_menu = AdminMenu.main_menu(user=user)
        return self.success(data=_admin_menu)
