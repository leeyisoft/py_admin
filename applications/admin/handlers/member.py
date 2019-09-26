#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""后台会员管理

[description]
"""
import tornado

from trest.router import get
from trest.router import put
from trest.router import post
from trest.router import delete
from trest.exception import JsonError
from trest.config import settings
from trest.utils.hasher import check_password
from trest.utils.encrypter import RSAEncrypter
from trest.utils import func

from applications.admin.utils import required_permissions

from applications.common.models.member import Member
from applications.common.models.member import MemberCertification
from applications.admin.models import Role
from applications.admin.models import AdminMenu

from .common import CommonHandler


class MemberHandler(CommonHandler):
    """docstring for Passport"""
    @get('member/index(.html)?')
    @tornado.web.authenticated
    def member_page(self, *args, **kwargs):
        """后台首页
        """
        params = {
            'sex_options_html': Member.sex_options_html()
        }
        self.render('member/index.html', **params)

    @delete('member')
    @tornado.web.authenticated
    def member_delete(self, *args, **kwargs):
        """删除用户
        """
        id = self.get_argument('id', None)

        Member.Q.filter(Member.id==id).delete()
        Member.session.commit()
        return self.success()

    @get('member')
    @tornado.web.authenticated
    def member_get(self, *args, **kwargs):
        limit = self.get_argument('limit', 10)
        page = self.get_argument('page', 1)
        username = self.get_argument('username', None)
        mobile = self.get_argument('mobile', None)
        email = self.get_argument('email', None)
        sex = self.get_argument('sex', None)

        query = Member.Q.filter(Member.deleted==0)
        if username:
            query = query.filter(Member.username==username)
        if mobile:
            query = query.filter(Member.mobile==mobile)
        if email:
            query = query.filter(Member.email==email)
        if sex:
            query = query.filter(Member.sex==sex)

        pagelist_obj = query.paginate(page=page, per_page=limit)

        if pagelist_obj is None:
            return self.error('暂无数据')

        total = pagelist_obj.total
        page = pagelist_obj.page
        items = pagelist_obj.items
        data = []
        for item in items:
            item2 = item.as_dict()
            item2['sex_option'] = item.sex_option
            data.append(item2)

        params = {
            'count': total,
            'uri': self.request.uri,
            'path': self.request.path,
            'data': data,
        }
        return self.success(**params)

    @get('member/add(.html)?')
    @tornado.web.authenticated
    def member_add_page(self, *args, **kwargs):
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

    @post('member')
    @tornado.web.authenticated
    def member_post(self, *args, **kwargs):
        params = self.params()

        params['status'] = params.get('status', 0)

        if not params.get('username', None):
            return self.error('用户名不能为空')
        if not params.get('password', None):
            return self.error('密码不能为空')

        count = Member.Q.filter(Member.username==params['username']).count()
        if count>0:
            return self.error('用户名已被占用')

        if func.is_mobile(params.get('mobile', '')):
            count = Member.Q.filter(Member.mobile==params['mobile']).count()
            if count>0:
                return self.error('电话号码已被占用', data=params)

        if func.is_email(params.get('email', '')):
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
        member = Member(**params)
        Member.session.add(member)
        Member.session.commit()

        return self.success(data=member.as_dict())

    @get('member/edit(.html)?')
    @tornado.web.authenticated
    def member_edit_page(self, *args, **kwargs):
        id = self.get_argument('id', None)

        menu_list = AdminMenu.children(status=1)
        member = Member.Q.filter(Member.id==id).first()

        data_info = member.as_dict()
        data_info.pop('password', None)
        params = {
            'member': member,
            'menu_list': menu_list,
            'data_info': data_info,
            'public_key': sys_config('sys_login_rsa_pub_key'),
            'rsa_encrypt': sys_config('login_pwd_rsa_encrypt'),
        }
        self.render('member/edit.html', **params)

    @put('member')
    @tornado.web.authenticated
    def member_put(self, *args, **kwargs):
        id = self.get_argument('id', None)
        params = self.params()
        params['status'] = params.get('status', 0)
        if not id:
            return self.error('用户ID不能为空')
        username = params.get('username', None)
        if username:
            count = Member.Q.filter(Member.id!=id).filter(Member.username==username).count()
            if count>0:
                return self.error('用户名已被占用')

        mobile = params.get('mobile', None)
        params.pop('mobile', None)
        if mobile:
            params['mobile'] = mobile
            if func.is_mobile(mobile):
                count = Member.Q.filter(Member.id!=id).filter(Member.mobile==mobile).count()
                if count>0:
                    return self.error('电话号码已被占用')

        email = params.get('email', None)
        params.pop('email', None)
        if email:
            params['email'] = email
            if func.is_email(email):
                count = Member.Q.filter(Member.id!=id).filter(Member.email==email).count()
                if count>0:
                    return self.error('Email已被占用')

        password = params.get('password', None)
        params.pop('password', None)
        if password:
            rsa_encrypt = params.get('rsa_encrypt', 0)
            if settings.login_pwd_rsa_encrypt and int(rsa_encrypt)==1 and len(password)>10:
                private_key = sys_config('sys_login_rsa_priv_key')
                # print('password: ', type(password), password)
                password = RSAEncrypter.decrypt(password, private_key)
            params['password'] = make_password(password)

        params.pop('_xsrf', None)
        params.pop('rsa_encrypt', None)
        Member.Q.filter(Member.id==id).update(params)
        Member.session.commit()

        # update member cache info
        member = Member.Q.filter(Member.id==id).first()
        cache_key = member.cache_info(self)

        return self.success(data=params)

    @get('member/(?P<id>\d*)')
    @tornado.web.authenticated
    def member_detail(self, id):
        user = Member.Q.filter(Member.id==id).first()
        data_info = user.as_dict()
        params = {
            'user': user,
            'data_info': data_info,
            'public_key': sys_config('sys_login_rsa_pub_key'),
            'rsa_encrypt': sys_config('login_pwd_rsa_encrypt'),
        }
        self.render('member/info.html', **params)

class MemberAuthorizeHandler(CommonHandler):
    """实名认证"""
    @get('member/authorize.html')
    @tornado.web.authenticated
    @required_permissions('admin:member:authorize')
    def member_authorize_page(self, *args, **kwargs):
        """**"""
        params = {
        }
        self.render('member/authorize.html', **params)

    @put('member/authorize')
    @tornado.web.authenticated
    def member_authorize_put(self, *args, **kwargs):
        """  """
        current_user_id = self.current_user.get('user_id')

        user_id = self.get_argument('user_id', None)
        status = self.get_argument('status', None)
        authorized = self.get_argument('authorized', None)
        remark = self.get_argument('remark', '')

        member = Member.Q.filter(Member.id==user_id).first()
        if member is None:
            return self.error('用户不存在')


        params = {
            'user_id': user_id,
            'updated_at': utime.timestamp(3),
            'authorized_user_id': current_user_id,
        }
        if status is not None:
            params['status'] = status
        if authorized is not None:
            params['authorized'] = authorized
            params['remark'] = remark
            if member.authorized:
                return self.error('已经实名认证')

        MemberCertification.Q.filter(MemberCertification.user_id==user_id).update(params)
        MemberCertification.session.commit()

        return self.success()

    @get('member/authorize')
    @tornado.web.authenticated
    def member_authorize_get(self, *args, **kwargs):
        limit = self.get_argument('limit', 10)
        page = self.get_argument('page', 1)
        user_id = self.get_argument('user_id', None)
        realname = self.get_argument('realname', None)
        idcardno = self.get_argument('idcardno', None)

        query = MemberCertification.Q
        # query = query.filter(MemberCertification.status==1)
        if user_id:
            query = query.filter(MemberCertification.user_id==user_id)
        if realname:
            query = query.filter(MemberCertification.realname==realname)
        if idcardno:
            query = query.filter(MemberCertification.idcardno==idcardno)

        pagelist_obj = query.paginate(page=page, per_page=limit)

        if pagelist_obj is None:
            return self.error('暂无数据')

        total = pagelist_obj.total
        page = pagelist_obj.page
        items = pagelist_obj.items
        data = []
        for item in items:
            item2 = item.as_dict()
            member = Member.get_info(item.user_id, fields='username,mobile')
            item2['username'] = member.get('username', '')
            item2['mobile'] = member.get('mobile', '')
            item2['authorized_option'] = item.authorized_option
            item2['idcard_img_html'] = '<a href="#" class="show_picture" img_url="%s"><i class="fa fa-picture-o"></i></a>' % self.static_url(item.idcard_img)
            data.append(item2)

        params = {
            'count': total,
            'uri': self.request.uri,
            'path': self.request.path,
            'data': data,
        }
        return self.success(**params)
