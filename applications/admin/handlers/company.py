#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
公司控制器
"""
import tornado

from applications.admin.services.company import CompanyService
from applications.core.decorators import required_permissions, settings
from .common import CommonHandler
from pyrestful.rest import get, post, put, delete


class IndexHandler(CommonHandler):

    @get('/admin/company', _catch_fire=settings.debug)
    @tornado.web.authenticated
    @required_permissions('admin:company:index')
    def index(self):
        module = self.get_argument('module', None)
        status = self.get_argument('status', None)
        type = self.get_argument('type', None)
        limit = self.get_argument('limit', '10')
        page = self.get_argument('page', '1')
        param = {
            'module': module,
            'status': status,
            'type': type
        }
        pagelist_obj= CompanyService.data_list(param, page, limit)
        res = {
            'page': page,
            'per_page': limit,
            'total': pagelist_obj.total,
            'items': [item.as_dict() for item in pagelist_obj.items],
        }
        return self.success(data=res)

    @get('/admin/company/{id}')
    @tornado.web.authenticated
    @required_permissions('admin:company:detail')
    def detail(self, company_id):
        data= CompanyService.detail_info(company_id)
        return self.success(data=data.as_dict())

    @post('/admin/company')
    @tornado.web.authenticated
    @required_permissions('admin:company:add')
    def add(self):
        module = self.get_argument('module', None)
        status = self.get_argument('status', None)
        type = self.get_argument('type', None)
        company_name = self.get_argument('company_name', None)
        description = self.get_argument('description', None)
        if not(module and status and type and company_name and description):
            return self.error('参数缺失')
        param = {
            'module': module,
            'status': status,
            'type': type,
            'company_name': company_name,
            'description': description
        }
        CompanyService.add_data(param)
        return self.success()

    @put('/admin/company')
    @tornado.web.authenticated
    @required_permissions('admin:company:edit')
    def edit(self):
        company_id = self.get_argument('id', None)
        module = self.get_argument('module', None)
        status = self.get_argument('status', None)
        comtype = self.get_argument('type', None)
        company_name = self.get_argument('company_name', None)
        description = self.get_argument('description', None)
        release = self.get_argument('release', None)
        if not(company_id and module and status and comtype and company_name and description):
            return self.error('参数缺失')
        param = {
            'company_id': company_id,
            'module': module,
            'status': status,
            'type': comtype,
            'company_name': company_name,
            'description': description
        }
        CompanyService.put_data(param)
        return self.success()

    @delete('/admin/company')
    @tornado.web.authenticated
    @required_permissions('admin:company:delete')
    def delete(self):
        company_id = self.get_argument('id', None)
        CompanyService.delete_data(company_id)
        return self.success()
