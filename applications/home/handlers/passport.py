#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""
import json
import tornado
import time
import datetime

from tornado.escape import json_decode

from applications.core.utils.encrypter import RSAEncrypter
from applications.core.utils.hasher import check_password
from applications.core.utils.hasher import make_password
from applications.core.utils import Func

from applications.core.settings_manager import settings
from applications.core.logger.client import SysLogger
from applications.core.cache import sys_config

from ..models.system import Member
from ..models.system import MemberOperationLog

from .common import CommonHandler


valid_code_key = 'ab1195c6f0084b4f8b007d3aa7628a38'

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
        # self.show(self.get_template_path())
        self.render('passport/login.html', **params)

    def post(self, *args, **kwargs):
        account = self.get_argument('account', None)
        next = self.get_argument('next', '')
        password = self.get_argument('password', '')
        rsa_encrypt = self.get_argument('rsa_encrypt', 0)

        if settings.login_pwd_rsa_encrypt and int(rsa_encrypt)==1 and len(password)>10:
            private_key = sys_config('sys_login_rsa_priv_key')
            password = RSAEncrypter.decrypt(password, private_key)

        if not account:
            return self.error('账号不能够为空')

        if Func.is_mobile(account):
            member = Member.Q.filter(Member.mobile==account).first()
        elif Func.is_email(account):
            member = Member.Q.filter(Member.email==account).first()
        else:
            member = Member.Q.filter(Member.username==account).first()

        if member is None:
            return self.error('用户名或者密码错误')

        if int(member.status)==0:
            return self.error('用户被“禁用”，请联系客服')
        if check_password(password, member.password) is not True:
            return self.error('用户名或者密码错误')


        Member.login_success(member, self)

        self.clear_cookie(valid_code_key)

        return self.success(next=next)

class RegisterHandler(CommonHandler):
    """docstring for Passport"""
    def get(self, *args, **kwargs):
        next = self.get_argument('next', '')
        # self.show('home/login')
        params = {
            'public_key': sys_config('sys_login_rsa_pub_key'),
            'rsa_encrypt': sys_config('login_pwd_rsa_encrypt'),
            'xsrf_token': self.xsrf_token,
            'next': next,
            'message': '',
        }
        self.render('passport/register.html', **params)

    def post(self, *args, **kwargs):
        email = self.get_argument('email', None)
        mobile = self.get_argument('mobile', None)
        username = self.get_argument('username', None)
        next = self.get_argument('next', '')
        password = self.get_argument('password', None)
        repass = self.get_argument('repass', '')
        rsa_encrypt = self.get_argument('rsa_encrypt', 0)

        if settings.login_pwd_rsa_encrypt and int(rsa_encrypt)==1 and len(password)>10:
            private_key = sys_config('sys_login_rsa_priv_key')
            password = RSAEncrypter.decrypt(password, private_key)
            repass = RSAEncrypter.decrypt(repass, private_key)

        if not username:
            return self.error('用户名不能为空')

        if not password:
            return self.error('密码不能为空')

        if repass!=password:
            msg = '两次输入的密码不一致，请重新输入'
            msg = "%s, %s" %(password, repass)
            return self.error(msg)

        count = Member.Q.filter(Member.username==username).count()
        if count>0:
            return self.error('用户名已被占用')

        params = {
            'username': username,
            'password': make_password(password),
            'status': 1,
        }
        if email:
            params['email'] = email
            count = Member.Q.filter(Member.email==email).count()
            if count>0:
                return self.error('Email已被占用')
        if mobile:
            params['mobile'] = mobile
            count = Member.Q.filter(User.mobile==mobile).count()
            if count>0:
                return self.error('电话号码已被占用')

        member = Member(**params)
        Member.session.add(member)
        Member.session.commit()

        Member.login_success(member, self)
        return self.success(next=next)

class ForgetHandler(CommonHandler):
    """docstring for Passport"""
    def get(self, *args, **kwargs):

        token = self.get_argument('token', None)
        token2 = self.get_secure_cookie(self.token_key)
        params = {
            'public_key': sys_config('sys_login_rsa_pub_key'),
            'rsa_encrypt': sys_config('login_pwd_rsa_encrypt'),
            'token': token,
            'xsrf_token': self.xsrf_token,
            'reset_pwd': '1',
        }
        # print("token2: ", token2)
        if token and token2:
            token2 = str(token2, encoding='utf-8')
            token2 = token2.replace('\'', '"')
            token2 = json_decode(token2)

            action = token2.get('action', '')
            account = token2.get('account', '')
            if token2.get('token', '')==token:
                params['reset_pwd'] = '2'
                params['username'] = token2.get('username', '')
        self.render('passport/forget.html', **params)

    def post(self, *args, **kwargs):
        """重置密码
        """
        token = self.get_argument('token', None)
        next = self.get_argument('next', '')
        password = self.get_argument('password', None)
        repass = self.get_argument('repass', '')
        rsa_encrypt = self.get_argument('rsa_encrypt', 0)

        token2 = self.get_secure_cookie(self.token_key)
        if not(token and token2):
            return self.error('Token不存在或已经过期')

        token2 = str(token2, encoding='utf-8')
        token2 = token2.replace('\'', '"')
        token2 = json_decode(token2)

        action = token2.get('action', '')
        account = token2.get('account', '')
        # print('token2 ', token2.get('token', ''), token)
        if token2.get('token', '')!=token:
            return self.error('Token不匹配')

        if not password:
            return self.error('新密码不能为空')

        if settings.login_pwd_rsa_encrypt and int(rsa_encrypt)==1 and len(password)>10:
            private_key = sys_config('sys_login_rsa_priv_key')
            password = RSAEncrypter.decrypt(password, private_key)
            repass = RSAEncrypter.decrypt(repass, private_key)

        if repass!=password:
            msg = '两次输入的密码不一致，请重新输入'
            msg = "%s, %s" %(password, repass)
            return self.error(msg)

        member = None
        if action=='email_reset_pwd':
            member = Member.Q.filter(Member.email==account).first()
        else:
            return self.error('不支持的action')

        if member is None:
            return self.error('用户不存在')

        if int(member.status)==0:
            return self.error('用户被“禁用”，请联系客服')
        user_id = member.uuid
        params = {
            'password': make_password(password),
        }
        Member.Q.filter(Member.uuid==user_id).update(params)
        Member.session.commit()

        params = {
            'user_id': user_id,
            'account': account,
            'action': 'email_reset_pwd',
            'ip': self.request.remote_ip,
            'client': 'web',
        }
        MemberOperationLog.add_log(params)

        self.clear_cookie(self.token_key)
        return self.success(next=next)


class LogoutHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.clear_cookie(self.user_session_key)
        self.redirect("/passport/login")

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
        img.save(imgio, 'GIF')
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
