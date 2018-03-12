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

from applications.core.cache import sys_config
from applications.core.handler import ApiHandler
from applications.core.utils import required_login
from applications.core.utils import utc_to_timezone

from applications.admin.handlers.common import BaseHandler


class MessageHandler(BaseHandler):
    """docstring for Passport"""
    @required_login
    def get(self, *args, **kwargs):
        pass


class EmailHandler(BaseHandler):
    """docstring for Passport"""
    @required_login
    def get(self, *args, **kwargs):
        pass