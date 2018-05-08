#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""

import json
import tornado
import time

from tornado.escape import json_decode

from applications.core.settings_manager import settings
from applications.core.logger.client import SysLogger
from applications.core.cache import sys_config
from applications.core.decorators import required_permissions
from applications.core.utils.encrypter import RSAEncrypter
from applications.core.utils.hasher import check_password
from applications.core.utils.hasher import make_password
from applications.core.utils import is_email
from applications.core.utils import sendmail
from applications.core.utils import uuid32

from ..models.system import Member
from ..models.system import MemberEmailActivateLog

from .common import CommonHandler


activate_email_token_key = 'c17a6633e5e64f00bfc93534cae80a2b'

class IndexHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        """Home首页
        """
        params = {
        }
        self.render('member/index.html', **params)

class HomeHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        """Home首页
        """
        params = {
        }
        self.render('member/home.html', **params)

class SetHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        """Home首页
        """
        uuid = self.current_user.get('uuid')
        member = Member.Q.filter(Member.uuid==uuid).first()
        data_info = member.as_dict()
        params = {
            'member': member,
            'data_info': data_info,
            'public_key': sys_config('sys_login_rsa_pub_key'),
            'rsa_encrypt': sys_config('login_pwd_rsa_encrypt'),
        }
        self.render('member/set.html', **params)


    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        uuid = self.current_user.get('uuid')
        username = self.get_argument('username', None)
        email = self.get_argument('email', None)
        mobile = self.get_argument('mobile', None)
        sex = self.get_argument('sex', 'HIDE')
        sign = self.get_argument('sign', '')

        params = {
            'sex': sex,
            'sign': sign,
        }
        if username:
            params['username'] = username
            count = Member.Q.filter(Member.uuid!=uuid).filter(Member.username==username).count()
            if count>0:
                return self.error('用户名已被占用')

        if mobile:
            params['mobile'] = mobile
            count = Member.Q.filter(Member.uuid!=uuid).filter(Member.mobile==mobile).count()
            if count>0:
                return self.error('电话号码已被占用')
        if email:
            params['email'] = email
            count = Member.Q.filter(Member.uuid!=uuid).filter(Member.email==email).count()
            if count>0:
                return self.error('Email已被占用')

        Member.Q.filter(Member.uuid==uuid).update(params)
        Member.session.commit()

        return self.success()


class ResetPasswordHandler(CommonHandler):
    def post(self, *args, **kwargs):
        """重置密码
        """
        user_id = self.current_user.get('uuid')
        next = self.get_argument('next', '')
        nowpass = self.get_argument('nowpass', None)
        password = self.get_argument('password', None)
        repass = self.get_argument('repass', '')
        rsa_encrypt = self.get_argument('rsa_encrypt', 0)

        if settings.login_pwd_rsa_encrypt and int(rsa_encrypt)==1 and len(password)>10:
            private_key = sys_config('sys_login_rsa_priv_key')
            nowpass = RSAEncrypter.decrypt(nowpass, private_key)
            password = RSAEncrypter.decrypt(password, private_key)
            repass = RSAEncrypter.decrypt(repass, private_key)

        if not nowpass:
            return self.error('当前密码不能够为空')

        if not password:
            return self.error('新密码不能为空')

        if repass!=password:
            msg = '两次输入的密码不一致，请重新输入'
            msg = "%s, %s" %(password, repass)
            return self.error(msg)

        member = Member.Q.filter(Member.uuid==user_id).first()

        if int(member.status)==0:
            return self.error('用户被“禁用”，请联系客服')
        if check_password(nowpass, member.password) is not True:
            return self.error('当前密码错误')

        params = {
            'password': make_password(password),
            'status': 1,
        }
        Member.Q.filter(Member.uuid==user_id).update(params)
        Member.session.commit()
        return self.success(next=next)


class ActivateHandler(CommonHandler):

    """docstring for Passport"""
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        """Home首页
        """
        user_id = self.current_user.get('uuid')
        token = self.get_argument('token', None)
        token2 = self.get_secure_cookie(activate_email_token_key)
        if token and token2:
            token2 = str(token2, encoding='utf-8')
            token2 = token2.replace('\'', '"')
            token2 = json_decode(token2)
            email = token2.get('email', '')
            if not Member.check_email_activated(user_id, email) and token2.get('token', '')==token:
                # 激活用户Email
                params = {
                    'user_id': user_id,
                    'email': email,
                    'ip': self.request.remote_ip,
                    'client': 'web'
                }
                MemberEmailActivateLog.activated_email(params)
                self.clear_cookie(activate_email_token_key)

        member = Member.Q.filter(Member.uuid==user_id).first()
        params = {
            'member': member,
        }
        self.render('member/activate.html', **params)


class SendmailHandler(CommonHandler):
    def activate_email(self, email):
        """激活邮箱发送邮件功能
        """
        if not is_email(email):
            return self.error('Email格式不正确')

        uuid = self.current_user.get('uuid')
        member = Member.Q.filter(Member.uuid==uuid).first()

        if member.email_activated:
            return self.error('已经激活了，请不要重复操作')

        token = self.get_secure_cookie(activate_email_token_key)
        if token:
            return self.error('邮件已发送，10分钟后重试')

        subject = '[%s]激活邮件' % sys_config('site_name')
        token = uuid32()
        activate_url = sys_config('site_url') + '/member/activate.html?token=' + token
        params = {'username': member.username, 'activate_url': activate_url}
        tmpl = 'common/activate_email_content.html'
        content = self.render_string(tmpl, **params)
        # print('content', content)
        sendmail({'to_addr': email, 'subject':subject, 'content': content})

        expires = time.time() + 600
        save = {'token':token, 'email': email}
        self.set_secure_cookie(activate_email_token_key, str(save), expires=expires)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        """激活邮箱“写入数据库、发送邮件”
        """
        email = self.get_argument('email', '')
        send_type = self.get_argument('type', '')
        if send_type=='activate_email':
            return self.activate_email(email)
        else:
            return self.error('未定义的操作')
        return self.success()

class MessageHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        """Home首页
        """
        params = {
        }
        self.render('member/message.html', **params)

class MemberUnlockedHandler(CommonHandler):
    @tornado.web.authenticated
    @required_permissions('admin:user:unlocked')
    def post(self, *args, **kwargs):
        password = self.get_argument('password', None)
        if not password:
            return self.error('请输入密码')

        return self.success()
