#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""
import tornado
from pyrestful.rest import JsonError
from pyrestful.rest import get
from pyrestful.rest import post

from applications.core.utils import sys_config
from applications.core.utils.encrypter import RSAEncrypter
from applications.core.utils.hasher import check_password
from applications.core.settings_manager import settings

from ..services.user import AdminUserService
from ..models import AdminUser
from .common import CommonHandler


class LoginHandler(CommonHandler):
    """docstring for Passport"""

    def __invalid_img_captcha(self, code):
        """ 图像验证码验证 不区分大小写"""
        valid_code = self.get_secure_cookie(settings.valid_code_key)
        valid_code = valid_code.decode('utf-8') if valid_code else ''
        return valid_code.lower()!=code.lower()

    def get(self, *args, **kwargs):
        next = self.get_argument('next', '')
        params = {
            'public_key': sys_config('sys_login_rsa_pub_key'),
            'rsa_encrypt': sys_config('login_pwd_rsa_encrypt'),
            'next': next,
            'message': '',
        }
        self.render('passport/login.html', **params)

    def post(self, *args, **kwargs):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        rsa_encrypt = self.get_argument('rsa_encrypt', '0')
        code = self.get_argument('code', '')

        if not username or not password or not rsa_encrypt or not code:
            return self.error('参数必须')

        test_verify_switch = sys_config('test_verify_switch')
        test_verify_switch = 1 if test_verify_switch else 0
        if int(test_verify_switch)==1:
            if self.__invalid_img_captcha(code):
                return self.error('验证码错误')

        if  int(rsa_encrypt) == 1:
            private_key = sys_config('sys_login_rsa_priv_key')
            password = RSAEncrypter.decrypt(password, private_key)
            if password==False:
                return self.error('密码错误')

        user = AdminUser.Q.filter(AdminUser.username == username).first()
        if user is None:
            return self.error('用户名或者密码错误')
        if check_password(password, user.password) is not True:
            return self.error('用户名或者密码错误')

        if int(user.status) == 0:
            return self.error('用户被“禁用”，请联系客服')

        AdminUserService.login_success(user, self)
        self.clear_cookie(settings.valid_code_key)
        data = {
            'username':user.username,
            'last_login_at':user.last_login_at,
            'login_count':user.login_count,
            'is_superadmin':self.super_role(),
        }
        return self.success('成功',data=data)

class LogoutHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        cache_key = self.get_secure_cookie(settings.admin_session_key)
        self.clear_cookie(cache_key)
        self.redirect(self.get_login_url())

class CaptchaHandler(CommonHandler):
    def get(self, *args, **kwargs):
        import io
        from applications.core.utils.image import create_validate_code
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
