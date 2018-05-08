#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""
import tornado

from applications.core.settings_manager import settings
from applications.core.logger.client import SysLogger

from .common import CommonHandler


class IndexHandler(CommonHandler):
    def get(self, *args, **kwargs):
        """首页
        """
        params = {
            'current_user': self.current_user,
        }
        self.render('index/index.html', **params)
