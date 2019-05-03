#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
广告位分类管理
"""
from applications.common.models.base import AdvertisingCategory

class AdvertisingCategoryService:

    @staticmethod
    def add_data(param):
        code=0
        msg=''

        check=AdvertisingCategory.Q.filter(AdvertisingCategory.name==param['name']).first()
        if check:
            code=1
            msg='分类名称存在'
            return (code,msg)

        try:
            data=AdvertisingCategory(**param)
            AdvertisingCategory.session.add(data)
            AdvertisingCategory.session.commit()
            return (code,msg)
        except Exception:
            AdvertisingCategory.session.rollback()
            code=1
            msg='出错'
            return (code,msg)


    @staticmethod
    def data_list(param,page,limit):
        code=0
        msg=''

        query=AdvertisingCategory.Q
        if param['status']:
            query=query.filter(AdvertisingCategory.status==param['status'])

        if param['lang']:
            query=query.filter(AdvertisingCategory.lang==param['lang'])

        query=query.filter(AdvertisingCategory.status!=-1)
        pagelist_obj = query.paginate(page=page, per_page=limit)
        if pagelist_obj is None:
            code = 1
            msg = "暂无数据"
        else:
            resdata = (pagelist_obj.total, pagelist_obj.items)
        return (code, msg, resdata)


    @staticmethod
    def data_list_valid():
        code=0
        msg=''
        res_data=[]

        query=AdvertisingCategory.Q.filter(AdvertisingCategory.status==1).all()
        AdvertisingCategory.session.commit()
        for val in query:
            res_data.append(val.as_dict())
        return (code,msg,res_data)


    @staticmethod
    def put_data(param,advertise_id):
         code=0
         msg=''

         try:

            AdvertisingCategory.Q.filter(AdvertisingCategory.id==advertise_id).update(param)
            AdvertisingCategory.session.commit()
            return (code,msg)

         except Exception:

            AdvertisingCategory.session.rollback()
            code=1
            msg='出错'
            return (code,msg)
