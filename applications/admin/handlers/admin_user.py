#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""AdminUser控制器
"""
import json
from trest.router import get
from trest.router import put
from trest.router import post
from trest.router import delete
from trest.exception import JsonError

from applications.admin.utils import required_permissions
from applications.admin.utils import admin_required_login

from applications.admin.services.admin_user import AdminUserService
from applications.admin.services.admin_menu import AdminMenuService

from .common import CommonHandler


class AdminUserHandler(CommonHandler):
    @post('admin_user')
    @admin_required_login
    @required_permissions()
    def admin_user_post(self, *args, **kwargs):
        """新增管理员"""
        role_id = self.get_argument('role_id', None)
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        email = self.get_argument('email', None)
        mobile = self.get_argument('mobile', None)
        status = self.get_argument('status', '1')
        permission = self.get_argument('permission', [])
        rsa_encrypt = self.get_argument('rsa_encrypt', 1)

        if not username:
            raise JsonError('用户名不能为空')
        if not password:
            raise JsonError('密码不能为空')
        param = {
            'status': status,
            'username': username,
            'password': password,
            'mobile': mobile,
            'email': email,
            'permission':permission,
            'role_id':role_id
        }

        AdminUserService.insert(param)
        return self.success()

    @get('admin_user/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def admin_user_get(self, id):
        """获取单个记录
        """
        resp_data = AdminUserService.get(id)
        return self.success(data=resp_data)

    @get('admin_user')
    @admin_required_login
    @required_permissions()
    def admin_user_list_get(self, *args, **kwargs):
        """列表、搜索记录
        """
        page = int(self.get_argument('page', 1))
        per_page = int(self.get_argument('limit', 10))
        title = self.get_argument('title', None)
        status = self.get_argument('status', None)
        mobile = self.get_argument('mobile', None)
        username = self.get_argument('username', None)
        role_id = self.get_argument('role_id', None)

        param = {}
        if title:
            param['title'] = title
        if status:
            param['status'] = status
        if mobile:
            param['mobile'] = mobile
        if username:
            param['username'] = username
        if role_id:
            param['role_id'] = role_id

        resp_data = AdminUserService.page_list(param, page, per_page)
        return self.success(data=resp_data)

    @put('admin_user/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def admin_user_put(self, id, *args, **kwargs):
        role_id = self.get_argument('role_id', None)
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        rsa_encrypt = self.get_argument('rsa_encrypt', '0')
        email = self.get_argument('email', None)
        mobile = self.get_argument('mobile', None)
        status = self.get_argument('status', '0')
        permission = self.get_argument('permission', [])

        if not id:
            raise JsonError('Edit用户ID不能为空')
        param = {
            'id': id,
            'status': status,
            'username': username,
            'mobile': mobile,
            'email': email
        }
        param['permission'] = '[]'
        try:
            param['permission'] = json.dumps(permission)
        except Exception as e:
            pass
        if role_id:
            param['role_id'] = role_id
        AdminUserService.update(id, param, rsa_encrypt)
        return self.success(data=param)

    @delete('admin_user/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def admin_user_delete(self, id, *args, **kwargs):
        param = {
            'status': -1
        }
        AdminUserService.update(id, param)
        return self.success()

    @get('/admin/init')
    def admin_init_get(self):
        """系统配置信息"""
        resp_data = AdminUserService.admin_init(self.xsrf_token.decode('utf-8'))
        return self.success(data=resp_data)

    @get('/admin/info')
    @admin_required_login
    def admin_info_get(self, *args, **kwargs):
        data = {
            'name': 'admin',
            'avatar' : self.static_url('image/default_avatar.jpg'),
            'menus': AdminMenuService.menu_list(1),
        }
        return self.success(data=data)


class UnlockAdminHandler(CommonHandler):
    @put('/admin/admin/unlocked')
    @admin_required_login
    def unlock_user(self):
        """锁屏解锁"""
        password = self.get_argument('password', None)
        if not password:
            raise JsonError('请输入密码')

        current_uid = self.current_user.get('id', 0)
        AdminUserService.unlock_user(current_uid, password);
        return self.success()


class AdminChangePwdHandler(CommonHandler):
    @put('/admin/admin/change_pwd')
    @admin_required_login
    @required_permissions()
    def admin_change_pwd(self):
        """
        修改密码
        :return:
        """
        password = self.get_argument('password', None)
        rsa_encrypt = self.get_argument('rsa_encrypt', None)
        admin_id = self.get_argument('admin_id', None)
        if password is None or rsa_encrypt is None or admin_id is None:
            raise JsonError('参数必须')

        AdminUserService.change_pwd(user, rsa_encrypt, admin_id)
        return self.success()
