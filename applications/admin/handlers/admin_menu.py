#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""AdminMenu控制器
"""
import json

from trest.router import get
from trest.router import put
from trest.router import post
from trest.router import delete
from trest.exception import JsonError

from applications.admin.utils import required_permissions
from applications.admin.utils import admin_required_login

from applications.admin.services.admin_menu import AdminMenuService

from .common import CommonHandler


class MenuHandler(CommonHandler):
    """docstring for AdminMenu"""

    # 系统现有api字典，组要用于menu_init_get 根据name过滤menu里面已经存在的API
    apis = {}

    @get('/admin/menu')
    @admin_required_login
    # def menu_list(self):
    def menu_get(self):
        """菜单列表 只需要登录就可以获取，不要参与授权检查（自动过滤非超级管理员未授权节点）
        """
        uid = self.current_user['id']
        menu_list = AdminMenuService.menu_list(uid)
        return self.success(data=menu_list)

    @get('/admin/menu/init')
    @admin_required_login
    def menu_init_get(self):
        """获取特定版本所有菜单 | 超级管理员才有的权限，编辑菜单之前调用
        """
        if not self.super_role():  # 非超级管理员
            raise JsonError('未授权', 401)

        # self.apis = AdminMenuService.api_node_list()
        def filter_menu(i2):
            """ 根据name过滤menu里面已经存在的API """
            if not i2:
                return []
            try:
                name = i2.get('name', '')
                children = i2.get('children', [])
                if name in self.apis.keys():
                    # print('name ', name, type(self.apis), self.apis.keys())
                    # 根据name过滤menu里面已经存在的API
                    i2['name'] = self.apis[name]['name']
                    # i2['title'] = self.apis[name]['title']
                    # path 以后台配置为准，所以不需要覆盖 path
                    i2['method'] = self.apis[name]['method']
                    self.apis.pop(name)
                i2['children'] = [filter_menu(i3) for i3 in children]
                return i2
            except Exception as e:
                # print('i2', i2)
                raise e
        menu_list = AdminMenuService.menu_list(1)
        # 一定要先执行 filter_menu/1 再返回self.apis.items()
        left = [filter_menu(i2) for i2 in menu_list]
        # right = [i1 for (k,i1) in self.apis.items()]
        right = []
        return self.success(data={'right':right,'left':left})

    @post('/admin/menu')
    @admin_required_login
    def menu_post(self):
        """保存修改的菜单 | 超级管理员才有的权限
        """
        if not self.super_role():  # 非超级管理员
            raise JsonError('未授权', 401)
        tree = self.get_argument('tree')
        if '\\u' in tree:
            tree = tree.encode('utf-8').decode('unicode_escape')
        # print('tree ', type(tree), tree)
        try:
            tree = json.loads(tree)
            AdminMenuService.save_data(tree)
        except JsonError as e:
            raise e
        except json.decoder.JSONDecodeError as e:
            raise JsonError('需要json数据')
        except Exception as e:
            raise e
        self.success()
