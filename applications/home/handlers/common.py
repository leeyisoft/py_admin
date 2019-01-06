#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""

import tornado

from tornado.escape import json_decode

from applications.core.cache import sys_config
from applications.core.cache import cache
from applications.core.settings_manager import settings
from applications.core.logger.client import SysLogger
from applications.core.handler import BaseHandler

from ..models import Member


class CommonHandler(BaseHandler):
    def get_current_user(self):
        cache_key = self.get_secure_cookie(settings.front_session_key)
        if cache_key is None:
            return None
        try:
            cache_key = str(cache_key, encoding='utf-8')
            # print('cache_key: ', cache_key)
            user = cache.get(cache_key)
            # print('user: ', type(user), user)
            if user:
                return user
            member_id = cache_key[len(settings.member_cache_prefix):]
            # print('member_id: ', member_id)
            member = Member.Q.filter(Member.id==member_id).first()
            if member is None:
                return None
            self.set_curent_user(member)
            user = cache.get(cache_key)
            # print('user: ', type(user), user)
            return user
        except Exception as e:
            raise e


    def set_curent_user(self, member):
        cache_key = member.cache_info(self)
        self.set_secure_cookie(settings.front_session_key, cache_key, expires_days=1)


    def get_login_url(self):
        return '/passport/login'

    def get_template_path(self):
        return 'applications/home/templates'

    def tpl_params(self):
        # 受欢迎的文章
        # populars = get_article(options={'get_list': True, 'order': '-hits', 'limit': 6})
        populars = []

        footer_address = sys_config(key='footer_address')
        telephone = sys_config(key='telephone')
        fax = sys_config(key='fax')
        email = sys_config(key='email')
        site_name = sys_config(key='site_name')

        params = {
            'footer_address': footer_address,
            'telephone': telephone,
            'fax': fax,
            'email': email,
            'populars_left': populars[:3],
            'populars_right': populars[3:],
            'ad_thumb_prefix': '',
            'article_thumb_prefix': '',
            'site_name': site_name,
            'app_name': 'home',
        }
        return params
