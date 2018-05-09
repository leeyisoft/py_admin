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

from applications.core.settings_manager import settings
from applications.core.logger.client import SysLogger
from applications.core.cache import sys_config
from applications.core.decorators import required_permissions
from applications.core.utils.encrypter import RSAEncrypter
from applications.core.utils.hasher import check_password
from applications.core.utils.hasher import make_password

from applications.core.utils import Func
from applications.core.utils import FileUtil
from applications.core.utils import Uploader

from ..models.system import Member
from ..models.system import MemberOperationLog

from .common import CommonHandler


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
    @tornado.web.authenticated
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

class UploadAvatorHandler(CommonHandler):
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        """上传头像
        """
        user_id = self.current_user.get('uuid')
        next = self.get_argument('next', '')
        imgfile = self.request.files.get('file')

        # 判断上传文件大小
        size = int(self.request.headers.get('Content-Length'))
        if (size/1024)>80:
            return self.error('文件大小不能够超过80KB')

        # PIL 是 python中对图片进行操作的模块, 感兴趣可以去看一下
        from PIL import Image
        import io
        import os
        # print('imgfile', type(imgfile))
        for img in imgfile:
            print('img', type(img))
            # 对文件进行重命名
            param = Uploader.upload_img(img)
            return self.success(data=param)
            # print("param: ", param)
            # SysLogger.debug(str(param))
            # SysLogger.debug(img)
        # member = Member.Q.filter(Member.uuid==user_id).first()

        # if int(member.status)==0:
        #     return self.error('用户被“禁用”，请联系客服')
        # if check_password(nowpass, member.password) is not True:
        #     return self.error('当前密码错误')

        # params = {
        #     'password': make_password(password),
        #     'status': 1,
        # }
        # Member.Q.filter(Member.uuid==user_id).update(params)
        # Member.session.commit()
        return self.success(next=next)

class ActivateHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        """Home首页
        """
        user_id = self.current_user.get('uuid')
        token = self.get_argument('token', None)
        token2 = self.get_secure_cookie(self.token_key)
        if token and token2:
            token2 = str(token2, encoding='utf-8')
            token2 = token2.replace('\'', '"')
            token2 = json_decode(token2)
            account = token2.get('account', '')
            if not Member.check_email_activated(user_id, account) and token2.get('token', '')==token:
                # 激活用户Email
                params = {
                    'user_id': user_id,
                    'account': account,
                    'action': 'activate_email',
                    'ip': self.request.remote_ip,
                    'client': 'web',
                }
                MemberOperationLog.add_log(params)
                self.clear_cookie(self.token_key)

        member = Member.Q.filter(Member.uuid==user_id).first()
        params = {
            'member': member,
        }
        self.render('member/activate.html', **params)


class SendmailHandler(CommonHandler):
    @tornado.web.authenticated
    def activate_email(self, email):
        """激活邮箱发送邮件功能
        """
        if not Func.is_email(email):
            return self.error('Email格式不正确')

        uuid = self.current_user.get('uuid')
        member = Member.Q.filter(Member.uuid==uuid).first()

        if member.email_activated:
            return self.error('已经激活了，请不要重复操作')

        token = self.get_secure_cookie(self.token_key)
        if token:
            return self.error('邮件已发送，10分钟后重试')

        subject = '[%s]激活邮件' % sys_config('site_name')
        token = Func.uuid32()
        action_url = sys_config('site_url') + '/member/activate.html?token=' + token

        localnow = Func.local_now() + datetime.timedelta(minutes=10)
        params = {
            'username': member.username,
            'expires': str(localnow),
            'action_url': action_url,
            'action_tips': '立即激活邮箱',
        }
        tmpl = 'common/email_content.html'
        content = self.render_string(tmpl, **params)
        # print('content', content)
        Func.sendmail({'to_addr': email, 'subject':subject, 'content': content})
        save = {
            'token':token,
            'account': email,
            'username': member.username,
            'action':'email_reset_pwd',
        }
        expires = time.mktime(localnow.timetuple())
        self.set_secure_cookie(self.token_key, str(save), expires=expires)
        return self.success()

    def email_reset_pwd(self, email):
        """使用Email充值密码发送邮件功能
        """
        if not Func.is_email(email):
            return self.error('Email格式不正确')

        token = self.get_secure_cookie(self.token_key)
        if token:
            return self.error('邮件已发送，30分钟后重试')

        member = Member.Q.filter(Member.email==email).first()
        if member is None:
            return self.error('账户没有注册')
        if member.status==0:
            return self.error('账户被禁用')

        subject = '[%s]找回密码' % sys_config('site_name')
        token = Func.uuid32()
        action_url = sys_config('site_url') + '/passport/forget.html?token=' + token

        localnow = Func.local_now() + datetime.timedelta(minutes=30)
        params = {
            'username': member.username,
            'expires': str(localnow),
            'action_url': action_url,
            'action_tips': '立即重置密码',
        }
        tmpl = 'common/email_content.html'
        content = self.render_string(tmpl, **params)
        # print('content', content)
        Func.sendmail({'to_addr': email, 'subject':subject, 'content': content})
        save = {
            'token':token,
            'account': email,
            'username': member.username,
            'action':'email_reset_pwd',
        }
        expires = time.mktime(localnow.timetuple())
        self.set_secure_cookie(self.token_key, str(save), expires=expires)
        return self.success()

    def post(self, *args, **kwargs):
        """激活邮箱“写入数据库、发送邮件”
        """
        account = self.get_argument('account', '')
        action = self.get_argument('action', '')
        vercode = self.get_argument('vercode', '')
        if action=='activate_email':
            return self.activate_email(account)
        elif action=='email_reset_pwd':
            return self.email_reset_pwd(account)
        else:
            return self.error('未定义的操作')

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
