#!/usr/bin/env python
# -*- coding: utf-8 -*-

from applications.core.settings_manager import settings
from tornado.util import import_object

from .file import FileUtil
from .file import Uploader
from .string import String2
from .object import RWLock

from ..db import redisdb


safestr = String2.safestr

def sys_config(key, field='value'):
    cache_key = '%s%s' % (settings.config_cache_prefix,key)
    cache_val = redisdb.get(cache_key)
    # print('cache_key', cache_key)
    if field=='delete_key_value':
        return redisdb.delete(cache_key)
    if cache_val:
        # print('cache_val: ', cache_val)
        return cache_val
    Config = import_object('applications.common.models.base.Config')
    if field=='value':
        query = "select `value` from `sys_config` where `status`=1 and `key`='%s';" % key;
        value = Config.session.execute(query).scalar()
        value = value if value is not None else ''
    elif type(field)==list:
        query = "select %s from `sys_config` where `status`=1 and `key`='%s';" % (','.join(field),key);
        # print('field', type(field), field)
        field = Config.session.execute(query).fetchone()
        # print('field', type(field), field)
        value = dict(field)
    # endif
    redisdb.set(cache_key, value, 86400)
    return value
