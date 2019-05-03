#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import redis

from .dbalchemy import Connector

from applications.core.settings_manager import settings


#指定decode_responses为True，表示输出为字符串
redisdb = redis.StrictRedis(
    host=settings.redis_config.get('host', '127.0.0.1'),
    port=settings.redis_config.get('port', 6379),
    password=settings.redis_config.get('password', ''),
    charset=settings.redis_config.get('charset', 'utf-8'),
    db=settings.redis_config.get('db', 0),
    decode_responses=True)

def mysqldb(dbt='master'):
    sess = Connector.get_session()
    return sess.get(dbt, False)