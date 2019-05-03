#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""

import json
import tornado

from pyrestful.rest import JsonError
from pyrestful.rest import get
from pyrestful.rest import post
from pyrestful.rest import delete
from pyrestful.rest import put

from applications.core.utils import sys_config
from applications.core.decorators import required_permissions
from applications.core.utils.encrypter import RSAEncrypter
from applications.core.utils.hasher import check_password
from applications.admin.services.role import RoleService
from applications.core.settings_manager import settings

from ..services.user import AdminUserService
from ..models import AdminUser
from .common import CommonHandler


class UserHandler(CommonHandler):
    """docstring for Passport"""
    @delete('/admin/user', _catch_fire=settings.debug)
    @tornado.web.authenticated
    @required_permissions('admin:user:delete')
    def delete(self):
        """删除用户
        """
        uid = self.get_argument('user_id', None)
        AdminUserService.delete_data(uid)
        return self.success()

    @post('/admin/user/unlocked', _catch_fire=settings.debug)
    @tornado.web.authenticated
    def unlocked(self):
        """锁屏解锁"""
        password = self.get_argument('password', None)

        if not password:
            return self.error('请输入密码')

        is_rsa=sys_config('login_pwd_rsa_encrypt')
        if  int(is_rsa) == 1:
            private_key = sys_config('sys_login_rsa_priv_key')
            try:
                password = RSAEncrypter.decrypt(password, private_key)
            except Exception:
                return self.error(msg='签名失败',code=11)
        user_info=self.get_current_user()
        check=AdminUser.Q.filter(AdminUser.id == user_info['id']).first()
        if check is None:
            return self.error('用户信息出错')

        if check_password(password,check.password)==False:
            return self.error('密码错误')

        return self.success()


    @get('/admin/user', _catch_fire=settings.debug)
    @tornado.web.authenticated
    @required_permissions('admin:user:index')
    def index(self):
        """管理员列表"""
        limit = self.get_argument('limit', 10)
        page = self.get_argument('page', 1)

        pagelist_obj = AdminUserService.get_data(limit, page)
        items2=[]
        for config in pagelist_obj.items:
            val=config.as_dict()
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

    @post('/admin/user', _catch_fire=settings.debug)
    @tornado.web.authenticated
    @required_permissions('admin:user:add')
    def add(self):
        """新增管理员"""
        role_id = self.get_argument('role_id', None)
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        email = self.get_argument('email', None)
        mobile = self.get_argument('mobile', None)
        status = self.get_argument('status', '1')
        permission = self.get_argument('permission',[])
        rsa_encrypt = self.get_argument('rsa_encrypt',1)

        if not username:
            return self.error('用户名不能为空')
        if not password:
            return self.error('密码不能为空')
        user = {
            'status': status,
            'username': username,
            'password': password,
            'mobile': mobile,
            'email': email,
            'permission':permission,
            'role_id':role_id
        }

        AdminUserService.save_data(user, rsa_encrypt, None)
        return self.success()

    @put('/admin/user',_catch_fire=settings.debug)
    @tornado.web.authenticated
    @required_permissions('admin:user:edit')
    def edit(self):
        role_id = self.get_argument('role_id', None)
        uid = self.get_argument('user_id', None)
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        rsa_encrypt = self.get_argument('rsa_encrypt', '0')
        email = self.get_argument('email', None)
        mobile = self.get_argument('mobile', None)
        status = self.get_argument('status', '0')
        permission = self.get_argument('permission',[])

        if not uid:
            raise JsonError('用户ID不能为空')
        user = {
            'id': uid,
            'status': status,
            'username': username,
            'mobile': mobile,
            'email': email
        }
        user['permission'] = '[]'
        try:
            user['permission'] = json.dumps(permission)
        except Exception as e:
            pass
        if role_id:
            user['role_id'] = role_id
        AdminUserService.save_data(user, rsa_encrypt, uid)
        return self.success(data=resdata)

    @get('/admin/valid_role')
    def valid_role(self):
        """获取有效的角色"""
        data = RoleService.get_valid_role()
        return self.success(data=data)


    @put('/admin/user/change_pwd',_catch_fire=settings.debug)
    @tornado.web.authenticated
    @required_permissions('admin:user:change_pwd')
    def change_pwd(self):
        """
        修改密码
        :return:
        """
        password=self.get_argument('password',None)
        rsa_encrypt=self.get_argument('rsa_encrypt',None)
        admin_id=self.get_argument('admin_id',None)
        if password is None or rsa_encrypt is None or admin_id is None:
            return self.error('参数必须')
        check=AdminUser.Q.filter(AdminUser.id == admin_id).first()
        if check is None:
            return self.error('参数无效')
        user={
            'password':password
        }
        AdminUserService.change_pwd(user, rsa_encrypt, admin_id)
        return self.success()
