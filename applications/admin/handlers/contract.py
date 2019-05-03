#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""合同控制器

[description]
"""

import tornado
import base64
from applications.admin.services.contract import ContractService
from applications.core.decorators import required_permissions
from .common import CommonHandler

from pyrestful.rest import get
from pyrestful.rest import delete
from pyrestful.rest import post
from pyrestful.rest import put

class ContractHandler(CommonHandler):

    @post('/admin/contract')
    @tornado.web.authenticated
    @required_permissions('admin:contract:add_record')
    def add_record(self):

        name=self.get_argument('name','')
        content=self.get_argument('content','')
        status=self.get_argument('status',1)
        type=self.get_argument('type',1)
        operate_id=self.get_argument('operate_id',0)
        lang=self.get_argument('lang','')

        if not name or not content or not type or not status or not operate_id:
            return self.error('参数错误')

        param={

            'name':name,
            'content':content,
            'status':status,
            'type':type,
            'operate_id':operate_id,
            'lang':lang,

        }

        (code,msg)=ContractService.add_data(param)
        if code==0:
            return self.success()
        else:
            return self.error(msg=msg)


    @get('/admin/contract')
    @tornado.web.authenticated
    @required_permissions('admin:contract:index')
    def index(self):

        page=int(self.get_argument('page',1))
        limit=int(self.get_argument('limit',10))
        name=self.get_argument('name',None)
        status=self.get_argument('status',None)
        lang=self.get_argument('lang',None)
        param={
            'name':name,
            'status':status,
            'lang':lang
        }

        (code,msg,(total,data))=ContractService.data_list(param,page,limit)
        new=[]
        for val in data:
            contract_data=val.as_dict()
            new.append(contract_data)
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


    @get('/admin/contract/{contract_id}')
    @tornado.web.authenticated
    @required_permissions('admin:contract:detail')
    def detail(self,contract_id):
        (code,msg,data)=ContractService.detail_info(contract_id)

        if code==0:
            return self.success(data=data)
        else:
            return self.error('出错')


    @put('/admin/contract')
    @tornado.web.authenticated
    @required_permissions('admin:contract:put_record')
    def put_record(self):

        name=self.get_argument('name','')
        content=self.get_argument('content','')
        status=self.get_argument('status',1)
        type=self.get_argument('type',1)
        operate_id=self.get_argument('operate_id',0)
        lang=self.get_argument('lang','')
        contract_id=self.get_argument('contract_id',0)

        if  not contract_id:
            return self.error('参数错误')


        param={

            'name':name,
            'content':content,
            'status':status,
            'type':type,
            'operate_id':operate_id,
            'lang':lang,

        }

        new={}
        for val in param.keys():
            if param[val] and param[val]!=0:
                new[val]=param[val]

        (code,msg)=ContractService.put_data(new,contract_id)
        if code==0:
            return self.success()
        else:
            return self.error(msg=msg)


    @delete('/admin/contract')
    @tornado.web.authenticated
    @required_permissions('admin:contract:dels')
    def dels(self):
        contract_id=self.get_argument('contract_id',None)

        if not contract_id:
            return self.error(msg='参数错误')

        param={

            'status':-1
        }

        (code,msg)=ContractService.put_data(param,contract_id)
        if code==0:
            return self.success()
        else:
            return self.error(msg=msg)



    @get('/generate/pdf')
    def pdf_generate(self):
        from applications.core.utils.generate_pdf import HTML2PDF
        (code,msg,data)=ContractService.detail_info(6)
        html=data['content']
        a=HTML2PDF.generate_html2pdf(html,'hello')

        #
        # html_e=bytes(html, encoding = "utf-8")
        #
        # html_=base64.b64encode(html_e)

        self.set_header('Content-Type','application/pdf')
        self.set_header('Content-Disposition','inline')

        # html_o=str(html_, encoding = "utf-8")

        self.write(html)
        # return self.finish()
