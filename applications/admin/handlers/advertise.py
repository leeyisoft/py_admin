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
from trest.utils.file import Uploader
from applications.common.models.base import AdvertisingCategory

from .common import CommonHandler


class AdvertiseHandler(CommonHandler):

    # @post('/admin/advertise')
    # @tornado.web.authenticated
    # @required_permissions()
    # def add(self):
    #     """
    #     新增广告
    #     """
    #     lang=self.get_argument('lang','en')
    #     title=self.get_argument('title',None)
    #     start_at=self.get_argument('start_at',None)
    #     end_at=self.get_argument('end_at',-1)
    #     #广告类型 1.链接 2.外链
    #     type=self.get_argument('type',1)
    #     client=self.get_argument('client',None)
    #     img=self.get_argument('img_url',None)
    #     link=self.get_argument('link',None)
    #     effects=self.get_argument('effects',None)
    #     category_id=self.get_argument('category_id',None)
    #     status=self.get_argument('status',1)

    #     if not title or not start_at or not end_at or not img or not category_id or not client:
    #         return self.error('参数错误')

    #     param={
    #         'lang':lang,
    #         'title':title,
    #         'start_at':start_at,
    #         'end_at':end_at,
    #         'type':type,
    #         'client':client,
    #         'img':img,
    #         'link':link,
    #         'effects':effects,
    #         'category_id':category_id,
    #         'status':status
    #     }
    #     AdvertisingService.add_data(param)
    #     return self.success()

    # @post('/admin/advertise/upfile')
    # @tornado.web.authenticated
    # def upfile(self):
    #     """
    #     上传图片
    #     """
    #     files=self.request.files
    #     if files['img'] is None:
    #         return self.error('参数错误')
    #     img=files['img'][0]
    #     path=Uploader.oss(img, 'advertise')
    #     return self.success(data=path)

    @get('/admin/advertise')
    @tornado.web.authenticated
    @required_permissions()
    def index(self):
        page=int(self.get_argument('page',1))
        limit=int(self.get_argument('limit',10))
        title=self.get_argument('title',None)
        status=self.get_argument('status',None)
        lang=self.get_argument('lang',None)

        param={}
        if title:
            param['title'] = title
        if status:
            param['status'] = status
        if lang:
            param['lang'] = lang
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
        res={
            'page':page,
            'per_page':limit,
            'total':pagelist_obj.total,
            'items':items,
        }
        return self.success(data=res)

    # @put('/admin/advertise')
    # @tornado.web.authenticated
    # @required_permissions()
    # def edit(self):
    #     """
    #     修改广告位
    #     """
    #     lang=self.get_argument('lang','en')
    #     title=self.get_argument('title',None)
    #     start_at=self.get_argument('start_at',None)
    #     end_at=self.get_argument('end_at',-1)
    #     #广告类型 1.链接 2.外链
    #     type=self.get_argument('type',1)
    #     client=self.get_argument('client',None)
    #     img=self.get_argument('img_url',None)
    #     link=self.get_argument('link',None)
    #     effects=self.get_argument('effects',None)
    #     advertise_id=self.get_argument('advertise_id',None)
    #     status=self.get_argument('status',1)
    #     category_id = self.get_argument('category_id', None)

    #     if not advertise_id:
    #         return self.error('参数错误')
    #     param={
    #         'lang':lang,
    #         'title':title,
    #         'start_at':start_at,
    #         'end_at':end_at,
    #         'type':type,
    #         'client':client,
    #         'img':img,
    #         'link':link,
    #         'effects':effects,
    #         'category_id':category_id,
    #         'status':status,
    #     }
    #     AdvertisingService.put_data(param, advertise_id)
    #     return self.success()

    # @delete('/admin/advertise')
    # @tornado.web.authenticated
    # @required_permissions()
    # def delete(self):
    #     ads_id=self.get_argument('ads_id', None)
    #     if not ads_id:
    #         return self.error(msg='参数错误')
    #     param={
    #         'status':-1
    #     }
    #     AdvertisingService.put_data(param,ads_id)
    #     return self.success()
