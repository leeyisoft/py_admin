#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""
import tornado

from applications.core.settings_manager import settings
from applications.core.logger.client import SysLogger
from applications.core.cache import sys_config

from .common import CommonHandler


class AboutHandler(CommonHandler):
    def get(self, *args, **kwargs):
        """
        关于我们
        """
        about_us_a = sys_config(key='about_us_a')
        about_us_b = sys_config(key='about_us_b')
        # teams = get_teams({'limit':8})
        teams = []
        params = {
            # 'request': request,
            'about_us_a': about_us_a,
            'about_us_b': about_us_b,
            'teams': teams,
            'new_right':{},
            'flatpage': {'title':'',},
        }
        # 合并字典
        params.update(self.tpl_params())

        self.render_html('singlepage/about.htm', **params)

class ActivityHandler(CommonHandler):
    def get(self, *args, **kwargs):
        """
        新闻活动
        """
        breadcrumb = [
            {'title': '新闻活动', 'url': '/company/activity/'},
            {'title': 'List', 'url': '#'},
        ]

        params = {
            'breadcrumb': breadcrumb,
            'arc_list': [],
            'flatpage': {'title':'',},
        }

        # 合并字典
        params.update(self.tpl_params())
        self.render_html('article/list1.htm', **params)

class RegulationsHandler(CommonHandler):
    def get(self, *args, **kwargs):
        """
        政策法规
        """
        breadcrumb = [
            {'title': '政策法规', 'url': '/regulations/'},
            {'title': 'List', 'url': '#'},
        ]
        params = {
            'breadcrumb': breadcrumb,
            'arc_list': [],
            'flatpage': {'title':'',},
        }
        # 合并字典
        params.update(self.tpl_params())
        self.render_html('article/list1.htm', **params)

class ProductHandler(CommonHandler):
    def get(self, *args, **kwargs):
        """
        产品展示
        """
        breadcrumb = [
            {'title': '产品展示', 'url': '/company/product/'},
            {'title': 'List', 'url': '#'},
        ]
        params = {
            'breadcrumb': breadcrumb,
            'arc_list': {},
            'flatpage': {'title':'',},
        }
        # 合并字典
        params.update(self.tpl_params())
        self.render_html('article/list2.htm', **params)


class ContactHandler(CommonHandler):
    def get(self, *args, **kwargs):
        """
        联系我们
        """
        contact = sys_config(key='contact')

        params = {
            'contact': contact,
            'flatpage': {'title':'',},
            'csrf_input': self.xsrf_form_html(),
        }        # 合并字典
        params.update(self.tpl_params())
        self.render_html('singlepage/contact.htm', **params)

