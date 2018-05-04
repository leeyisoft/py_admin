#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""

import tornado

from tornado.escape import json_decode

from applications.core.settings_manager import settings
from applications.core.logger.client import SysLogger
from applications.core.utils import utc_to_timezone
from applications.core.decorators import required_permissions

from applications.core.handler import BaseHandler


class CommonHandler(BaseHandler):
    user_session_key = 'e35196e55a3e4014bd262d456947acb5'
    def get_current_user(self):
        user = self.get_secure_cookie(self.user_session_key)
        if user is None:
            return None
        try:
            user = str(user, encoding='utf-8')
            user = user.replace('\'', '"')
            user = json_decode(user)
            return user
        except Exception as e:
            raise e

    def get_template_path(self):
        return 'applications/admin/templates'

class MessageHandler(BaseHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        pass

class EmailHandler(BaseHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        pass