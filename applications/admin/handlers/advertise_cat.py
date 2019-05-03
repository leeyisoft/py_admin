#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""广告位控制器

[description]
"""

import tornado
from applications.admin.services.advertise_category import AdvertisingCategoryService
from applications.core.decorators import required_permissions

from .common import CommonHandler

from pyrestful.rest import get
from pyrestful.rest import delete
from pyrestful.rest import post
from pyrestful.rest import put

class AdvertiseCatHandler(CommonHandler):

    @get('/admin/advertise_cat')
    @tornado.web.authenticated
    @required_permissions('admin:advertise_cat:index')
    def index(self):
        """
        广告位分类
        :return:
        """
        page=int(self.get_argument('page',1))
        limit=int(self.get_argument('limit',10))
        status=self.get_argument('status',None)
        lang=self.get_argument('lang',None)

        param={
            'status':status,
            'lang':lang
        }
        (code,msg,(total,data))=AdvertisingCategoryService.data_list(param,page,limit)
        if code==0:
            new=[]
            for val in data:
                middle=val.as_dict()
                new.append(middle)
            res={
                'page':page,
                'per_page':limit,
                'total':total,
                'items':new
            }
            return self.success(data=res)
        else:
            return self.error('出错')


    @post('/admin/advertise_cat/add_record')
    @tornado.web.authenticated
    @required_permissions('admin:advertise_cat:add_record')
    def add_record(self):
        """
        新增广告位分类
        """
        lang=self.get_argument('lang','en')
        name=self.get_argument('name',None)
        status=self.get_argument('status',1)

        if not name or not status:
            return self.error('参数错误')


        param={
            'lang':lang,
            'name':name,
            'status':status,

        }

        (code,msg)=AdvertisingCategoryService.add_data(param)
        if code==0:
            return self.success()
        else:
            return self.error(msg=msg)


    @put('/admin/advertise_cat/edit_record')
    @tornado.web.authenticated
    @required_permissions('admin:advertise_cat:edit_record')
    def edit_record(self):
        """
        修改广告位分类
        """
        lang=self.get_argument('lang','en')
        name=self.get_argument('name',None)
        status=self.get_argument('status',1)
        cat_id=self.get_argument('cat_id',None)

        if not cat_id:
            return self.error('参数错误')


        param={
            'lang':lang,
            'name':name,
            'status':status,

        }

        new={}
        for val in param.keys():
            if param[val] and param[val]!=0:
                new[val]=param[val]


        (code,msg)=AdvertisingCategoryService.put_data(new,cat_id)
        if code==0:
            return self.success()
        else:
            return self.error(msg=msg)


    @delete('/admin/advertise_cat/dels')
    @tornado.web.authenticated
    @required_permissions('admin:advertise_cat:dels')
    def dels(self):
        cat_id=self.get_argument('cat_id',None)

        if not cat_id:
            return self.error(msg='参数错误')

        param={

            'status':-1
        }

        (code,msg)=AdvertisingCategoryService.put_data(param,cat_id)
        if code==0:
            return self.success()
        else:
            return self.error(msg=msg)


    @get('/admin/advertise_cat/valid')
    @tornado.web.authenticated
    @required_permissions('admin:advertise_cat:valid')
    def valid(self):
        """
        有效的分类列表
        :return:
        """

        (code,msg,data)=AdvertisingCategoryService.data_list_valid()
        if code==0:

            return self.success(data=data)

        else:
            return self.error('出错')
