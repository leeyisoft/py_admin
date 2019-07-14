#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
黑名单控制器
"""
import tornado
from trest.router import get
from trest.router import post
from trest.router import put
from trest.router import delete

from trest.settings_manager import settings
from applications.admin.utils import required_permissions
from applications.admin.services.blacklist import BlackListService
from .common import CommonHandler

class IndexHandler(CommonHandler):

    @get('/admin/blacklist')
    @tornado.web.authenticated
    @required_permissions()
    def index(self):
        value = self.get_argument('value', None)
        bltype = self.get_argument('type', None)
        limit = self.get_argument('limit', '10')
        page = self.get_argument('page', '1')
        loan_order_id = self.get_argument('loan_order_id', None)
        admin_id = self.get_argument('admin_id', None)
        param = {}
        if value:
            param['value'] = value
        if bltype:
            param['bltype'] = bltype
        if loan_order_id:
            param['loan_order_id'] = loan_order_id
        if admin_id:
            param['admin_id'] = admin_id
        pagelist_obj = BlackListService.data_list(param, page, limit)
        # print('pagelist_obj ', type(pagelist_obj), pagelist_obj.items)
        items = []
        for val in pagelist_obj.items:
            items.append(val.as_dict())

        options = {}
        if int(page) == 1:
            options['types'] = BlackListService.type_options()
            options['status'] = BlackListService.status_options()
        res = {
            'page': page,
            'per_page': limit,
            'total': pagelist_obj.total,
            'items': items,
            'options': options,
        }
        return self.success(data=res)

    @get('/admin/blacklist/{id}')
    @tornado.web.authenticated
    @required_permissions()
    def detail(self, id):
        obj = BlackListService.detail_info(id)
        return self.success(data=obj.as_dict())


    @post('/admin/blacklist')
    @tornado.web.authenticated
    @required_permissions()
    def add(self):
        type = self.get_argument('type', None)
        value = self.get_argument('value', None)
        reason = self.get_argument('reason', None)
        loan_order_id = self.get_argument('loan_order_id', None)
        if not(value and type):
            return self.error('参数缺失')
        admin_id = self.current_user.get('id')
        param = {
            'value': value,
            'reason': reason,
            'type': type,
            'admin_id': admin_id,
            'loan_order_id': loan_order_id
        }
        BlackListService.add_data(param)
        return self.success()


    @put('/admin/blacklist')
    @tornado.web.authenticated
    @required_permissions()
    def edit(self):
        id = self.get_argument('id', None)
        status = self.get_argument('status', None)
        if not(id and status):
            return self.error('参数缺失')
        param = {
            'id': id,
            'status': status
        }
        BlackListService.put_data(param)
        return self.success()


    @delete('/admin/blacklist')
    @tornado.web.authenticated
    @required_permissions()
    def delete(self):
        id = self.get_argument('id', None)
        if not id:
            return self.error('参数缺失')
        BlackListService.delete_data(id)
        return self.success()
