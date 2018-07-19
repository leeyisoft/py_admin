#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""

import tornado

from tornado.escape import json_decode

from applications.core.settings_manager import settings
from applications.core.logger.client import SysLogger
from applications.core.handler import BaseHandler
from applications.core.cache import cache

from ..models import User

class CommonHandler(BaseHandler):
    session_key = 'de0b3fb0c2f44563944a8cccca7f225a'
    def get_current_user(self):
        cache_key = self.get_secure_cookie(self.session_key)
        if cache_key is None:
            return None
        try:
            cache_key = str(cache_key, encoding='utf-8')
            user = cache.get(cache_key)
            if user:
                return user
            user_id = cache_key[len(settings.user_cache_prefix):]
            user = User.Q.filter(User.id==user_id).first()
            if user is None:
                return None
            self.set_curent_user(user)
            user = cache.get(cache_key)
            # print('user: ', type(user), user)
            return user
        except Exception as e:
            raise e


    def set_curent_user(self, user):
        """设置登录用户cookie信息"""
        user_fileds = ['id', 'username', 'role_id']
        cache_key = '%s%s' % (settings.user_cache_prefix, user.id)
        user = user.as_dict(user_fileds)
        cache.set(cache_key, user, timeout=86400)
        self.set_secure_cookie(self.session_key, cache_key, expires_days=1)


    def super_role(self):
        user_id = self.current_user.get('id')
        role_id = self.current_user.get('role_id')
        return True if (user_id in settings.SUPER_ADMIN) or (role_id==settings.SUPER_ROLE_ID) else False


    def get_template_path(self):
        return 'applications/admin/templates'
