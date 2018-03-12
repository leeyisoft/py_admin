#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""

from applications.core.encrypter import RSAEncrypter
from applications.core.settings_manager import settings
from applications.core.logger.client import SysLogger

from applications.core.cache import sys_config
from applications.core.models import Config
from applications.core.models import User
from applications.core.utils import required_login

from applications.admin.handlers.common import BaseHandler


class DashboardHandler(BaseHandler):
    @required_login
    def get(self, *args, **kwargs):
        """后台首页
        """
        items = {
            'menus': self.admin_menus(),
        }
        self.render('dashboard/index.html', **items)
