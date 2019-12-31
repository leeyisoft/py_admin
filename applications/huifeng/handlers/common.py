#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""

import tornado

from tornado.escape import json_decode

from trest.cache import cache
from trest.config import settings
from trest.logger.client import SysLogger
from trest.handler import Handler

class CommonHandler(Handler):
    def get_current_user(self):
        return None

    def set_curent_user(self, member):
        cache_key = member.cache_info(self)
        self.set_secure_cookie(settings.front_session_key, cache_key, expires_days=1)

    def get_login_url(self):
        return '/passport/login'
