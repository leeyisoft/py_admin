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
from trest.config import settings
from trest.utils.hasher import check_password
from trest.utils.encrypter import RSAEncrypter

from applications.common.utils import sys_config
from applications.admin.utils import required_permissions

from ..services.role import RoleService
from ..services.user import AdminUserService
from ..services.menu import AdminMenuService
from ..models import Role
from ..models import AdminUser
from .common import CommonHandler


class UserHandler(CommonHandler):
    """docstring for Passport"""
    @delete('/admin/user/(?P<uid>\d*)')
    @tornado.web.authenticated
    @required_permissions()
    def user_delete(self, uid):
        """删除用户
        """
        AdminUserService.delete_data(uid)
        return self.success()

    @get('/admin/user')
    @tornado.web.authenticated
    @required_permissions()
    def user_get(self, *args, **kwargs):
        """管理员列表"""
        limit = self.get_argument('limit', 10)
        page = self.get_argument('page', 1)

        pagelist_obj = AdminUserService.get_data(limit, page)
        items2=[]
        for item in pagelist_obj.items:
            val = item.as_dict()
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

    @get('/admin/user/add')
    @tornado.web.authenticated
    def user_add(self, *args, **kwargs):
        role_id = settings.DEFAULT_ROLE_ID
        menu_list = AdminMenuService.menu_list(1)
        params = {
            'status':1,
            'role_id':role_id,
            'username':'',
            'mobile': '',
            'email': '',
        }
        user = AdminUser(**params)

        data_info = user.as_dict()
        try:
            data_info['permission'] = json.loads(user.permission)
        except Exception as e:
            data_info['permission'] = []

        params = {
            'user': user,
            'role_option': Role.option_html(role_id),
            'menu_list': menu_list,
            'data_info': data_info,
            'public_key': sys_config('sys_login_rsa_pub_key'),
            'rsa_encrypt': sys_config('login_pwd_rsa_encrypt'),
        }
        self.render('user/add.html', **params)

    @post('/admin/user')
    @tornado.web.authenticated
    @required_permissions()
    def user_post(self):
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

    @get('/admin/user/edit.html')
    @tornado.web.authenticated
    def user_edit(self, *args, **kwargs):
        id = self.get_argument('id', None)

        menu_list = AdminMenuService.menu_list(1)
        user = AdminUser.Q.filter(AdminUser.id==id).first()


        user.mobile = user.mobile if user.mobile else ''
        user.email = user.email if user.email else ''

        data_info = user.as_dict()
        # SysLogger.debug(data_info)
        try:
            data_info['permission'] = json.loads(user.permission)
        except Exception as e:
            data_info['permission'] = []

        params = {
            'user': user,
            'role_option': Role.option_html(user.role_id),
            'menu_list': menu_list,
            'data_info': data_info,
            'public_key': sys_config('sys_login_rsa_pub_key'),
            'rsa_encrypt': sys_config('login_pwd_rsa_encrypt'),
        }
        self.render('user/edit.html', **params)

    @put('/admin/user')
    @tornado.web.authenticated
    @required_permissions()
    def user_put(self):
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
            raise JsonError('Edit用户ID不能为空')
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
        return self.success()

    @get('/admin/valid_role')
    def valid_role(self):
        """获取有效的角色"""
        data = RoleService.get_valid_role()
        return self.success(data=data)

class UnlockUserHandler(CommonHandler):
    @put('/admin/user/unlocked')
    @tornado.web.authenticated
    def unlock_user(self):
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

class UserChangePwdHandler(CommonHandler):
    @put('/admin/user/change_pwd')
    @tornado.web.authenticated
    @required_permissions()
    def use_change_pwd(self):
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
