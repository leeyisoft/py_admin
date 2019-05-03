#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
定时任务中间件
"""

from tornado.ioloop import PeriodicCallback
from tornado.gen import coroutine
from tornado.util import import_object

from ..logger import SysLogger
from ..settings_manager import settings


class PeriodicCallbackMiddleware(object):
    def process_init(self, application):
        try:
            items = settings.CRONTAB_PeriodicCallback
            for (path_obj, method_name, params, inteval) in items:
                obj = import_object(path_obj)
                c_func = getattr(obj, method_name)
                PeriodicCallback(lambda: c_func(**params), inteval).start()
        except Exception as e:
            raise e
            pass
