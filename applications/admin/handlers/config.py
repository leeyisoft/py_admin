#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""

import tornado

from pyrestful.rest import get
from pyrestful.rest import delete
from pyrestful.rest import post
from pyrestful.rest import put

from applications.admin.services.config import ConfigService
from applications.core.settings_manager import settings
from applications.core.decorators import required_permissions

from .common import CommonHandler


class ConfigHandler(CommonHandler):
    """docstring for Passport"""

    @get('/admin/config.page', _catch_fire=settings.debug)
    def page(self, *args, **kwargs):
        next = self.get_argument('next', '')
        params = {
            'next': next,
        }
        self.render('config/index.html', **params)

    @get('/admin/config', _catch_fire=settings.debug)
    @tornado.web.authenticated
    @required_permissions('admin:config:index_list_all')
    def index_list_all(self):
        page=int(self.get_argument('page',1))
        limit=int(self.get_argument('limit',10))
        param={
            'key':self.get_argument('key',None)
        }
        pagelist_obj = ConfigService.get_data(param, limit, page)
        index_list={
            'page':page,
            'per_page':limit,
            'total':pagelist_obj.total,
            'items':[item.as_dict() for item in pagelist_obj.items],
        }
        return self.success(data=index_list)

    @delete('/admin/config', _catch_fire=settings.debug)
    @tornado.web.authenticated
    @required_permissions('admin:config:delete_one')
    def delete_one(self):
        key = self.get_argument('key', None)
        ConfigService.delete_data(key)
        return self.success()

    @post('/admin/config', _catch_fire=settings.debug)
    @tornado.web.authenticated
    @required_permissions('admin:config:add')
    def add(self):
        title = self.get_argument('title', None)
        key = self.get_argument('key', None)
        value = self.get_argument('value', None)
        subtitle = self.get_argument('subtitle', None)
        sort = self.get_argument('sort',None)
        remark = self.get_argument('remark', None)
        system = self.get_argument('system', 0)
        status = self.get_argument('status',1)
        if title is None or key is  None or value is None:
            return self.error('参数不全')
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

    @put('/admin/config', _catch_fire=settings.debug)
    @tornado.web.authenticated
    @required_permissions('admin:config:edit')
    def edit(self):
        title = self.get_argument('title', None)
        key = self.get_argument('key', None)
        value = self.get_argument('value', None)
        sort = self.get_argument('sort', None)
        remark = self.get_argument('remark', None)
        system = self.get_argument('system', 0)
        status = self.get_argument('status',1)
        if not title or not key or not value:
            return self.error('参数不全')
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
