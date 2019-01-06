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
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import TemplateNotFound


from .settings_manager import settings
from .mixins.exception import UncaughtExceptionMixin
from .exception import Http404
from .exception import HttpBadRequestError
from .cache import close_caches
from .cache import sys_config


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
        msg = '%s' % msg
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

    def error(self, msg='error', code=500, **args):
        code = int(code) if str(code).isdigit() else 500
        self.set_status(code, msg)
        return self._return(msg, code, **args)

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

class _TemplateRendring(object):
  """
  A simple class to hold methods for rendering templates.
  """
  def render_template(self, template_name, **kwargs):
    template_dirs = []
    # print('self.settings', self.settings)
    # print('self.settings', self.settings['template_path'])
    if self.settings.get('template_path', ''):
      template_dirs.append(self.settings['template_path'])
    # print('self.settings', self.settings['template_path'])
    env = Environment(loader=FileSystemLoader(template_dirs))

    try:
      template = env.get_template(template_name)
    except TemplateNotFound:
      raise TemplateNotFound(template_name)
    content = template.render(kwargs)
    return content

class BaseHandler(UncaughtExceptionMixin, _HandlerPatch, _TemplateRendring):
    def create_template_loader(self, template_path):
        loader = self.application.tmpl
        if loader is None:
            return super(BaseHandler, self).create_template_loader(template_path)
        else:
            return loader(template_path)

    def params(self):
        return dict((k, self.get_argument(k) ) for k, _ in self.request.arguments.items())

    def invalid_img_captcha(self, code):
        """ 图像验证码验证 不区分大小写"""
        valid_code = self.get_secure_cookie(settings.valid_code_key)
        valid_code = valid_code.decode('utf-8')
        return valid_code.lower()!=code.lower()

    def render_html(self, template_name, **kwargs):
        self.settings['template_path'] = self.get_template_path()
        kwargs.update(dict(
            sys_config=sys_config,
            def_avator=self.static_url('image/default_avatar.jpg'),

            handler=self,
            request=self.request,
            current_user=self.current_user,
            locale=self.locale,
            _=self.locale.translate,
            pgettext=self.locale.pgettext,
            static_url=self.static_url,
            xsrf_form_html=self.xsrf_form_html,
            reverse_url=self.reverse_url
        ))
        content = self.render_template(template_name, **kwargs)
        self.write(content)

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
