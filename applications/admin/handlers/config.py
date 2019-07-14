#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""

import tornado

from trest.exception import JsonError
from trest.router import get
from trest.router import delete
from trest.router import post
from trest.router import put

from applications.admin.services.config import ConfigService
from trest.settings_manager import settings
from applications.admin.utils import required_permissions
from applications.common.models.base import Config

from .common import CommonHandler


class ConfigPageHandler(CommonHandler):
    """docstring for Passport"""

    @get('/admin/config.page')
    @tornado.web.authenticated
    @required_permissions()
    def config_page(self, *args, **kwargs):
        params = {}
        self.render('config/index.html', **params)

    @get('/admin/config/edit.page')
    @tornado.web.authenticated
    @required_permissions()
    def edit_page(self, *args, **kwargs):
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

class ConfigHandler(CommonHandler):
    """docstring for Passport"""
    @post('/admin/config')
    @tornado.web.authenticated
    @required_permissions()
    def config_post(self):
        title = self.get_argument('title', None)
        key = self.get_argument('key', None)
        value = self.get_argument('value', None)
        subtitle = self.get_argument('subtitle', None)
        sort = self.get_argument('sort',None)
        remark = self.get_argument('remark', None)
        system = self.get_argument('system', 0)
        status = self.get_argument('status',1)
        if title is None or key is  None or value is None:
            return self.error('参数不全', data=['post'])
        params={
            'title':title,
            'key':key,
            'value':value,
            'subtitle':subtitle,
            'sort':sort,
            'remark':remark,
            'system':system,
            'status':status
        }
        ConfigService.save_data(title, key,params)
        return self.success()

    @put('/admin/config')
    @tornado.web.authenticated
    @required_permissions()
    def config_put(self):
        title = self.get_argument('title', None)
        key = self.get_argument('key', None)
        value = self.get_argument('value', None)
        sort = self.get_argument('sort', None)
        remark = self.get_argument('remark', None)
        system = self.get_argument('system', 0)
        status = self.get_argument('status',1)
        if not title or not key or not value:
            return self.error('参数不全', data=['put'])
        param={
            'key':key,
            'title':title,
            'value':value,
            'sort':sort,
            'remark':remark,
            'system':system,
            'status':status
        }
        ConfigService.update_data(param)
        return self.success()

    @get('/admin/config3')
    @tornado.web.authenticated
    @required_permissions()
    def config_get3(self, *args, **kwargs):
        return self.success(data = ['config_get3'])

    @get('/admin/config2')
    @tornado.web.authenticated
    @required_permissions()
    def config_get2(self, *args, **kwargs):
        return self.success(data = ['config_get2'])

    @get('/admin/config')
    @tornado.web.authenticated
    @required_permissions()
    def config_get(self, *args, **kwargs):
        page = int(self.get_argument('page',1))
        limit = int(self.get_argument('limit',10))
        param = {
            'key':self.get_argument('key',None)
        }
        pagelist_obj = ConfigService.get_data(param, limit, page)
        index_list = {
            'page':page,
            'per_page':limit,
            'total':pagelist_obj.total,
            'items':[item.as_dict() for item in pagelist_obj.items],
        }
        return self.success(data = index_list)

    @delete('/admin/config')
    @tornado.web.authenticated
    @required_permissions()
    def config_delete(self):
        key = self.get_argument('key', None)
        ConfigService.delete_data(key)
        return self.success()
