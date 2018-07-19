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
from applications.core.utils.encrypter import aes_decrypt
from applications.core.utils.encrypter import aes_encrypt

from applications.core.settings_manager import settings
from applications.core.logger.client import SysLogger
from applications.core.cache import sys_config

from ..models import Member
from ..models import MemberOperationLog

from .common import CommonHandler


class LoginHandler(CommonHandler):
    """docstring for Passport"""
    def get(self, *args, **kwargs):
        next = self.get_argument('next', '')
        if self.current_user:
            next = next if next else '/member/index'
            self.redirect(next)

        params = {
            'public_key': sys_config('sys_login_rsa_pub_key'),
            'rsa_encrypt': sys_config('login_pwd_rsa_encrypt'),
            'next': next,
            'message': '',
        }
        # self.show(self.get_template_path())
        self.render('passport/login.html', **params)

    def post(self, *args, **kwargs):
        next = self.get_argument('next', '')
        account = self.get_argument('account', None)
        password = self.get_argument('password', '')
        rsa_encrypt = self.get_argument('rsa_encrypt', 0)
        code = self.get_argument('code', '')
        _ = self.locale.translate

        if self.invalid_img_captcha(code):
            return self.error(_('验证码错误'))

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

        self.clear_cookie(settings.valid_code_key)

        return self.success(next=next)

class RegisterHandler(CommonHandler):
    """docstring for Passport"""
    def get(self, *args, **kwargs):
        next = self.get_argument('next', '')
        referrer = self.get_argument('referrer', '')
        # print(aes_encrypt('de001cb8f0404944994e14f20bf76a02', prefix=''))
        params = {
            'public_key': sys_config('sys_login_rsa_pub_key'),
            'rsa_encrypt': sys_config('login_pwd_rsa_encrypt'),
            'next': next,
            'referrer_name': '',
            'ref_user_id': '',
        }

        if referrer:
            ref_info = {}
            try:
                ref_user_id = aes_decrypt(referrer, prefix='')
                ref_info = Member.get_info(ref_user_id, 'username')
                params['referrer_name'] = ref_info.get('username', '')
                params['ref_user_id'] = ref_user_id
            except Exception as e:
                pass

        # self.show('home/login')
        self.render('passport/register.html', **params)

    def post(self, *args, **kwargs):
        next = self.get_argument('next', '')
        email = self.get_argument('email', None)
        mobile = self.get_argument('mobile', None)
        username = self.get_argument('username', None)
        sex = self.get_argument('sex', None)
        password = self.get_argument('password', None)
        repass = self.get_argument('repass', '')
        rsa_encrypt = self.get_argument('rsa_encrypt', 0)
        ref_user_id = self.get_argument('ref_user_id', '')
        code = self.get_argument('code', '')
        _ = self.locale.translate

        if self.invalid_img_captcha(code):
            return self.error(_('验证码错误'))

        if not email:
            return self.error('Email不能为空')

        if not password:
            return self.error('密码不能为空')

        if settings.login_pwd_rsa_encrypt and int(rsa_encrypt)==1 and len(password)>10:
            private_key = sys_config('sys_login_rsa_priv_key')
            password = RSAEncrypter.decrypt(password, private_key)
            repass = RSAEncrypter.decrypt(repass, private_key)

        if repass!=password:
            msg = '两次输入的密码不一致，请重新输入'
            msg = "%s, %s" %(password, repass)
            return self.error(msg)

        count = Member.Q.filter(Member.username==username).count()
        if count>0:
            return self.error('用户名已被占用')

        client = 'web'
        params = {
            'username': username,
            'password': make_password(password),
            'status': 1,
            'avatar': 'image/default_avatar.jpg',
            'register_ip': self.request.remote_ip,
            'register_client': client,
        }
        if email:
            params['email'] = email
            count = Member.Q.filter(Member.email==email).count()
            if count>0:
                return self.error('Email已被占用')
        if mobile:
            if not Func.mobile(mobile):
                return self.error('电话号码格式有误')
            params['mobile'] = mobile
            count = Member.Q.filter(User.mobile==mobile).count()
            if count>0:
                return self.error('电话号码已被占用')
        if sex:
            params['sex'] = sex
        if ref_user_id:
            params['ref_user_id'] = ref_user_id

        (code, member) = Member.register(params)
        if code==0:
            Member.login_success(member, self, client=client)
            return self.success(next=next)
        else:
            return self.error(member)

class ForgetHandler(CommonHandler):
    """docstring for Passport"""
    def get(self, *args, **kwargs):
        token = self.get_argument('token', None)
        token2 = self.get_secure_cookie(settings.token_key)

        params = {
            'public_key': sys_config('sys_login_rsa_pub_key'),
            'rsa_encrypt': sys_config('login_pwd_rsa_encrypt'),
            'token': token,
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
        code = self.get_argument('code', '')
        _ = self.locale.translate

        if self.invalid_img_captcha(code):
            return self.error(_('验证码错误'))

        token2 = self.get_secure_cookie(settings.token_key)
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
        user_id = member.id
        params = {
            'password': make_password(password),
        }
        Member.Q.filter(Member.id==user_id).update(params)
        Member.session.commit()

        params = {
            'user_id': user_id,
            'account': account,
            'action': 'email_reset_pwd',
            'ip': self.request.remote_ip,
            'client': 'web',
        }
        MemberOperationLog.add_log(params)

        self.clear_cookie(settings.token_key)
        return self.success(next=next)


class LogoutHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.clear_cookie(settings.front_session_key)
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
        img.save(imgio, 'GIF')
        #返回图片
        self.set_header('Content-Type', 'image/png')
        self.write(imgio.getvalue())
        return self.finish()
