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
from trest.config import settings

from applications.admin.services.advertise import AdvertisingService
from applications.admin.utils import required_permissions
from applications.admin.utils import admin_required_login
from trest.utils.file import Uploader
from applications.common.models.base import AdvertisingCategory

from .common import CommonHandler


class AdvertisingHandler(CommonHandler):

    @post('/admin/advertising')
    @admin_required_login
    @required_permissions()
    def advertising_post(self):
        """
        新增广告
        """
        title=self.get_argument('title',None)
        start_at=self.get_argument('start_at',None)
        end_at=self.get_argument('end_at',-1)
        #广告类型 1.链接 2.外链
        type=self.get_argument('type',1)
        img=self.get_argument('img_url',None)
        link=self.get_argument('link',None)
        category_id=self.get_argument('category_id',None)
        status=self.get_argument('status',1)

        if not title or not start_at or not end_at or not img or not category_id or not client:
            return self.error('参数错误')

        param={
            'title':title,
            'start_at':start_at,
            'end_at':end_at,
            'type':type,
            'img':img,
            'link':link,
            'category_id':category_id,
            'status':status
        }
        AdvertisingService.add_data(param)
        return self.success()


    @get('/admin/advertising')
    @admin_required_login
    @required_permissions()
    def advertising_get(self):
        page=int(self.get_argument('page',1))
        limit=int(self.get_argument('limit',10))
        title=self.get_argument('title',None)
        status=self.get_argument('status',None)

        param={}
        if title:
            param['title'] = title
        if status:
            param['status'] = status

        pagelist_obj=AdvertisingService.data_list(param,page,limit)
        items=[]
        for val in pagelist_obj.items:
            if val is not None:
                data=val.as_dict()
                category_info= AdvertisingCategory.Q.filter(AdvertisingCategory.id==data['category_id']).first()
                if category_info is not None:
                    data['category']=category_info.as_dict()['name']
                else:
                    data['category']=''
                items.append(data)
        resp = {
            'page':page,
            'per_page':limit,
            'total':pagelist_obj.total,
            'items':items,
        }
        return self.success(data = resp)

    @put('/admin/advertising')
    @admin_required_login
    @required_permissions()
    def advertising_put(self):
        """
        修改广告位
        """
        title=self.get_argument('title',None)
        start_at=self.get_argument('start_at',None)
        end_at=self.get_argument('end_at',-1)
        #广告类型 1.链接 2.外链
        type=self.get_argument('type',1)
        img=self.get_argument('img_url',None)
        link=self.get_argument('link',None)
        advertise_id=self.get_argument('advertise_id',None)
        status=self.get_argument('status',1)
        category_id = self.get_argument('category_id', None)

        if not advertise_id:
            return self.error('参数错误')
        param = {
            'title':title,
            'start_at':start_at,
            'end_at':end_at,
            'type':type,
            'img':img,
            'link':link,
            'category_id':category_id,
            'status':status,
        }
        AdvertisingService.put_data(param, advertise_id)
        return self.success()

    @delete('/admin/advertising')
    @admin_required_login
    @required_permissions()
    def advertising_delete(self):
        advertise_id = self.get_argument('advertise_id', None)
        if not advertise_id:
            return self.error(msg='参数错误')
        param = {
            'status':-1
        }
        AdvertisingService.put_data(param, advertise_id)
        return self.success()
