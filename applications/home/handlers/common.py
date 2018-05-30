#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""

import tornado

from tornado.escape import json_decode

from applications.core.logger.client import SysLogger
from applications.core.handler import BaseHandler


class CommonHandler(BaseHandler):
    session_key = 'ba561cfa32694a83883791db60d26135'
    token_key = 'c17a6633e5e64f00bfc93534cae80a2b'
    def get_current_user(self):
        user = self.get_secure_cookie(self.session_key)
        if user is None:
            return None
        try:
            user = str(user, encoding='utf-8')
            user = user.replace('\'', '"')
            user = json_decode(user)
            avatar = user.get('avatar', None)
            if avatar:
                user['avatar'] = self.static_url(user['avatar'])
            else:
                user['avatar'] = self.static_url('image/default_avatar.jpg')
            return user
        except Exception as e:
            raise e

    def set_curent_user(self, member):
        """设置登录用户cookie信息"""
        user_fileds = ['uuid', 'username', 'avatar', 'sign']
        user = member.as_dict(user_fileds)
        self.set_secure_cookie(self.session_key, str(user), expires_days=1)

    def get_login_url(self):
        return '/passport/login'

    def get_template_path(self):
        return 'applications/home/templates'

