#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""广告位控制器

[description]
"""

import tornado
from applications.admin.services.notice import NoticeService
from applications.core.decorators import required_permissions
from .common import CommonHandler

from pyrestful.rest import get
from pyrestful.rest import delete
from pyrestful.rest import post
from pyrestful.rest import put

class NoticeHandler(CommonHandler):

    @post('/admin/notice')
    @tornado.web.authenticated
    @required_permissions('admin:notice:add_record')
    def add_record(self):

        title=self.get_argument('title','')
        content=self.get_argument('content','')
        sort=self.get_argument('sort',0)
        status=self.get_argument('status',1)
        operate_id=self.get_argument('operate_id',0)
        lang=self.get_argument('lang','')

        if not title or not content or not sort or not status:
            return self.error('参数错误')

        param={
            'title':title,
            'content':content,
            'status':status,
            'sort':sort,
            'operate_id':operate_id,
            'lang':lang,
        }
        (code,msg)=NoticeService.add_data(param)
        if code==0:
            return self.success()
        else:
            return self.error(msg=msg)


    @get('/admin/notice')
    @tornado.web.authenticated
    @required_permissions('admin:notice:index')
    def index(self):

        page=int(self.get_argument('page',1))
        limit=int(self.get_argument('limit',10))
        title=self.get_argument('title',None)
        status=self.get_argument('status',None)
        lang=self.get_argument('lang',None)
        param={
            'title':title,
            'status':status,
            'lang':lang
        }
        (code,msg,(total,data))=NoticeService.data_list(param,page,limit)
        new=[]
        for val in data:
            notice_data=val.as_dict()
            new.append(notice_data)
        if code==0:
            res={
                'page':page,
                'per_page':limit,
                'total':total,
                'items':new
            }
            return self.success(data=res)
        else:
            return self.error('出错')


    @put('/admin/notice')
    @tornado.web.authenticated
    @required_permissions('admin:notice:put_record')
    def put_record(self):

        title=self.get_argument('title','')
        content=self.get_argument('content','')
        sort=self.get_argument('sort',0)
        status=self.get_argument('status',1)
        notice_id=self.get_argument('notice_id',0)
        operate_id=self.get_argument('operate_id',0)
        lang=self.get_argument('lang','')

        if  not notice_id:
            return self.error('参数错误')
        param={
            'title':title,
            'content':content,
            'status':status,
            'sort':sort,
            'operate_id':operate_id,
            'lang':lang,
        }
        new={}
        for val in param.keys():
            if param[val] and param[val]!=0:
                new[val]=param[val]

        (code,msg)=NoticeService.put_data(new,notice_id)
        if code==0:
            return self.success()
        else:
            return self.error(msg=msg)


    @delete('/admin/notice')
    @tornado.web.authenticated
    @required_permissions('admin:notice:dels')
    def dels(self):
        notice_id=self.get_argument('notice_id',None)

        if not notice_id:
            return self.error(msg='参数错误')

        param={

            'status':-1
        }

        (code,msg)=NoticeService.put_data(param,notice_id)
        if code==0:
            return self.success()
        else:
            return self.error(msg=msg)



