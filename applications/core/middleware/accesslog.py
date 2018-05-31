#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
access log中间件，替换tornado的log_request实现插件式日志输出
"""
import datetime
import logging
import pytz

access_log = logging.getLogger('access_log')


class AccessLogMiddleware(object):
    def process_init(self, application):
        application.settings['log_function'] = self.log

    def log(self, handler):
        utc_now = datetime.datetime.now(pytz.timezone('UTC'))
        message = {
            'remote_ip': handler.request.remote_ip,
            'utc_created_at': str(utc_now),
            'host': handler.request.headers.get('host', ''),
            'method': handler.request.method,
            'uri': handler.request.uri,
            'version': handler.request.version,
            'status_code': handler.get_status(),
            'content_length': handler.request.headers.get('Content-Length', ''),
            'referer': handler.request.headers.get('Referer', ''),
            'user_agent': handler.request.headers.get('User-Agent', ''),
            'request_time': 1000.0 * handler.request.request_time(),
            'uuid': handler.get_argument('uuid', ''),
            'client': handler.get_argument('client', ''),
            'token': handler.get_argument('token', ''),
        }
        access_log.info(message)
