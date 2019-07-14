#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
广告位分类管理
"""
from applications.common.models.base import AdvertisingCategory
from trest.exception import JsonError
class AdvertisingCategoryService:

    @staticmethod
    def add_data(param):
        check = AdvertisingCategory.Q.filter(AdvertisingCategory.name == param['name']).first()
        if check:
            raise JsonError('分类名称存在')
        try:
            data = AdvertisingCategory(**param)
            AdvertisingCategory.session.add(data)
            AdvertisingCategory.session.commit()
            return True
        except Exception as e:
            AdvertisingCategory.session.rollback()
            raise e


    @staticmethod
    def data_list(param,page,limit):
        query = AdvertisingCategory.Q
        if param['status']:
            query = query.filter(AdvertisingCategory.status == param['status'])

        if param['lang']:
            query = query.filter(AdvertisingCategory.lang == param['lang'])

        query = query.filter(AdvertisingCategory.status != -1)
        pagelist_obj = query.paginate(page=page, per_page=limit)
        if pagelist_obj is None:
            raise JsonError('暂无数据')
        return pagelist_obj


    @staticmethod
    def data_list_valid():
        res_data = []
        query=AdvertisingCategory.Q.filter(AdvertisingCategory.status==1).all()
        AdvertisingCategory.session.commit()
        for val in query:
            res_data.append(val.as_dict())
        return res_data


    @staticmethod
    def put_data(param, advertise_id):
         try:
             AdvertisingCategory.Q.filter(AdvertisingCategory.id == advertise_id).update(param)
             AdvertisingCategory.session.commit()
         except Exception as e:
             AdvertisingCategory.session.rollback()
             raise e
         return True
