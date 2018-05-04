#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
base handler
要获得中间件等特性需继承BaseHandler
"""

import tornado.locale
import tornado.web

from tornado.escape import xhtml_escape
from tornado.escape import json_encode

from .settings_manager import settings
from .mixins.exception import UncaughtExceptionMixin
from .exception import Http404
from .exception import HttpBadRequestError
from .cache import close_caches


class _HandlerPatch(tornado.web.RequestHandler):

    def get_format(self, params_name="format"):
        format = self.get_argument(params_name, None)
        if not format:
            accept = self.request.headers.get('Accept')
            try:
                format = accept.split(',')[0].split('/')[1]
                format = 'json' if format=='*' else format
            except Exception as e:
                format = 'json'
        return format.lower() or 'json'

    def _return(self, msg, code=0, **args):
        resp_str = ''
        requ_format = self.get_format()
        if requ_format in ['json', 'jsonp']:
            self.set_header('Content-Type', 'application/json; charset=UTF-8')
            data_dict = {
                'code': code,
                'msg': msg,
            }
            data_dict.update(args)
            resp_str = json_encode(data_dict)
            if requ_format=='jsonp':
                callback = self.get_argument('callback', 'callback')
                resp_str = '%s(%s)' % (callback, resp_str)
        else:
            self.set_header('Content-Type', 'text/html; charset=UTF-8')

            resp_str = msg if args.get('xhtml_escape', True) is False else xhtml_escape(msg)

        self.write(resp_str)
        self.finish()
        return

    def error(self, msg='error', code=990000):
        code = int(code) if str(code).isdigit() else 990000
        self.set_status(code, msg)
        return self._return(msg, code)

    def success(self, msg='success', **args):
        self.set_status(200, msg)
        return self._return(msg, code=0, **args)

    def show(self, data, **args):
        return self._return(data, **args)

    def get_user_locale(self):
        if settings.TRANSLATIONS_CONF.use_accept_language:
            return None

        return tornado.locale.get(settings.TRANSLATIONS_CONF.locale_default)

    def on_finish(self):
        try:
            close_caches()
        except:
            pass

class BaseHandler(UncaughtExceptionMixin, _HandlerPatch):
    def create_template_loader(self, template_path):
        loader = self.application.tmpl
        if loader is None:
            return super(BaseHandler, self).create_template_loader(template_path)
        else:
            return loader(template_path)

    def params(self):
        return dict((k, self.get_argument(k) ) for k, _ in self.request.arguments.items())

class ErrorHandler(UncaughtExceptionMixin, _HandlerPatch):
    def initialize(self, *args, **kwargs):
        pass

    def prepare(self):
        super(ErrorHandler, self).prepare()
        raise Http404()


if settings.MIDDLEWARE_CLASSES:
    from .mixins.middleware import MiddlewareHandlerMixin

    BaseHandler.__bases__ = (MiddlewareHandlerMixin,) + BaseHandler.__bases__
