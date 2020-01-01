#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""
from trest.router import get
from trest.router import put
from trest.router import post

from applications.common.utils import sys_config

from .common import CommonHandler
from ..utils import tpl_params
from ..services.friendlink import FriendlinkService
from ..services.advertising import AdvertisingService
from ..services.goods import GoodsService

class IndexHandler(CommonHandler):
    @get('/case.html')
    def case_get(self, *args, **kwargs):
        params = tpl_params()
        params['index_welcome'] = sys_config('index_welcome', ['title', 'value'])
        params['friendlinks'] = FriendlinkService.get_list({'status': 1})
        params['index_banner'] = AdvertisingService.list_for_category('index_banner', 3)
        params['index_square'] = AdvertisingService.list_for_category('index_square', 4)
        self.render('case.htm', **params)


    @get('/')
    def index_get(self, *args, **kwargs):
        """首页
        """
        params = tpl_params()
        params['index_welcome'] = sys_config('index_welcome', ['title', 'value'])
        params['friendlinks'] = FriendlinkService.get_list({'status': 1})
        params['index_banner'] = AdvertisingService.list_for_category('index_banner', 3)
        params['index_square'] = AdvertisingService.list_for_category('index_square', 4)
        params['index_goods'] = GoodsService.list_most_importance(4)
        self.render('index.htm', **params)
