#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""

import json
import tornado

from applications.core.settings_manager import settings
from applications.core.logger.client import SysLogger
from applications.core.cache import sys_config
from applications.core.cache import cache
from applications.core.decorators import required_permissions
from applications.core.utils import Func
from applications.core.models import Config

from .common import CommonHandler


class ConfigHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    @required_permissions('admin:config:index')
    def get(self, *args, **kwargs):
        params = {
        }
        self.render('config/index.html', **params)

    @tornado.web.authenticated
    @required_permissions('admin:config:delete')
    def delete(self, *args, **kwargs):
        """删除系统配置
        """
        key = self.get_argument('key', None)
        config = Config.Q.filter(Config.key==key).first()
        if not config:
            return self.error(msg='配置不存在', code=404)
        if config.system==1:
            return self.error('系统配置不可删除')

        Config.Q.filter(Config.key==key).delete()
        Config.session.commit()

        cache_key = '%s%s' % (settings.config_cache_prefix,key)
        cache.delete(cache_key)
        return self.success()

class ConfigListHandler(CommonHandler):
    """系统配置列表"""
    @tornado.web.authenticated
    @required_permissions('admin:config:index')
    def get(self, *args, **kwargs):
        limit = self.get_argument('limit', 10)
        page = self.get_argument('page', 1)
        pagelist_obj = Config.Q.filter().paginate(page=page, per_page=limit)
        if pagelist_obj is None:
            return self.error('暂无数据')

        total = pagelist_obj.total
        page = pagelist_obj.page
        items = pagelist_obj.items

        params = {
            'count': total,
            'uri': self.request.uri,
            'path': self.request.path,
            'data': [config.as_dict() for config in items],
        }
        return self.success(**params)

class ConfigAddHandler(CommonHandler):
    """系统配置添加功能"""

    @tornado.web.authenticated
    @required_permissions('admin:config:add')
    def get(self, *args, **kwargs):
        key = self.get_argument('key', None)
        config = Config(sort=20, system=0)

        data_info = config.as_dict()
        params = {
            'config': config,
            'data_info': data_info,
        }
        self.render('config/edit.html', **params)

    @tornado.web.authenticated
    @required_permissions('admin:config:add')
    def post(self, *args, **kwargs):
        title = self.get_argument('title', None)
        key = self.get_argument('key', None)

        params = self.params()
        params.pop('old_key', None)
        params.pop('_xsrf', None)

        if not title:
            return self.error('分组名称不能为空')

        count = Config.Q.filter(Config.key==key).count()
        if count>0:
            return self.error('KEY已被占用')
        count = Config.Q.filter(Config.title==title).count()
        if count>0:
            return self.error('名称已被占用')

        config = Config(**params)
        Config.session.add(config)
        Config.session.commit()
        return self.success(data=params)

class ConfigEditHandler(CommonHandler):
    """系统配置增删查改功能"""
    @tornado.web.authenticated
    @required_permissions('admin:config:edit')
    def get(self, *args, **kwargs):
        key = self.get_argument('key', None)
        config = Config.Q.filter(Config.key==key).first()
        if config is None:
            return self.error('不存在的数据')
        data_info = config.as_dict()
        params = {
            'config': config,
            'data_info': data_info,
        }
        self.render('config/edit.html', **params)


    @tornado.web.authenticated
    @required_permissions('admin:config:edit')
    def post(self, *args, **kwargs):
        title = self.get_argument('title', None)
        key = self.get_argument('key', None)
        old_key = self.get_argument('old_key', None)

        params = self.params()
        params.pop('old_key', None)
        params.pop('_xsrf', None)

        count = Config.Q.filter(Config.key!=old_key).filter(Config.key==key).count()
        if count>0:
            return self.error('KEY已被占用')
        if title:
            count = Config.Q.filter(Config.key!=old_key).filter(Config.title==title).count()
            if count>0:
                return self.error('名称已被占用')

        config = Config.Q.filter(Config.key==old_key).first()
        if config:
            params = {**config.as_dict(), **params}
            params['utc_created_at'] = Func.str_to_datetime(params['utc_created_at'], 'UTC')

        Config.Q.filter(Config.key==old_key).delete()
        Config.session.add(Config(**params))
        Config.session.commit()
        params.pop('utc_created_at', None)

        cache_key = '%s%s' % (settings.config_cache_prefix,key)
        cache.delete(cache_key)

        return self.success(data=params)
