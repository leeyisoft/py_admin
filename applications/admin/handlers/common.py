#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""
from trest.exception import JsonError
from trest.config import settings
from trest.handler import Handler
from trest.cache import cache

from applications.common.utils import sys_config
from applications.admin.services.user import AdminUserService

from ..models import AdminUser


class CommonHandler(Handler):
    format = 'json'

    def params(self):
        return dict((k, self.get_argument(k)) for k, _ in self.request.arguments.items())

    def get_template_namespace(self):
        namespace = super().get_template_namespace()
        namespace['sys_config'] = sys_config
        return namespace

    def get_current_user(self):
        cache_key = self.get_secure_cookie(settings.admin_session_key)
        if not cache_key:
            return None
        try:
            cache_key = str(cache_key, encoding='utf-8')
            user = cache.get(cache_key)
            if user:
                return user
            user_id = cache_key[len(settings.admin_cache_prefix):]
            user = AdminUser.Q.filter(AdminUser.id==user_id).first()
            if user is None:
                return None
            self.set_curent_user(user)
            return cache.get(cache_key)
        except Exception as e:
            raise e

    def set_curent_user(self, user):
        """设置登录用户cookie信息"""
        user_fileds = ['id', 'username', 'role_id']
        cache_key = '%s%d' % (settings.admin_cache_prefix, user.id)
        user = user.as_dict(user_fileds)
        cache.set(cache_key, user, timeout=86400)
        self.set_secure_cookie(settings.admin_session_key, cache_key, expires_days=1)

    def super_role(self):
        """"判断当前用户是否超级用户"""
        user_id = 0
        role_id = 0
        if self.current_user:
            user_id = self.current_user.get('id', 0)
            role_id = self.current_user.get('role_id', 0)
        return AdminUserService.is_super_role(user_id, role_id) if user_id>0 else False


    def get_login_url(self):
        return '/#/login'

    def get_template_path(self):
        return 'applications/admin/templates'
