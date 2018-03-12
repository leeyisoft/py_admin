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
from applications.core.models import UserGroup
from applications.core.models import UserGroupMap

from applications.core.cache import sys_config
from applications.core.handler import ApiHandler
from applications.core.utils import required_login
from applications.core.utils import utc_to_timezone

from applications.admin.handlers.common import BaseHandler


class UserHandler(BaseHandler):
    """docstring for Passport"""
    @required_login
    def get(self, *args, **kwargs):
        """后台首页
        """
        args = {
            'menus': self.admin_menus(),
        }
        self.render('user/index.html', **args)


class UserListHandler(BaseHandler, ApiHandler):
    """docstring for Passport"""
    @required_login
    def get(self, *args, **kwargs):
        limit = self.get_argument('limit', 10)
        page = self.get_argument('page', 1)
        pagelist_obj = User.Q.filter().paginate(page=page, per_page=limit)
        if pagelist_obj is None:
            return self.error('暂无数据')

        total = pagelist_obj.total
        page = pagelist_obj.page
        items = pagelist_obj.items
        # print('items : ', items)

        args = {
            'count': total,
            'uri': self.request.uri,
            'path': self.request.path,
            'data': [user.as_dict() for user in items],
        }
        return self.success(**args)

class UserSaveHandler(BaseHandler, ApiHandler):
    """docstring for Passport"""
    @required_login
    def get(self, *args, **kwargs):
        uuid = self.get_argument('uuid', None)
        user = User.Q.filter(User.uuid==uuid).first()
        groups = UserGroup.Q.filter(UserGroup.deleted==0).filter(UserGroup.status==1).all()

        # user.group_id = User.group_id(user)
        print('user ', user.group_id)
        args = {
            'user': user,
            'groups': groups
        }
        self.render('user/save.html', **args)

    @required_login
    def post(self, *args, **kwargs):
        group_id = self.get_argument('group_id', None)
        uuid = self.get_argument('uuid', None)
        username = self.get_argument('username', None)
        email = self.get_argument('email', None)
        mobile = self.get_argument('mobile', None)
        status = self.get_argument('status', 0)
        if not username:
            return self.error('用户名不能为空')
        # if not email and not is_email(email):
        #     return self.error('Email格式不正确')
        # if not mobile and not is_mobile(mobile):
        #     return self.error('电话号码不能为空')

        if uuid:
            res = User.Q.filter(User.uuid!=uuid).filter(User.username==username).count()
            if res>0:
                return self.error('用户名已被占用')

            if mobile:
                res = User.Q.filter(User.uuid!=uuid).filter(User.mobile==mobile).count()
                if res>0:
                    return self.error('电话号码已被占用')
            if email:
                res = User.Q.filter(User.uuid!=uuid).filter(User.email==email).count()
                if res>0:
                    return self.error('Email已被占用')

            user = {
                'username':username,
            }
            if mobile:
                user['mobile'] = mobile
            if email:
                user['email'] = email
            user['status'] = status
            User.Q.filter(User.uuid==uuid).update(user)

            ugmap = UserGroupMap(user_id=uuid, group_id=group_id)
            UserGroupMap.session.merge(ugmap)
        else:
            if username:
                res = User.Q.filter(User.username==username).count()
                if res>0:
                    return self.error('用户名已被占用')

            params = {
                'username': username,
            }
            if mobile:
                params['mobile'] = mobile
                res = User.Q.filter(User.mobile==mobile).count()
                if res>0:
                    return self.error('电话号码已被占用')
            if email:
                params['email'] = email
                res = User.Q.filter(User.email==email).count()
                if res>0:
                    return self.error('Email已被占用')
            user = User(**params)
            User.session.add(user)
            # 为了输出
            user = user.as_dict()
        User.session.commit()

        return self.success(data=user)

class GroupHandler(BaseHandler):
    """docstring for Passport"""
    @required_login
    def get(self, *args, **kwargs):
        args = {
            'menus': self.admin_menus(),
        }
        self.render('user/group.html', **args)


class GroupListHandler(BaseHandler, ApiHandler):
    """用户组列表"""
    @required_login
    def get(self, *args, **kwargs):
        limit = self.get_argument('limit', 10)
        page = self.get_argument('page', 1)
        pagelist_obj = UserGroup.Q.filter().paginate(page=page, per_page=limit)
        if pagelist_obj is None:
            return self.error('暂无数据')

        total = pagelist_obj.total
        page = pagelist_obj.page
        items = pagelist_obj.items

        args = {
            'count': total,
            'uri': self.request.uri,
            'path': self.request.path,
            'data': [group.as_dict() for group in items],
        }
        return self.success(**args)

class GroupSaveHandler(BaseHandler, ApiHandler):
    """用户组增删查改功能"""
    @required_login
    def get(self, *args, **kwargs):
        uuid = self.get_argument('uuid', None)
        group = UserGroup.Q.filter(UserGroup.uuid==uuid).first()
        args = {
            'group': group,
        }
        self.render('user/group_save.html', **args)


    @required_login
    def post(self, *args, **kwargs):
        groupname = self.get_argument('groupname', None)
        uuid = self.get_argument('uuid', None)
        status = self.get_argument('status', 0)
        if not groupname:
            return self.error('分组名称不能为空')

        if uuid:
            group = {
                'groupname':groupname,
            }
            group['status'] = status
            UserGroup.Q.filter(UserGroup.uuid==uuid).update(group)


        else:
            group = UserGroup(groupname=groupname)
            UserGroup.session.add(group)
        UserGroup.session.commit()
        return self.success()

    @required_login
    def delete(self, *args, **kwargs):
        uuid = self.get_argument('uuid', None)
        if not uuid:
            return self.error('非法操作')

        group = {
            'deleted':1,
        }
        UserGroup.Q.filter(UserGroup.uuid==uuid).update(group)
        UserGroup.session.commit()
        return self.success()


class GroupAccreditHandler(BaseHandler, ApiHandler):
    """用户组授权功能"""
    @required_login
    def get(self, *args, **kwargs):
        uuid = self.get_argument('uuid', None)
        if not uuid:
            return self.error('非法操作')

        group = UserGroup.Q.filter(UserGroup.uuid==uuid).first()
        group.permission = group.permission.split(',') if group.permission else []

        from applications.acl import accredit
        from applications.acl import acl_nodes
        # return self.success(data=accredit(acl_nodes))
        args = {
            'group': group,
            'accredit_items': accredit(acl_nodes)
        }
        self.render('user/group_accredit.html', **args)


    @required_login
    def post(self, *args, **kwargs):
        uuid = self.get_argument('uuid', None)
        permission = self.get_argument('permission', '')
        if not uuid:
            return self.error('非法操作')
        # print(type(permission), permission)
        group = {
            'permission': permission,
        }
        UserGroup.Q.filter(UserGroup.uuid==uuid).update(group)
        UserGroup.session.commit()
        return self.success()


