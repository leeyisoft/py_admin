#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
帮助管理
"""
from applications.common.models.loan import LoanHelp


class HelpService:
    @staticmethod
    def add_data(param):
        code=0
        msg=''
        try:
            data=LoanHelp(**param)
            LoanHelp.session.add(data)
            LoanHelp.session.commit()
            return (code,msg)
        except Exception:
            LoanHelp.session.rollback()
            code=1
            msg='出错'
            return (code,msg)

    @staticmethod
    def data_list(param,page,limit):
        code=0
        msg=''
        res_data=[]

        query=LoanHelp.Q
        if param['title']:
            query=query.filter(LoanHelp.title==param['title'])

        if param['status']:
            query=query.filter(LoanHelp.status==param['status'])

        if param['lang']:
            query=query.filter(LoanHelp.lang==param['lang'])

        query=query.filter(LoanHelp.status!=-1)
        pagelist_obj = query.paginate(page=page, per_page=limit)
        if pagelist_obj is None:
            code = 1
            msg = "暂无数据"
        else:
            resdata = (pagelist_obj.total, pagelist_obj.items)
        return (code, msg, resdata)


    @staticmethod
    def put_data(param,advertise_id):
         code=0
         msg=''
         try:
            LoanHelp.Q.filter(LoanHelp.id==advertise_id).update(param)
            LoanHelp.session.commit()
            return (code,msg)
         except Exception:
            LoanHelp.session.rollback()
            code=1
            msg='出错'
            return (code,msg)
