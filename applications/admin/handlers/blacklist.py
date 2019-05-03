#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
黑名单控制器
"""
import tornado
from pyrestful.rest import get
from pyrestful.rest import post
from pyrestful.rest import put
from pyrestful.rest import delete

from applications.core.settings_manager import settings
from applications.core.decorators import required_permissions
from applications.admin.services.blacklist import BlackListService
from .common import CommonHandler

class IndexHandler(CommonHandler):

    @get('/admin/blacklist', _catch_fire=settings.debug)
    @tornado.web.authenticated
    @required_permissions('admin:blacklist:index')
    def index(self):
        value = self.get_argument('value', None)
        type = self.get_argument('type', None)
        limit = self.get_argument('limit', '10')
        page = self.get_argument('page', '1')
        order_number = self.get_argument('order_number', None)
        admin_id = self.get_argument('admin_id', None)
        param = {
            'value': value,
            'type': type,
            'order_number': order_number,
            'admin_id': admin_id
        }
        (code, msg, (total, data)) = BlackListService.data_list(param, page, limit)
        if code > 0:
            return self.error(msg=msg)
        options = {}
        if int(page) == 1:
            options['types'] = BlackListService.type_options()
            options['status'] = BlackListService.status_options()
        res = {
            'page': page,
            'per_page': limit,
            'total': total,
            'items': data,
            'options': options
        }
        return self.success(data=res)


    @get('/admin/blacklist/{id}')
    @tornado.web.authenticated
    @required_permissions('admin:blacklist:detail')
    def detail(self, id):
        (code, msg, data) = BlackListService.detail_info(id)
        if code > 0:
            return self.error(msg=msg)
        return self.success(data=data)


    @post('/admin/blacklist', _catch_fire=settings.debug)
    @tornado.web.authenticated
    @required_permissions('admin:blacklist:add')
    def add(self):
        type = self.get_argument('type', None)
        value = self.get_argument('value', None)
        reason = self.get_argument('reason', None)
        order_number = self.get_argument('order_number', None)
        if not(value and type):
            return self.error('参数缺失')
        admin_id = self.current_user.get('id')
        param = {
            'value': value,
            'reason': reason,
            'type': type,
            'admin_id': admin_id,
            'order_number': order_number
        }
        (code, msg, res_data) = BlackListService.add_data(param)
        if code > 0:
            return self.error(msg=msg)
        return self.success()


    @put('/admin/blacklist', _catch_fire=settings.debug)
    @tornado.web.authenticated
    @required_permissions('admin:blacklist:edit')
    def edit(self):
        id = self.get_argument('id', None)
        status = self.get_argument('status', None)
        if not(id and status):
            return self.error('参数缺失')
        param = {
            'id': id,
            'status': status
        }
        (code, msg, res_data) = BlackListService.put_data(param)
        if code > 0:
            return self.error(msg=msg)
        return self.success()


    @delete('/admin/blacklist')
    @tornado.web.authenticated
    @required_permissions('admin:blacklist:delete')
    def delete(self):
        id = self.get_argument('id', None)
        if not id:
            return self.error('参数缺失')
        (code, msg, res_data) = BlackListService.delete_data(id)
        if code > 0:
            return self.error(msg=msg)
        return self.success()
