#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""
import tornado

from applications.admin.services.menu import MenuService
from applications.core.settings_manager import settings
from applications.core.decorators import required_permissions
from applications.core.db import mysqldb
from ..models import AdminMenu,AdminUser,Role
from .common import CommonHandler

from pyrestful import mediatypes
from pyrestful.rest import get
from pyrestful.rest import delete
from pyrestful.rest import post
from pyrestful.rest import put

class MenuHandler(CommonHandler):
    """docstring for AdminMenu"""

    @delete('/admin/menu')
    @tornado.web.authenticated
    @required_permissions('admin:menu:delete')
    def delete(self):
        """删除菜单
        """
        menu_id = self.get_argument('id', None)
        MenuService.delete_data(menu_id,self.super_role())
        return self.success()


    @put('/admin/menu/sort')
    @tornado.web.authenticated
    @required_permissions('admin:menu:sort')
    def sort(self):

        ids = self.get_argument('ids', None)
        val = self.get_argument('val', 20)
        if int(ids)<0 and not val:
            return self.error('参数错误')

        menu = {
            'sort':val,
        }

        AdminMenu.Q.filter(AdminMenu.id==ids).update(menu)
        AdminMenu.session.commit()
        return self.success()


    @put('/admin/menu/status')
    @tornado.web.authenticated
    @required_permissions('admin:menu:status')
    def status(self):
        ids = self.get_argument('ids', None)
        val = self.get_argument('val', 1)
        menu = {
            'status':val,
        }
        MenuService.save_data(menu, ids)
        return self.success(data=menu)


    @get('/admin/menu',_catch_fire=settings.debug)
    @tornado.web.authenticated
    @required_permissions('admin:menu:web_admin_list')
    def web_admin_list(self):
        """菜单列表"""
        is_nav=self.get_argument('is_nav',None)
        if not self.super_role():
            user_id = self.current_user.get('id')
            menu_list=AdminMenu.get_user_menu(user_id)
        else:
            user_id = 0
            menu_list = AdminMenu.children(user_id=user_id,is_nav=is_nav)

        tab_data = []
        for menu in menu_list:
            tab_data.append({'title': menu.get('title')})
        tab_data.append({'title': '模块排序'})
        params = {
            'menu_list': menu_list,
            'tab_data': tab_data,
        }
        return self.success(msg='成功',data=params)


    @get('/admin/menu/{id}')
    @tornado.web.authenticated
    @required_permissions('admin:menu:detail')
    def detail(self,menu_id):
        """菜单详情"""
        menu_list=AdminMenu.info(menu_id)
        return self.success(msg='成功',data=menu_list)


    @get('/admin/down_menu')
    @tornado.web.authenticated
    @required_permissions('admin:menu:add_menu_list')
    def add_menu_list(self):
        """新增菜单页面，菜单列表"""
        menu=AdminMenu.menu_option('')
        return self.success(msg='成功',data=menu)


    @post('/admin/menu')
    @tornado.web.authenticated
    @required_permissions('admin:menu:web_menu_add')
    def web_menu_add(self):
        """新增菜单"""
        title = self.get_argument('title','')
        code = self.get_argument('code','')
        parent_id = self.get_argument('parent_id',0)
        icon = self.get_argument('icon','')
        path = self.get_argument('path','')
        param = self.get_argument('param','')
        status = self.get_argument('status',1)
        system= self.get_argument('system',0)
        nav= self.get_argument('nav',0)
        user_id=self.get_argument('user_id',0)

        params={
         'title':title,
         'code':code,
         'parent_id':parent_id,
         'icon':icon,
         'path':path,
         'param':param,
         'status':status,
         'system':system,
         'nav':nav,
         'user_id':user_id,

        }

        if not code:
            return self.error('授权码不能够为空')

        if MenuService.check_code(code):
            return self.error('Code已被占用')

        if path[0:4]!='http' and path[0:1]!='/':
            path = '/' + path

        if parent_id and parent_id=='top':
            parent_id = 0

        MenuService.save_data(params,None)

        return self.success(msg='成功')


    @put('/admin/menu')
    @tornado.web.authenticated
    @required_permissions('admin:menu:edit')
    def edit(self):
        """编辑"""
        menu_id = self.get_argument('id', None)
        title = self.get_argument('title','')
        code = self.get_argument('code','')
        parent_id = self.get_argument('parent_id',None)
        icon = self.get_argument('icon','')
        path = self.get_argument('path','')
        param = self.get_argument('param','')
        status = self.get_argument('status',None)
        system= self.get_argument('system',None)
        nav= self.get_argument('nav',None)
        user_id=self.get_argument('user_id',0)

        if int(menu_id)<=0:
            return self.error('参数错误')

        if path[0:4]!='http' and path[0:1]!='/':
           path = '/' + path

        param={
            'title':title,
            'code':code,
            'parent_id':parent_id,
            'icon':icon,
            'path':path,
            'param':param,
            'status':status,
            'system':system,
            'nav':nav,
            'user_id':user_id,
        }
        MenuService.save_data(param, menu_id)
        self.success(msg='成功')
