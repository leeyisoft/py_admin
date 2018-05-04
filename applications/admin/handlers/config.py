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
from applications.core.decorators import required_permissions

from applications.admin.models.system import Config
from applications.admin.models.system import AdminMenu

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

        res = Config.Q.filter(Config.key==key).count()
        if res>0:
            return self.error('KEY已被占用')
        res = Config.Q.filter(Config.title==title).count()
        if res>0:
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

        res = Config.Q.filter(Config.key!=old_key).filter(Config.key==key).count()
        if res>0:
            return self.error('KEY已被占用')
        if title:
            res = Config.Q.filter(Config.key!=old_key).filter(Config.title==title).count()
            if res>0:
                return self.error('名称已被占用')

        Config.Q.filter(Config.key==old_key).delete()
        config = Config(**params)
        Config.session.add(config)
        Config.session.commit()
        return self.success(data=params)
