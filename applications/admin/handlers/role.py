#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""
import tornado

from trest.router import get
from trest.router import put
from trest.router import post
from trest.router import delete
from trest.exception import JsonError
from trest.settings_manager import settings

from applications.admin.services.role import RoleService
from applications.admin.services.menu import AdminMenuService
from applications.admin.utils import required_permissions
from ..models import AdminMenu
from .common import CommonHandler


class RoleHandler(CommonHandler):
    """docstring for Passport"""

    @post('/admin/role')
    @tornado.web.authenticated
    @required_permissions()
    def web_role_add(self):
        """新增角色"""
        rolename = self.get_argument('rolename', None)
        role = {
            'rolename': rolename,
            'status': 1,
            'id':None

        }
        RoleService.save_data(self.super_role(), role)
        return self.success()

    @put('/admin/role')
    @tornado.web.authenticated
    @required_permissions()
    def web_role_edit(self):
        rolename = self.get_argument('rolename', None)
        roleid = self.get_argument('id', None)
        sort = self.get_argument('sort', None)
        status = self.get_argument('status', 0)
        permission = self.get_argument('permission',[])

        if not roleid:
            return self.error('参数错误')

        role = {
            'status': status,
            'rolename':rolename,
            'permission':permission,
            'sort':sort,
        }
        RoleService.save_data(self.super_role(), role, roleid)
        return self.success(data=role)

    @get(r'/admin/role/(?P<role_id>\d*)')
    @tornado.web.authenticated
    @required_permissions()
    def role_detail(self, role_id):
        """个人角色列表"""
        # role_id = kwargs.get('role_id',None)
        role = RoleService.get_info(role_id)
        if not role:
            return self.error('不存在的数据')
        return self.success(data=role.as_dict())


    @get('/admin/role')
    @tornado.web.authenticated
    @required_permissions()
    def web_role_list(self, *args, **kwargs):
        """角色列表"""
        limit = self.get_argument('limit', '10')
        page = self.get_argument('page', '1')
        pagelist_obj = RoleService.get_data(limit, page)
        items2=[]
        for item in pagelist_obj.items:
            val=item.as_dict()
            if not val['permission'] or val['permission']=='':
                val['permission']=[]
            else:
                val['permission']=val['permission'].replace('\\','').replace('[','').replace(']','').replace('"','').split(',')
            items2.append(val)

        params = {
            'page':page,
            'per_page':limit,
            'total':pagelist_obj.total,
            'items': items2,
        }
        return self.success(data=params)

    # @get('/admin/permission')
    # @tornado.web.authenticated
    # def permission_list(self):
    #     """权限菜单列表"""
    #     # menu_list = AdminMenuService.children(status=1)
    #     menu_list = []
    #     return self.success(msg='成功xx',data=menu_list)


    @delete('/admin/role')
    @tornado.web.authenticated
    @required_permissions()
    def web_role_delete(self):
        """删除角色
        """
        role_id = self.get_argument('role_id', None)
        RoleService.delete_data(role_id)
        return self.success()
