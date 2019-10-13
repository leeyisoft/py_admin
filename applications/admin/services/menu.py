#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
菜单管理
* 以 菜单节点 name 为授权码
* 一颗完整的菜单树为 base_menu 加 0 或者多个 API节点
* 一个经过配置的API节点，有如下信息，如果icon不为空，nav就为1

一个没做任务配置的API节点，会有3项数据
{
    name: "login_page",
    path: "/admin/login",
    component: ""
}

"""
import re
import os
import json
import inspect
from tornado.util import import_object
from trest.exception import JsonError
from trest.utils import func
from trest.config import settings
from applications.admin.models import AdminUser
from applications.admin.services.user import AdminUserService


class AdminMenuService:
    @staticmethod
    def info(name):
        item = {
            "nav": 1,
            "status": 1,
            "system": 1,
            "name": "admin:content:index",
            "title": "内容",
            "icon": "aicon ai-xitonggongneng",
            "path": "/admin/content/index",
            "param": "",
            "children": []
        }
        return item

    @classmethod
    def brand_crumbs(cls, id):
        """获取当前节点的面包屑

        [description]

        Arguments:
            id {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        menu = []
        return menu

    @staticmethod
    def save_data(tree):
        """
        保存菜单树
        """
        fpath = os.path.join(settings.ROOT_PATH, 'datas', 'json', 'menu.json')
        formatted_json = json.dumps(tree, ensure_ascii=False, indent = 4, sort_keys=False)

        with open(fpath) as f:
            md50 = func.md5(formatted_json)
            md51 = func.md5(f.read())
            if md50==md51:
                raise JsonError('数据没有变化', 0)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(formatted_json)
            f.write("\n")
        return True

    @staticmethod
    def menu_list(uid):
        """
        获取菜单树
        """
        if not(uid>0):
            raise JsonError('请登录', 706)
        menu_json = os.path.join(settings.ROOT_PATH, 'datas', 'json', 'menu.json')
        menus = []
        try:
            with open(menu_json) as f:
                menus = json.loads(f.read())
        except Exception as e:
            pass
        user = AdminUser.Q.filter(AdminUser.id==uid).first()
        if AdminUserService.is_super_role(uid, user.role_id):
            return menus
        # print('query.statement: ', query.statement)
        permission = user.user_permission + user.role_permission if user else []
        def _filter_permission(m1):
            """
            检查菜单是否存在授权列表中
            """
            if not m1:
                return False
            name = m1.get('name', '')
            if name not in permission:
                return False
            m1['children'] = list(filter(_filter_permission, m1.get('children', [])))
            return m1
        return list(filter(_filter_permission, menus))

    @staticmethod
    def api_node_list():
        """
        获取后端API节点信息
        API docstring 需要包含 "[\s\S]*menu:([\s\S]*)endmenu[\s\S]*" 格式数据例如：
            案例1：
                menu:
                    component - Layout
                    title - 修改密码 | 用于标题
                    icon - | 空字符串，或不填写，当有icon的时候，为 nav=1
                    param -
                endmenu

            案例2：
                menu:
                    component - Layout
                    title - 锁屏解锁 | 用于标题
                    icon - | 空字符串，或不填写，当有icon的时候，为 nav=1
                    param - ?status=1&role_id=2
                endmenu

            案例3：
                menu:
                    component - Layout
                    title - 管理员管理 | 用于标题
                    icon - user | 空字符串，或不填写，当有icon的时候，为 nav=1
                    param -
                endmenu
            案例4：
                menu:
                    title - 管理员管理
                endmenu
        """
        app_name = 'admin'
        app_urls = import_object(f'applications.{app_name}.urls.urls')
        # print('app_urls ', type(app_urls), app_urls)
        data = []
        for hanlder in app_urls:
            if type(hanlder)==tuple:
                continue
            apis = list(hanlder.__dict__.items())
            data += [f1.__dict__ for (n,f1) in apis if inspect.isfunction(f1)]
        # endfor
        apis = {}
        for item in data:
            try:
                item2 = {}
                item2['name']  = item['func_name']
                item2['path']  = item['_path']
                item2['method'] = item['_method']
                component = ''
                if item['func_doc']:
                    res = re.findall('[\s\S]*menu:([\s\S]*)endmenu[\s\S]*', item['func_doc'])
                    args = [i for i in res[0].split('\n') if i.strip()]
                    if not args:
                        continue
                    for i in args:
                        i2 = i.split('-', 1)
                        key = i2[0].strip().lower()
                        val = i2[1] if len(i2)>1 else ''
                        val = val.split('|', 1)[0].strip()
                        if key=='component':
                            component = val
                        else:
                            item2[key] = val
                else:
                    continue
                item2['component']  =  component
                if item2.get('icon', ''):
                    item2['nav'] = 1
                apis[item['func_name']] = item2
            except Exception as e:
                # print('item ', type(item), item)
                continue
        return apis
