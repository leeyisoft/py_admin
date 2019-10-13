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
from applications.admin.utils import admin_required_login

from applications.common.models.user import User
from applications.common.models.user import UserCertification
from applications.admin.models import Role
from applications.admin.models import AdminMenu

from .common import CommonHandler


class UserHandler(CommonHandler):
    """docstring for Passport"""
    @get('user/index(.html)?')
    @admin_required_login
    def user_page(self, *args, **kwargs):
        """后台首页
        """
        params = {
            'sex_options_html': User.sex_options_html()
        }
        self.render('user/index.html', **params)

    @delete('user')
    @admin_required_login
    def user_delete(self, *args, **kwargs):
        """删除用户
        """
        id = self.get_argument('id', None)

        User.Q.filter(User.id==id).delete()
        User.session.commit()
        return self.success()

    @get('user')
    @admin_required_login
    def user_get(self, *args, **kwargs):
        limit = self.get_argument('limit', 10)
        page = self.get_argument('page', 1)
        username = self.get_argument('username', None)
        mobile = self.get_argument('mobile', None)
        email = self.get_argument('email', None)
        sex = self.get_argument('sex', None)

        query = User.Q.filter(User.deleted==0)
        if username:
            query = query.filter(User.username==username)
        if mobile:
            query = query.filter(User.mobile==mobile)
        if email:
            query = query.filter(User.email==email)
        if sex:
            query = query.filter(User.sex==sex)

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

    @get('user/add(.html)?')
    @admin_required_login
    def user_add_page(self, *args, **kwargs):
        menu_list = AdminMenu.children(status=1)
        user = User(status=1, deleted=0)

        data_info = user.as_dict()

        params = {
            'user': user,
            'menu_list': menu_list,
            'data_info': data_info,
            'public_key': sys_config('sys_login_rsa_pub_key'),
            'rsa_encrypt': sys_config('login_pwd_rsa_encrypt'),
        }
        self.render('user/add.html', **params)

    @post('user')
    @admin_required_login
    def user_post(self, *args, **kwargs):
        params = self.params()

        params['status'] = params.get('status', 0)

        if not params.get('username', None):
            return self.error('用户名不能为空')
        if not params.get('password', None):
            return self.error('密码不能为空')

        count = User.Q.filter(User.username==params['username']).count()
        if count>0:
            return self.error('用户名已被占用')

        if func.is_mobile(params.get('mobile', '')):
            count = User.Q.filter(User.mobile==params['mobile']).count()
            if count>0:
                return self.error('电话号码已被占用', data=params)

        if func.is_email(params.get('email', '')):
            count = User.Q.filter(User.email==params['email']).count()
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
        user = User(**params)
        User.session.add(user)
        User.session.commit()

        return self.success(data=user.as_dict())

    @get('user/edit(.html)?')
    @admin_required_login
    def user_edit_page(self, *args, **kwargs):
        id = self.get_argument('id', None)

        menu_list = AdminMenu.children(status=1)
        user = User.Q.filter(User.id==id).first()

        data_info = user.as_dict()
        data_info.pop('password', None)
        params = {
            'user': user,
            'menu_list': menu_list,
            'data_info': data_info,
            'public_key': sys_config('sys_login_rsa_pub_key'),
            'rsa_encrypt': sys_config('login_pwd_rsa_encrypt'),
        }
        self.render('user/edit.html', **params)

    @put('user')
    @admin_required_login
    def user_put(self, *args, **kwargs):
        id = self.get_argument('id', None)
        params = self.params()
        params['status'] = params.get('status', 0)
        if not id:
            return self.error('用户ID不能为空')
        username = params.get('username', None)
        if username:
            count = User.Q.filter(User.id!=id).filter(User.username==username).count()
            if count>0:
                return self.error('用户名已被占用')

        mobile = params.get('mobile', None)
        params.pop('mobile', None)
        if mobile:
            params['mobile'] = mobile
            if func.is_mobile(mobile):
                count = User.Q.filter(User.id!=id).filter(User.mobile==mobile).count()
                if count>0:
                    return self.error('电话号码已被占用')

        email = params.get('email', None)
        params.pop('email', None)
        if email:
            params['email'] = email
            if func.is_email(email):
                count = User.Q.filter(User.id!=id).filter(User.email==email).count()
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
        User.Q.filter(User.id==id).update(params)
        User.session.commit()

        # update user cache info
        user = User.Q.filter(User.id==id).first()
        cache_key = user.cache_info(self)

        return self.success(data=params)

    @get('user/(?P<id>\d*)')
    @admin_required_login
    def user_detail(self, id):
        user = User.Q.filter(User.id==id).first()
        data_info = user.as_dict()
        params = {
            'user': user,
            'data_info': data_info,
            'public_key': sys_config('sys_login_rsa_pub_key'),
            'rsa_encrypt': sys_config('login_pwd_rsa_encrypt'),
        }
        self.render('user/info.html', **params)

class UserAuthorizeHandler(CommonHandler):
    """实名认证"""
    @get('user/authorize.html')
    @admin_required_login
    @required_permissions('admin:user:authorize')
    def user_authorize_page(self, *args, **kwargs):
        """**"""
        params = {
        }
        self.render('user/authorize.html', **params)

    @put('user/authorize')
    @admin_required_login
    def user_authorize_put(self, *args, **kwargs):
        """  """
        current_user_id = self.current_user.get('user_id')

        user_id = self.get_argument('user_id', None)
        status = self.get_argument('status', None)
        authorized = self.get_argument('authorized', None)
        remark = self.get_argument('remark', '')

        user = User.Q.filter(User.id==user_id).first()
        if user is None:
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
            if user.authorized:
                return self.error('已经实名认证')

        UserCertification.Q.filter(UserCertification.user_id==user_id).update(params)
        UserCertification.session.commit()

        return self.success()

    @get('user/authorize')
    @admin_required_login
    def user_authorize_get(self, *args, **kwargs):
        limit = self.get_argument('limit', 10)
        page = self.get_argument('page', 1)
        user_id = self.get_argument('user_id', None)
        realname = self.get_argument('realname', None)
        idcardno = self.get_argument('idcardno', None)

        query = UserCertification.Q
        # query = query.filter(UserCertification.status==1)
        if user_id:
            query = query.filter(UserCertification.user_id==user_id)
        if realname:
            query = query.filter(UserCertification.realname==realname)
        if idcardno:
            query = query.filter(UserCertification.idcardno==idcardno)

        pagelist_obj = query.paginate(page=page, per_page=limit)

        if pagelist_obj is None:
            return self.error('暂无数据')

        total = pagelist_obj.total
        page = pagelist_obj.page
        items = pagelist_obj.items
        data = []
        for item in items:
            item2 = item.as_dict()
            user = User.get_info(item.user_id, fields='username,mobile')
            item2['username'] = user.get('username', '')
            item2['mobile'] = user.get('mobile', '')
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
