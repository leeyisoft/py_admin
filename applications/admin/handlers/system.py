#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""

import tornado

from applications.core.settings_manager import settings
from applications.core.logger.client import SysLogger
from applications.core.utils import utc_to_timezone
from applications.core.decorators import required_permissions

from applications.core.handler import BaseHandler


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