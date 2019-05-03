#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
公告管理
"""
from applications.common.models.base import Notice


class NoticeService:
    @staticmethod
    def add_data(param):
        code=0
        msg=''
        try:
            data=Notice(**param)
            Notice.session.add(data)
            Notice.session.commit()
            return (code,msg)
        except Exception:
            Notice.session.rollback()
            code=1
            msg='出错'
            return (code,msg)


    @staticmethod
    def data_list(param,page,limit):
        code=0
        msg=''
        res_data=[]
        query=Notice.Q
        if param['title']:
            query=query.filter(Notice.title==param['title'])

        if param['status']:
            query=query.filter(Notice.status==param['status'])

        if param['lang']:
            query=query.filter(Notice.lang==param['lang'])

        query=query.filter(Notice.status!=-1)
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

            Notice.Q.filter(Notice.id==advertise_id).update(param)
            Notice.session.commit()
            return (code,msg)

         except Exception:

            Notice.session.rollback()
            code=1
            msg='出错'
            return (code,msg)
