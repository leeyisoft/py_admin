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


class CommonHandler(BaseHandler):
    session_key = 'e35196e55a3e4014bd262d456947acb5'
    def get_current_user(self):
        user = self.get_secure_cookie(self.session_key)
        if user is None:
            return None
        try:
            user = str(user, encoding='utf-8')
            user = user.replace('\'', '"')
            user = json_decode(user)
            return user
        except Exception as e:
            raise e

    def set_curent_user(self, user):
        """设置登录用户cookie信息"""
        user_fileds = ['uuid', 'username', 'role_id']
        user_str = str(user.as_dict(user_fileds))
        self.set_secure_cookie(self.session_key, user_str, expires_days=1)

    def super_role(self):
        user_id = self.current_user.get('uuid')
        role_id = self.current_user.get('role_id')
        return True if (user_id in settings.SUPER_ADMIN) or (role_id==settings.SUPER_ROLE_ID) else False

    def get_template_path(self):
        return 'applications/admin/templates'
