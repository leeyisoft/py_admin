#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""
from trest.router import get
from trest.exception import Http404
from applications.common.utils import sys_config

from .common import CommonHandler
from ..utils import tpl_params
from ..services.friendlink import FriendlinkService
from ..services.advertising import AdvertisingService
from ..services.goods import GoodsService

class IndexHandler(CommonHandler):
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

    @get('/case.html')
    def case_list_get(self, *args, **kwargs):
        params = tpl_params()
        params['index_welcome'] = sys_config('index_welcome', ['title', 'value'])
        params['friendlinks'] = FriendlinkService.get_list({'status': 1})
        params['index_banner'] = AdvertisingService.list_for_category('index_banner', 3)
        params['index_square'] = AdvertisingService.list_for_category('index_square', 4)
        self.render('goods_list.htm', **params)

    @get('/case/(?P<id>[0-9]+)')
    def case_get(self, id):
        params = tpl_params()
        goods = GoodsService.get(id)
        if not goods:
            raise Http404('Nonexistent records')

        GoodsService.increase_hits(goods.id)
        params['goods'] = goods

        self.render('goods_detail.htm', **params)

    @get('/service.html')
    def service_get(self, *args, **kwargs):
        params = tpl_params()
        params['service_banner'] = AdvertisingService.get_for_category('service_banner')
        params['service_services'] = AdvertisingService.get_for_category('service_services')
        params['service_contact_us'] = AdvertisingService.get_for_category('service_contact_us')
        params['service_flow'] = AdvertisingService.list_for_category('service_flow', 12)
        self.render('singlepage_service.htm', **params)

    @get('/about.html')
    def about_get(self, *args, **kwargs):
        params = tpl_params()

        params['about_banner'] = AdvertisingService.get_for_category('about_banner')
        params['about_us'] = AdvertisingService.get_for_category('about_us')
        params['team'] = AdvertisingService.list_for_category('team', 9)
        self.render('singlepage_about.htm', **params)
