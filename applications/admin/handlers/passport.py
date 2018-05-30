#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""

import tornado

from applications.core.utils.encrypter import RSAEncrypter
from applications.core.utils.hasher import check_password
from applications.core.utils.hasher import make_password
from applications.core.utils import Func
from applications.core.settings_manager import settings
from applications.core.logger.client import SysLogger
from applications.core.cache import sys_config

from ..models import User

from .common import CommonHandler


valid_code_key = 'f782d88f80e84779ab754accce47a62c'

class LoginHandler(CommonHandler):
    """docstring for Passport"""
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
        username = self.get_argument('username')
        next = self.get_argument('next', '')
        password = self.get_argument('password', '')
        rsa_encrypt = self.get_argument('rsa_encrypt', 0)

        if settings.login_pwd_rsa_encrypt and int(rsa_encrypt)==1 and len(password)>10:
            private_key = sys_config('sys_login_rsa_priv_key')
            password = RSAEncrypter.decrypt(password, private_key)

        user = User.Q.filter(User.username==username).first()
        if user is None:
            return self.error('用户名或者密码错误')
        if check_password(password, user.password) is not True:
            return self.error('用户名或者密码错误')

        if int(user.status)==0:
            return self.error('用户被“禁用”，请联系客服')

        User.login_success(user, self)
        self.clear_cookie(valid_code_key)


        return self.success(next=next)

class LogoutHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.clear_cookie(self.session_key)
        self.redirect(self.get_login_url())


class CaptchaHandler(CommonHandler):
    def get(self, *args, **kwargs):
        import io
        from applications.core.utils.image import create_validate_code
        #创建一个文件流
        imgio = io.BytesIO()
        #生成图片对象和对应字符串
        img, code = create_validate_code(size=(160, 38), font_size=32)
        self.set_secure_cookie(valid_code_key, code, expires_days=1)
        #将图片信息保存到文件流
        img.save(imgio, 'png')
        #返回图片
        self.set_header('Content-Type', 'image/png')
        self.write(imgio.getvalue())
        return self.finish()

    def post(self, *args, **kwargs):
        valid_code = self.get_argument('valid_code')
        if self.get_secure_cookie(valid_code_key)==valid_code:
            return self.success()
        else:
            return self.error(_('验证码错误'))
