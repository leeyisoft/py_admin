#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""后台会员管理

[description]
"""

import json
import tornado

from applications.core.settings_manager import settings
from applications.core.logger.client import SysLogger
from applications.core.cache import sys_config
from applications.core.decorators import required_permissions
from applications.core.utils.encrypter import RSAEncrypter
from applications.core.utils.hasher import make_password
from applications.core.utils import Func

from ..models import Member
from ..models import Role
from ..models import AdminMenu

from .common import CommonHandler


class MemberHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    @required_permissions('admin:member:index')
    def get(self, *args, **kwargs):
        """后台首页
        """
        # return self.show('<script type="text/javascript">alert(1)</script>')
        params = {
        }
        self.render('member/index.html', **params)

    @tornado.web.authenticated
    @required_permissions('admin:member:delete')
    def delete(self, *args, **kwargs):
        """删除用户
        """
        # return self.show('<script type="text/javascript">alert(1)</script>')
        uuid = self.get_argument('uuid', None)

        Member.Q.filter(Member.uuid==uuid).delete()
        Member.session.commit()
        return self.success()

class MemberListHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    @required_permissions('admin:member:index')
    def get(self, *args, **kwargs):
        limit = self.get_argument('limit', 10)
        page = self.get_argument('page', 1)
        pagelist_obj = Member.Q.filter(Member.deleted==0).paginate(page=page, per_page=limit)
        if pagelist_obj is None:
            return self.error('暂无数据')

        total = pagelist_obj.total
        page = pagelist_obj.page
        items = pagelist_obj.items

        params = {
            'count': total,
            'uri': self.request.uri,
            'path': self.request.path,
            'data': [user.as_dict() for user in items],
        }
        return self.success(**params)

class MemberAddHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    @required_permissions('admin:member:add')
    def get(self, *args, **kwargs):
        menu_list = AdminMenu.children(status=1)
        member = Member(status=1, deleted=0)

        data_info = member.as_dict()

        params = {
            'member': member,
            'menu_list': menu_list,
            'data_info': data_info,
            'public_key': sys_config('sys_login_rsa_pub_key'),
            'rsa_encrypt': sys_config('login_pwd_rsa_encrypt'),
        }
        self.render('member/add.html', **params)

    @tornado.web.authenticated
    @required_permissions('admin:member:add')
    def post(self, *args, **kwargs):
        params = self.params()

        params['status'] = params.get('status', 0)

        if not params.get('username', None):
            return self.error('用户名不能为空')
        if not params.get('password', None):
            return self.error('密码不能为空')

        count = Member.Q.filter(Member.username==params['username']).count()
        if count>0:
            return self.error('用户名已被占用')

        if Func.is_mobile(params.get('mobile', '')):
            count = Member.Q.filter(Member.mobile==params['mobile']).count()
            if count>0:
                return self.error('电话号码已被占用', data=params)

        if Func.is_email(params.get('email', '')):
            count = Member.Q.filter(Member.email==params['email']).count()
            if count>0:
                return self.error('Email已被占用')

        password = params.get('password')
        rsa_encrypt = params.get('rsa_encrypt', 0)
        if settings.login_pwd_rsa_encrypt and int(rsa_encrypt)==1 and len(password)>10:
            private_key = sys_config('sys_login_rsa_priv_key')
            password = RSAEncrypter.decrypt(password, private_key)
            params['password'] = make_password(password)

        params.pop('_xsrf', None)
        params.pop('rsa_encrypt', None)
        params['uuid'] = Func.uuid32()
        member = Member(**params)
        Member.session.add(member)
        Member.session.commit()

        return self.success(data=member.as_dict())

class MemberEditHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    @required_permissions('admin:member:edit')
    def get(self, *args, **kwargs):
        uuid = self.get_argument('uuid', None)

        menu_list = AdminMenu.children(status=1)
        member = Member.Q.filter(Member.uuid==uuid).first()

        data_info = member.as_dict()

        params = {
            'member': member,
            'menu_list': menu_list,
            'data_info': data_info,
            'public_key': sys_config('sys_login_rsa_pub_key'),
            'rsa_encrypt': sys_config('login_pwd_rsa_encrypt'),
        }
        self.render('member/edit.html', **params)

    @tornado.web.authenticated
    @required_permissions('admin:member:edit')
    def post(self, *args, **kwargs):
        uuid = self.get_argument('uuid', None)

        params = self.params()

        params['status'] = params.get('status', 0)

        if not uuid:
            return self.error('用户ID不能为空')

        username = params.get('username', None)
        if username:
            count = Member.Q.filter(Member.uuid!=uuid).filter(Member.username==username).count()
            if count>0:
                return self.error('用户名已被占用')

        mobile = params.get('mobile', None)
        params.pop('mobile', None)
        if mobile:
            params['password'] = mobile
            if Func.is_mobile(mobile):
                count = Member.Q.filter(Member.uuid!=uuid).filter(Member.mobile==params['mobile']).count()
                if count>0:
                    return self.error('电话号码已被占用')

        email = params.get('email', None)
        params.pop('email', None)
        if email:
            params['email'] = email
            if Func.is_email(email):
                count = Member.Q.filter(Member.uuid!=uuid).filter(Member.email==params['email']).count()
                if count>0:
                    return self.error('Email已被占用')

        password = params.get('password', None)
        if password:
            rsa_encrypt = params.get('rsa_encrypt', 0)
            if settings.login_pwd_rsa_encrypt and int(rsa_encrypt)==1 and len(password)>10:
                private_key = sys_config('sys_login_rsa_priv_key')
                password = RSAEncrypter.decrypt(password, private_key)
            params['password'] = make_password(password)

        params.pop('_xsrf', None)
        params.pop('rsa_encrypt', None)
        Member.Q.filter(Member.uuid==uuid).update(params)
        Member.session.commit()

        return self.success(data=params)

class MemberInfoHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    @required_permissions('admin:member:info')
    def get(self, *args, **kwargs):
        uuid = self.current_user.get('uuid', None)
        user = Member.Q.filter(Member.uuid==uuid).first()
        data_info = user.as_dict()
        params = {
            'user': user,
            'data_info': data_info,
            'public_key': sys_config('sys_login_rsa_pub_key'),
            'rsa_encrypt': sys_config('login_pwd_rsa_encrypt'),
        }
        self.render('member/info.html', **params)

    @tornado.web.authenticated
    @required_permissions('admin:member:info')
    def post(self, *args, **kwargs):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        rsa_encrypt = self.get_argument('rsa_encrypt', 0)
        email = self.get_argument('email', None)
        mobile = self.get_argument('mobile', None)

        uuid = self.current_user.get('uuid', None)
        user = {}

        if username:
            user['username'] = username
            count = Member.Q.filter(Member.uuid!=uuid).filter(Member.username==username).count()
            if count>0:
                return self.error('用户名已被占用')
        if password:
            if settings.login_pwd_rsa_encrypt and int(rsa_encrypt)==1 and len(password)>10:
                private_key = sys_config('sys_login_rsa_priv_key')
                password = RSAEncrypter.decrypt(password, private_key)
            user['password'] = make_password(password)

        if mobile:
            user['mobile'] = mobile
            count = Member.Q.filter(Member.uuid!=uuid).filter(Member.mobile==mobile).count()
            if count>0:
                return self.error('电话号码已被占用')
        if email:
            user['email'] = email
            count = Member.Q.filter(Member.uuid!=uuid).filter(Member.email==email).count()
            if count>0:
                return self.error('Email已被占用')


        Member.Q.filter(Member.uuid==uuid).update(user)
        Member.session.commit()

        return self.success(data=user)
