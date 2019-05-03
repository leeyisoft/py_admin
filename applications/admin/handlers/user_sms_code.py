#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

[description]
"""
import os
import tornado
from applications.admin.services.user_sms_code import UserSmsCodeService
from applications.core.decorators import required_permissions

from .common import CommonHandler
from pyrestful.rest import get

class UserSmsCodeHandler(CommonHandler):

    @get('/admin/user_sms_code')
    @tornado.web.authenticated
    @required_permissions('admin:user_sms_code:index')
    def index(self):

        page=int(self.get_argument('page',1))
        limit=int(self.get_argument('limit',10))
        mobile=self.get_argument('mobile',None)
        param={
            'mobile':mobile,
        }
        (code,msg,(total,data))=UserSmsCodeService.data_list(param,page,limit)
        if code==0:
            field=['platform','mobile','code','user_id','message','created_at','client']
            new=[]
            for val in data:
                middle=val.as_dict(field)
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
