#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
公告管理
"""
from applications.common.models.base import Contract


class ContractService:
    @staticmethod
    def add_data(param):
        code=0
        msg=''

        try:
            data=Contract(**param)
            Contract.session.add(data)
            Contract.session.commit()
            return (code,msg)
        except Exception:
            Contract.session.rollback()
            code=1
            msg='出错'
            return (code,msg)

    @staticmethod
    def data_list(param,page,limit):
        code=0
        msg=''
        res_data=[]

        query=Contract.Q
        if param['name']:
            query=query.filter(Contract.name==param['name'])

        if param['status']:
            query=query.filter(Contract.status==param['status'])

        if param['lang']:
            query=query.filter(Contract.lang==param['lang'])

        query=query.filter(Contract.status!=-1)
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

            Contract.Q.filter(Contract.id==advertise_id).update(param)
            Contract.session.commit()
            return (code,msg)
         except Exception:
            Contract.session.rollback()
            code=1
            msg='出错'
            return (code,msg)

    @staticmethod
    def detail_info(contract_id):
        code=0
        msg=''
        data=Contract.Q.filter(Contract.id==contract_id).first()
        Contract.session.commit()
        if data:
            data=data.as_dict()
        return (code,msg,data)
