#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""用户级别
[description]
"""
import tornado

from trest.router import get
from trest.router import put
from trest.router import post
from trest.router import delete
from trest.exception import JsonError
from trest.config import settings

from applications.admin.services.level import LevelService
from applications.admin.utils import required_permissions
from applications.admin.utils import admin_required_login
from .common import CommonHandler


class LevelHandler(CommonHandler):

    @post('/admin/level')
    @admin_required_login
    @required_permissions()
    def add_record(self):

        name=self.get_argument('name',None)
        min_exper=self.get_argument('min_exper',None)
        max_exper=self.get_argument('max_exper',None)
        intro=self.get_argument('intro',None)
        default=self.get_argument('default',None)
        expire=self.get_argument('expire',None)
        status=self.get_argument('status',1)
        if not name or not min_exper or not max_exper or not status or not intro or not default or not expire:
            return self.error('参数错误')

        param={
            'name':name,
            'min_exper':min_exper,
            'max_exper':max_exper,
            'intro':intro,
            'status':status,
            'default':default,
            'expire':expire
        }
        (code,msg)=LevelService.add_data(param)
        if code==0:
            return self.success()
        else:
            return self.error(msg=msg)


    @get('/admin/level')
    @admin_required_login
    @required_permissions()
    def index(self):

        page=int(self.get_argument('page',1))
        limit=int(self.get_argument('limit',10))
        title=self.get_argument('title',None)
        status=self.get_argument('status',None)
        param={
            'name':title,
            'status':status,
        }

        (code,msg,(total,data))=LevelService.data_list(param,page,limit)
        new=[]
        for val in data:
            notice_data=val.as_dict()
            new.append(notice_data)
        if code==0:
            resp = {
                'page':page,
                'per_page':limit,
                'total':total,
                'items':new
            }
            return self.success(data=res)
        else:
            return self.error('出错')


    @get('/admin/level/valid')
    @admin_required_login
    @required_permissions()
    def valid(self):
        """
        查询有效的等级
        :return:
        """
        param={
            'status':1,
        }
        (code,msg,data)=LevelService.valid_level(param)
        if code==0:
            return self.success(data=data)
        else:
            return self.error('出错')


    @put('/admin/level')
    @admin_required_login
    @required_permissions()
    def put_record(self):

        name=self.get_argument('name',None)
        min_exper=self.get_argument('min_exper',None)
        max_exper=self.get_argument('max_exper',None)
        intro=self.get_argument('intro',None)
        default=self.get_argument('default',None)
        expire=self.get_argument('expire',None)
        status=self.get_argument('status',1)
        level_id=self.get_argument('level_id',0)
        if  not level_id:
            return self.error('参数错误')

        param={
            'name':name,
            'min_exper':min_exper,
            'max_exper':max_exper,
            'intro':intro,
            'status':status,
            'default':default,
            'expire':expire
        }
        new={}
        for val in param.keys():
            if param[val] and param[val]!=0:
                new[val]=param[val]

        (code,msg)=LevelService.put_data(new,level_id)
        if code==0:
            return self.success()
        else:
            return self.error(msg=msg)


    @delete('/admin/level')
    @admin_required_login
    @required_permissions()
    def dels(self):
        level_id=self.get_argument('level_id',None)
        if not level_id:
            return self.error(msg='参数错误')
        param={
            'status':-1
        }
        (code,msg)=LevelService.put_data(param,level_id)
        if code==0:
            return self.success()
        else:
            return self.error(msg=msg)



