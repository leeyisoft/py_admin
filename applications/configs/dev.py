#!/usr/bin/env python
# -*- coding: utf-8 -*-

debug = True

INSTALLED_APPS = (
    'admin',
    # 'home',
)

oss_config = {
    'accesskeyid':'',
    'accesskey':'',
    'endpoint':'oss-ap-southeast-1.aliyuncs.com',
    'bucket_name':'',
}


sentry_url = ''
rabbitmq_config = ''

# 数据库连接字符串，
# 元祖，每组为n个数据库连接，有且只有一个master，可配与不配slave
DATABASE_CONNECTION = {
    'default': {
        'connections': [
            {
                'ROLE': 'master',
                'DRIVER': 'mysql+mysqldb',
                'UID': 'admin',
                # 进过AES加密的密码，格式 aes::: + ciphertext
                'PASSWD': 'admin',
                'HOST': '127.0.0.1',
                'PORT': 3306,
                'DATABASE': 'db_py_admin',
                'QUERY': {'charset': 'utf8'}
            }
        ]
    }
}

CACHES = {
    'default_redis': {
        'BACKEND': 'applications.core.cache.backends.rediscache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
        'OPTIONS': {
            'DB': 3,
            'PASSWORD': 'abc123456',
            'PARSER_CLASS': 'redis.connection.DefaultParser',
            'POOL_KWARGS': {
                'socket_timeout': 2,
                'socket_connect_timeout': 2
            },
            'PING_INTERVAL': 120  # 定时ping redis连接池，防止被服务端断开连接（s秒）
        }
    },

}

redis_config = {
    'host': '127.0.0.1',
    'port': 6379,
    'password': 'abc123456',
    'charset': 'utf-8',
    'db': 3,
}
