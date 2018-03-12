#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""

from applications.core.encrypter import RSAEncrypter
from applications.core.settings_manager import settings
from applications.core.logger.client import SysLogger

from applications.core.models import Config
from applications.core.models import User
from applications.core.cache import sys_config
from applications.core.utils import required_login

from applications.admin.handlers.common import BaseHandler


class LoginHandler(BaseHandler):
    """docstring for Passport"""
    def get(self, *args, **kwargs):
        args = {
            'public_key': sys_config('sys_login_rsa_pub_key'),
            'rsa_encrypt': sys_config('login_pwd_rsa_encrypt'),
        }
        self.render('passport/login.html', **args)

    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password', '')
        rsa_encrypt = self.get_argument('rsa_encrypt', 0)
        # print('password ', password)
        # print('rsa_encrypt ', rsa_encrypt)
        if settings.login_pwd_rsa_encrypt and int(rsa_encrypt)==1 and len(password)>10:
            private_key = '/Users/leeyi/chanrongdai/eam/py_admin/datas/private.pem'
            password = RSAEncrypter.decrypt(password, private_key)

        # 给密码加密
        password = password

        user = User.Q.filter(User.username==username).filter(User.password==password).first()
        if user is None:
            return self.error('用户名或者密码错误')

        if int(user.status)==0:
            return self.error('用户被锁定，请联系客服')

        print('user', type(user))
        self.session[self.user_session_key] = user
        self.session.set_expire(3600 * 24 * 30) #30天
        # self.set_secure_cookie("user",)
        # self.redirect("/")
        return self.success()

class LogoutHandler(BaseHandler):
    """docstring for Passport"""
    @required_login
    def get(self, *args, **kwargs):
        if self.user_session_key in self.session:
            del self.session[self.user_session_key]
        self.redirect("/admin/login.html")
