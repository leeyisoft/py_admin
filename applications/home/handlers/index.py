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
            'ad_list': [],
            'slogan': {'title':'','cvalue':''},
            'welcome': {'title':'', 'subtitle':'','cvalue':''},
            'offer': {'title':'', 'subtitle':'','cvalue':''},
            'welcome': {'title':'', 'subtitle':'','cvalue':''},
            'services_1': {'title':'','cvalue':''},
            'services_2': {'title':'','cvalue':''},
            'services_3': {'title':'','cvalue':''},
            'company_news': [],
            'new_right': None,
        }
        # 合并字典
        params.update(self.tpl_params())
        self.render_html('index.htm', **params)
