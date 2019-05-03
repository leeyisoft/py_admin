#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
base handler
要获得中间件等特性需继承BaseHandler
"""

import tornado.locale
import tornado.web

import pyrestful.rest

from tornado.escape import xhtml_escape
from tornado.escape import json_encode

from raven.contrib.tornado import SentryMixin

from .settings_manager import settings
from .mixins.exception import UncaughtExceptionMixin
from .exception import Http404
from .exception import HttpBadRequestError
from .cache import close_caches
from applications.core.utils import sys_config


class _HandlerPatch(pyrestful.rest.RestHandler, tornado.web.RequestHandler):
    response_to_mq = False

    def error(self, msg='error', code=1, **args):
        code = int(code) if str(code).isdigit() else 1
        self.set_status(200, msg)
        return self.api_json_error(msg, code=code, **args)

    def success(self, msg='success', **args):
        self.set_status(200, msg)
        return self.api_json_error(msg, code=0, **args)

    def get_user_locale(self):
        if settings.TRANSLATIONS_CONF.use_accept_language:
            user_locale = self.get_argument('lang', None)
            if user_locale in ['en', 'us','en_US', 'en-US']:
                return tornado.locale.get('en_US')
            elif user_locale in ['cn','zh_CN', 'zh-CN', 'zh-hans', 'zh-Hans-CN']:
                return tornado.locale.get('zh_CN')
            elif user_locale in ['ph','en_PH', 'en-PH']:
                # 英国 -菲律宾共和国
                return tornado.locale.get('en_PH')
            elif user_locale in ['id','id_ID', 'id-ID']:
                # 印尼 -印尼
                return tornado.locale.get('id_ID')
            elif user_locale in ['vi','vi_VN', 'vi-VN']:
                # 越南 -越南
                return tornado.locale.get('vi_VN')
            elif user_locale in ['tw','zh_TW', 'zh-TW']:
                return tornado.locale.get('zh_TW')
        # 默认中文
        return tornado.locale.get(settings.TRANSLATIONS_CONF.locale_default)

    def on_finish(self):
        try:
            close_caches()
        except:
            pass

class BaseHandler(SentryMixin, UncaughtExceptionMixin, _HandlerPatch):
    def create_template_loader(self, template_path):
        loader = self.application.tmpl
        if loader is None:
            return super(BaseHandler, self).create_template_loader(template_path)
        else:
            return loader(template_path)

    def params(self):
        return dict((k, self.get_argument(k) ) for k, _ in self.request.arguments.items())

    def get_template_namespace(self):
        """Returns a dictionary to be used as the default template namespace.

        May be overridden by subclasses to add or modify values.

        The results of this method will be combined with additional
        defaults in the `tornado.template` module and keyword arguments
        to `render` or `render_string`.
        """
        namespace = dict(
            sys_config=sys_config,
            def_avator=self.static_url('image/default_avatar.jpg'),
            lang=self.get_argument('lang', None),

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
        if self.ui:
            namespace.update(self.ui)
        return namespace

class ErrorHandler(UncaughtExceptionMixin, _HandlerPatch):
    def initialize(self, *args, **kwargs):
        pass

    def prepare(self):
        super(ErrorHandler, self).prepare()
        raise Http404()


if settings.MIDDLEWARE_CLASSES:
    from .mixins.middleware import MiddlewareHandlerMixin

    BaseHandler.__bases__ = (MiddlewareHandlerMixin,) + BaseHandler.__bases__
