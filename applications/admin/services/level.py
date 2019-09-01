#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
会员级别
"""
from applications.common.models.member import MemberLevel


class LevelService:
    @staticmethod
    def add_data(param):
        code=0
        msg=''
        try:
            data=MemberLevel(**param)
            MemberLevel.session.add(data)
            MemberLevel.session.commit()
            return (code,msg)
        except Exception:
            MemberLevel.session.rollback()
            code=1
            msg='出错'
            return (code,msg)


    @staticmethod
    def data_list(param,page,limit):
        code=0
        msg=''
        query=MemberLevel.Q
        if param['name']:
            query=query.filter(MemberLevel.name==param['name'])

        if param['status']:
            query=query.filter(MemberLevel.status==param['status'])

        query=query.filter(MemberLevel.status!=-1)
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
            MemberLevel.Q.filter(MemberLevel.id==advertise_id).update(param)
            MemberLevel.session.commit()
            return (code,msg)
         except Exception:
            MemberLevel.session.rollback()
            code=1
            msg='出错'
            return (code,msg)

    @staticmethod
    def valid_level(param):
        code=0
        msg=''
        res_data=[]
        query=MemberLevel.Q.filter(MemberLevel.status==param['status']).all()
        for val in query:
            middle=val.as_dict()
            res_data.append(middle)
        return (code,msg,res_data)

    @staticmethod
    def level_options():
        """
        用户等级选项列表
        :return:
        """
        data = MemberLevel.session.query(MemberLevel.id, MemberLevel.name)\
            .filter(MemberLevel.status == 1).all()
        item_dict = {}
        item_list = []
        if not data:
            return (item_dict, item_list)
        for raw in data:
            temp = {}
            (temp['value'], temp['label']) = raw
            item_list.append(temp)
            item_dict[temp['value']] = temp['label']
        return (item_dict, item_list)
