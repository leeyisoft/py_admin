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

from trest.config import settings
from trest.logger.client import SysLogger
from applications.common.utils import sys_config
from applications.admin.utils import required_permissions
from trest.models import Attach
from trest.utils.encrypter import RSAEncrypter
from trest.utils.encrypter import aes_encrypt
from trest.utils.hasher import check_password
from trest.utils.hasher import make_password

from trest.utils import Func
from trest.utils import FileUtil
from trest.utils import Uploader

from ..models import Member
from ..models import MemberOperationLog

from .common import CommonHandler


class IndexHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        """Home首页
        """
        params = {
            'active': {'index':'layui-this'},
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

class UploadHandler(CommonHandler):
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        """上传图片"""
        user_id = self.current_user.get('id')

        next = self.get_argument('next', '')
        imgfile = self.request.files.get('file')
        action = self.get_argument('action', None)
        path = self.get_argument('path', 'default_path')

        if action not in ['alipay', 'wechatpay', 'avatar']:
            return self.error('不支持的action')

        for img in imgfile:
            print('img', type(img))
            # 对文件进行重命名
            file_ext = FileUtil.file_ext(img['filename'])
            path = '%s/' % path
            save_name = img['filename']
            file_md5 = Func.md5(img['body'])
            if action=='avatar':
                save_name = '%s.%s' %(user_id, file_ext)
            elif action in ['alipay', 'wechatpay']:
                save_name = '%s_%s.%s' %(user_id, action, file_ext)
            try:
                param = Uploader.upload_img(file_md5, img, save_name, path, {
                    'user_id': user_id,
                    'ip': self.request.remote_ip,
                })
                return self.success(data=param)
            except Exception as e:
                if settings.debug:
                    raise e
                SysLogger.error(e)
                return self.error('上传失败')

        return self.error('参数错误')

class SetHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        """Home首页
        """
        user_id = self.current_user.get('id')
        member = Member.Q.filter(Member.id==user_id).first()
        data_info = member.as_dict()
        params = {
            'member': member,
            'data_info': data_info,
            'public_key': sys_config('login_rsa_pub_key'),
            'rsa_encrypt': sys_config('login_pwd_rsa_encrypt'),
            'active': {'set':'layui-this'},
        }
        self.render('member/set.html', **params)

    @tornado.web.authenticated
    def put(self, *args, **kwargs):
        user_id = self.current_user.get('id')
        username = self.get_argument('username', None)
        email = self.get_argument('email', None)
        mobile = self.get_argument('mobile', None)
        sex = self.get_argument('sex', None)
        sign = self.get_argument('sign', None)
        avatar = self.get_argument('avatar', None)
        file_md5 = self.get_argument('file_md5', None)

        params = {}

        if username:
            params['username'] = username
            count = Member.Q.filter(Member.id!=user_id).filter(Member.username==username).count()
            if count>0:
                return self.error('用户名已被占用')

        if mobile:
            params['mobile'] = mobile
            count = Member.Q.filter(Member.id!=user_id).filter(Member.mobile==mobile).count()
            if count>0:
                return self.error('电话号码已被占用')
        if email:
            params['email'] = email
            count = Member.Q.filter(Member.id!=user_id).filter(Member.email==email).count()
            if count>0:
                return self.error('Email已被占用')

        if sex:
            params['sex'] = sex
        if sign is not None:
            params['sign'] = sign

        if avatar and file_md5:
            params['avatar'] = avatar
            member = Member.Q.filter(Member.id==user_id).first()

            if avatar!=member.avatar:
                Attach.remove_avatar(user_id, member.avatar)

            query = "REPLACE INTO `sys_attach_related` (`file_md5`, `related_table`, `related_id`, `ip`, `created_at`) VALUES ('%s', '%s', '%d', '%s', '%s')" % (
                file_md5,
                'member',
                user_id,
                self.request.remote_ip,
                utime.timestamp(3),
            )
            # print('query ', query )
            Member.session.execute(query)
        Member.Q.filter(Member.id==user_id).update(params)
        Member.session.commit()

        # 设置登录用户cookie信息
        member = Member.Q.filter(Member.id==user_id).first()
        self.set_curent_user(member)

        return self.success()

class ResetPasswordHandler(CommonHandler):
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        """重置密码
        """
        user_id = self.current_user.get('id')
        next = self.get_argument('next', '')
        nowpass = self.get_argument('nowpass', None)
        password = self.get_argument('password', None)
        repass = self.get_argument('repass', '')
        rsa_encrypt = self.get_argument('rsa_encrypt', 0)

        if settings.login_pwd_rsa_encrypt and int(rsa_encrypt)==1 and len(password)>10:
            private_key = sys_config('login_rsa_priv_key')
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

        member = Member.Q.filter(Member.id==user_id).first()

        if int(member.status)==0:
            return self.error('用户被“禁用”，请联系客服')
        if check_password(nowpass, member.password) is not True:
            return self.error('当前密码错误')

        params = {
            'password': make_password(password),
            'status': 1,
        }
        Member.Q.filter(Member.id==user_id).update(params)
        Member.session.commit()
        return self.success(next=next)

class ActivateHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        """Home首页
        """
        user_id = self.current_user.get('id')
        token = self.get_argument('token', None)
        token2 = self.get_secure_cookie(settings.token_key)
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
                self.clear_cookie(settings.token_key)

        member = Member.Q.filter(Member.id==user_id).first()
        params = {
            'member': member,
            'active': {'set':'layui-this'},
        }
        self.render('member/activate.html', **params)

class SendmailHandler(CommonHandler):
    @tornado.web.authenticated
    def activate_email(self, email):
        """激活邮箱发送邮件功能
        """
        if not Func.is_email(email):
            return self.error('Email格式不正确')

        user_id = self.current_user.get('id')
        member = Member.Q.filter(Member.id==user_id).first()

        if member.email_activated:
            return self.error('已经激活了，请不要重复操作')

        token = self.get_secure_cookie(settings.token_key)
        if token:
            return self.error('邮件已发送，10分钟后重试')

        self.success()

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
        self.set_secure_cookie(settings.token_key, str(save), expires=expires)
        return

    def email_reset_pwd(self, email):
        """使用Email充值密码发送邮件功能
        """
        if not Func.is_email(email):
            return self.error('Email格式不正确')

        token = self.get_secure_cookie(settings.token_key)
        if token:
            return self.error('邮件已发送，30分钟后重试')

        member = Member.Q.filter(Member.email==email).first()
        if member is None:
            return self.error('账户没有注册')
        if member.status==0:
            return self.error('账户被禁用')

        self.success()

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
        self.set_secure_cookie(settings.token_key, str(save), expires=expires)
        return

    def post(self, *args, **kwargs):
        """激活邮箱“写入数据库、发送邮件”
        """
        account = self.get_argument('account', '')
        action = self.get_argument('action', '')
        code = self.get_argument('code', '')
        _ = self.locale.translate

        if self.invalid_img_captcha(code):
            return self.error(_('验证码错误'))

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
            'active': {'message':'layui-this'},
        }
        self.render('member/message.html', **params)

class InviteHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        """邀请好友
        """
        user_id = self.current_user.get('id')
        referrer = aes_encrypt(user_id, prefix='')
        reg_uri = '%s://%s/%s%s' %(
            self.request.protocol,
            self.request.host,
            'passport/reg.html?referrer=',
            referrer,
        )
        reg_uri_mobile = reg_uri
        if 'mobile' in settings.INSTALLED_APPS:
            reg_uri_mobile = '%s://%s/%s%s' %(
                self.request.protocol,
                self.request.host,
                'mobile/reg.html?referrer=',
                referrer,
            )

        query = Member.Q
        query = query.filter(Member.ref_user_id==user_id)
        query = query.filter(Member.status==1)
        query = query.filter(Member.deleted==0)
        member_li = query.order_by(Member.created_at.desc()).all()

        from trest.utils.image import qrcode_base64_img
        logo = settings.STATIC_PATH+'/image/logo.png'
        qrcode_img = qrcode_base64_img(reg_uri_mobile, logo)

        params = {
            'reg_uri': reg_uri,
            'qrcode_img': qrcode_img,
            'member_li': member_li,
            'active': {'invite':'layui-this'},
        }
        self.render('member/invite.html', **params)

class MemberUnlockedHandler(CommonHandler):
    @tornado.web.authenticated
    @required_permissions()
    def post(self, *args, **kwargs):
        password = self.get_argument('password', None)
        if not password:
            return self.error('请输入密码')

        return self.success()
