#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
广告位管理
"""
from pyrestful.rest import JsonError
from applications.core.utils import utime
from applications.common.models.base import Advertising
from applications.common.models.base import AdvertisingCategory


class AdvertisingService:
    @staticmethod
    def add_data(param):
        try:
            data=Advertising(**param)
            Advertising.session.add(data)
            Advertising.session.commit()
            return True
        except Exception as e:
            Advertising.session.rollback()
            raise e

    @staticmethod
    def data_list(param,page,limit):
        query=Advertising.Q
        if 'title' in param.keys():
            query=query.filter(Advertising.title==param['title'])

        if 'status' in param.keys():
            query=query.filter(Advertising.status==param['status'])

        if 'lang' in param.keys():
            query=query.filter(Advertising.lang==param['lang'])

        query=query.filter(Advertising.status!=-1)
        pagelist_obj = query.order_by(Advertising.created_at.desc()).paginate(page=page, per_page=limit)
        if pagelist_obj is None:
            raise JsonError('暂无数据')
        return pagelist_obj

    @staticmethod
    def put_data(param, advertise_id):
         try:
            Advertising.Q.filter(Advertising.id==advertise_id).update(param)
            Advertising.session.commit()
            return True
         except Exception as e:
            raise e
