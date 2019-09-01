#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""广告位控制器

[description]
"""

import tornado

from trest.router import get
from trest.router import put
from trest.router import post
from trest.router import delete
from trest.exception import JsonError
from trest.settings_manager import settings

from applications.admin.services.advertise_category import AdvertisingCategoryService
from applications.admin.utils import required_permissions

from .common import CommonHandler


class AdvertiseCatHandler(CommonHandler):

    @get('/admin/advertise_cat')
    @tornado.web.authenticated
    @required_permissions()
    def index(self):
        """
        广告位分类
        :return:
        """
        limit = self.get_argument('limit', '10')
        page = self.get_argument('page', '1')
        status = self.get_argument('status', None)
        lang = self.get_argument('lang', None)

        param={
            'status': status,
            'lang': lang
        }
        pagelist_obj = AdvertisingCategoryService.data_list(param, page, limit)
        res = {
            'page': page,
            'per_page': limit,
            'total': pagelist_obj.total,
            'items': [item.as_dict() for item in pagelist_obj.items],
        }
        return self.success(data=res)

    @post('/admin/advertise_cat')
    @tornado.web.authenticated
    @required_permissions()
    def add(self):
        """
        新增广告位分类
        """
        lang = self.get_argument('lang', 'en')
        name = self.get_argument('name', None)
        status = self.get_argument('status', '1')

        if not name or not status:
            return self.error('参数错误')
        param ={
            'lang': lang,
            'name': name,
            'status': status,

        }
        AdvertisingCategoryService.add_data(param)
        return self.success()

    @put('/admin/advertise_cat')
    @tornado.web.authenticated
    @required_permissions()
    def edit(self):
        """
        修改广告位分类
        """
        lang = self.get_argument('lang', 'en')
        name = self.get_argument('name', None)
        status = self.get_argument('status', '1')
        cat_id = self.get_argument('cat_id', None)

        if not cat_id:
            return self.error('参数错误')
        param = {
            'lang': lang,
            'name': name,
            'status': status,
        }
        AdvertisingCategoryService.put_data(param, cat_id)
        return self.success()

    @delete('/admin/advertise_cat')
    @tornado.web.authenticated
    @required_permissions()
    def delete(self):
        cat_id = self.get_argument('cat_id', None)
        if not cat_id:
            return self.error(msg='参数错误')
        param = {
            'status': -1
        }
        AdvertisingCategoryService.put_data(param, cat_id)
        return self.success()


    @get('/admin/advertise_cat/valid')
    @tornado.web.authenticated
    # @required_permissions()
    def valid(self):
        """
        有效的分类列表
        :return:
        """
        data = AdvertisingCategoryService.data_list_valid()
        return self.success(data=data)

