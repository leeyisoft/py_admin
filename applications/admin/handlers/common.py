#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""

import tornado

from tornado.escape import json_decode

from applications.core.settings_manager import settings
from applications.core.logger.client import SysLogger
from applications.core.cache import sys_config

from applications.core.handler import BaseHandler


class CommonHandler(BaseHandler):
    user_session_key = 'e35196e55a3e4014bd262d456947acb5'
    def get_current_user(self):
        user = self.get_secure_cookie(self.user_session_key)
        if user is None:
            return None
        try:
            user = str(user, encoding='utf-8')
            user = user.replace('\'', '"')
            user = json_decode(user)
            return user
        except Exception as e:
            raise e

    def super_role(self):
        user_id = self.current_user.get('uuid')
        role_id = self.current_user.get('role_id')
        return True if (user_id in settings.SUPER_ADMIN) or (role_id==settings.SUPER_ROLE_ID) else False

    def get_template_path(self):
        return 'applications/admin/templates'


    def get_template_namespace(self):
        """Returns a dictionary to be used as the default template namespace.

        May be overridden by subclasses to add or modify values.

        The results of this method will be combined with additional
        defaults in the `tornado.template` module and keyword arguments
        to `render` or `render_string`.
        """
        namespace = dict(
            sys_config=sys_config,

            handler=self,
            request=self.request,
            current_user=self.current_user,
            locale=self.locale,
            _=self.locale.translate,
            pgettext=self.locale.pgettext,
            static_url=self.static_url,
            xsrf_form_html=self.xsrf_form_html,
            reverse_url=self.reverse_url
        )
        namespace.update(self.ui)
        return namespace
