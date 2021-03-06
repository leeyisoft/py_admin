#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""

from tornado.escape import json_decode

from trest.router import get
from trest.router import put
from trest.router import post
from trest.router import delete
from trest.exception import JsonError
from trest.config import settings
from trest.utils.hasher import check_password
from trest.utils.encrypter import RSAEncrypter

from applications.common.utils import sys_config
from applications.common.models.admin_user import AdminUser

from applications.admin.utils import admin_required_login

from applications.admin.services.admin_user import AdminUserService
from .common import CommonHandler


class AdminLoginHandler(CommonHandler):
    """docstring for Passport"""

    def __invalid_img_captcha(self, code):
        """ 图像验证码验证 不区分大小写"""
        valid_code = self.get_secure_cookie(settings.valid_code_key)
        valid_code = valid_code.decode('utf-8') if valid_code else ''
        return valid_code.lower()!=code.lower()

    @post('login')
    def login_post(self, *args, **kwargs):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        code = self.get_argument('code', '')
        # print('login_post self.request.arguments ', type(self.request.arguments), self.request.arguments)
        if not username:
            post_data = self.request.body.decode('utf-8')
            try:
                post_data = json_decode(post_data)
                username = post_data.get('username', '')
                password = post_data.get('password', '')
                code = post_data.get('code', '')
            except Exception as e:
                pass
            # print('login_post data ', type(post_data), post_data)
        # print('login_post ', self.request.headers)
        if not username or not password:
            raise JsonError('参数必须')

        test_verify_switch = sys_config('test_verify_switch')
        test_verify_switch = 1 if test_verify_switch else 0

        if int(test_verify_switch)==1:
            if self.__invalid_img_captcha(code):
                raise JsonError('验证码错误')

        rsa_encrypt = sys_config('login_pwd_rsa_encrypt')
        if  int(rsa_encrypt) == 1:
            private_key = sys_config('login_rsa_priv_key')
            password = RSAEncrypter.decrypt(password, private_key)
            if password==False:
                raise JsonError('密码错误')

        user = AdminUser.Q.filter(AdminUser.username == username).first()
        if user is None:
            raise JsonError('用户名或者密码错误')
        if check_password(password, user.password) is not True:
            raise JsonError('用户名或者密码错误')

        if int(user.status) == 0:
            raise JsonError('用户被“禁用”，请联系客服')

        AdminUserService.login_success(user, self)
        self.clear_cookie(settings.valid_code_key)
        data = {
            'username':user.username,
            'last_login_at':user.last_login_at,
            'login_count':user.login_count,
            'is_superadmin':self.super_role(),
            'token': 'token'
        }
        return self.success('成功',data=data)


class AdminLogoutHandler(CommonHandler):
    @post('logout')
    @admin_required_login
    def admin_logout_post(self):
        self.clear_cookie(settings.admin_session_key)
        self.set_cookie('_xsrf', self.xsrf_token.decode("utf-8"))
        return self.success()

class CaptchaHandler(CommonHandler):
    @get('captcha/?(.png)?')
    def get(self, *args, **kwargs):
        import io
        from applications.common.utils import create_validate_code
        #创建一个文件流
        imgio = io.BytesIO()
        #生成图片对象和对应字符串
        img, code = create_validate_code(size=(160, 38), font_size=32)
        self.set_secure_cookie(settings.valid_code_key, code, expires_days=1)
        #将图片信息保存到文件流
        img.save(imgio, 'png')
        #返回图片
        self.set_header('Content-Type', 'image/png')
        self.write(imgio.getvalue())
        return self.finish()
