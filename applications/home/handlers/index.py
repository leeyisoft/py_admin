#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""
import tornado

from applications.core.utils import sys_config
from applications.core.settings_manager import settings
from applications.core.logger.client import SysLogger

from .common import CommonHandler

from ..utils import tpl_params
from ..models.content import Contact
from ..models.content import Article


class IndexHandler(CommonHandler):
    def get(self, *args, **kwargs):
        """首页
        """
        # ad_list = get_ad(position='index_banner') # 名称中包含 "abc"的人
        ad_list = []

        welcome = sys_config('index_welcome', ['title', 'value'])
        offer = sys_config('index_what_we_offer', ['title', 'value'])
        new_right = sys_config('index_new_right_img', ['title', 'value'])
        slogan = sys_config('index_slogan', ['title', 'value'])
        services_1 = sys_config('index_services_1', ['title', 'value'])
        services_2 = sys_config('index_services_2', ['title', 'value'])
        services_3 = sys_config('index_services_3', ['title', 'value'])

        # 公司动态
        # company_news = get_article(category='company_news', options={'limit': 2, 'order': '-publish_date'})
        company_news = []
        params = {}
        params['category'] = 'activity'
        params['per_page'] = 3
        news_obj = Article.lists(params)
        print('news_obj ', type(news_obj), news_obj.items)
        if news_obj and news_obj.items:
            for item in news_obj.items:
                company_news.append(item)

        # 产品展示
        # products = get_article(category='products', options={'get_list': True, 'order': '-publish_date', 'limit': 8})
        products = []

        params = {
            'ad_list': ad_list,
            'welcome': welcome,
            'offer': offer,
            'new_right': new_right,
            'products_left': products[:4],
            'products_right': products[4:],
            'slogan': slogan,
            'services_1': services_1,
            'services_2': services_2,
            'services_3': services_3,
            'company_news': company_news,
        }
        # 合并字典
        params.update(tpl_params())
        self.render_html('index.htm', **params)
