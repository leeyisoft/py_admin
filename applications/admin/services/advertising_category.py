#!/usr/bin/env python
# -*- coding: utf-8 -*-
from trest.utils import utime
from trest.logger import SysLogger
from trest.config import settings
from trest.exception import JsonError
from applications.common.models.advertising_category import AdvertisingCategory


class AdvertisingCategoryService:
    @staticmethod
    def data_list(where, page, per_page):
        """列表记录
        Arguments:
            where dict -- 查询条件
            page int -- 当前页
            per_page int -- 每页记录数

        return:
            Paginate 对象 | None
        """
        query = AdvertisingCategory.Q

        if 'status' in where.keys():
            query = query.filter(AdvertisingCategory.status == where['status'])
        else:
            query = query.filter(AdvertisingCategory.status != -1)

        pagelist_obj = query.paginate(page=page, per_page=per_page)
        if pagelist_obj is None:
            raise JsonError('暂无数据')
        return pagelist_obj

    @staticmethod
    def get(id):
        """获取单条记录

        [description]

        Arguments:
            id int -- 主键

        return:
            AdvertisingCategory Model 实例 | None
        """
        if not id:
            raise JsonError('ID不能为空')
        obj = AdvertisingCategory.Q.filter(AdvertisingCategory.id == id).first()
        return obj

    @staticmethod
    def update(id, param):
        """更新记录

        [description]

        Arguments:
            id int -- 主键
            param dict -- [description]

        return:
            True | JsonError
        """
        param.pop('_xsrf', None)
        param.pop('file', None)
        param.pop('id', None)

        if not id:
            raise JsonError('ID 不能为空')

        try:
            AdvertisingCategory.Q.filter(AdvertisingCategory.id == id).update(param)
            AdvertisingCategory.session.commit()
            return True
        except Exception as e:
            AdvertisingCategory.session.rollback()
            SysLogger.error(e)
            raise JsonError('update error')

    @staticmethod
    def insert(param):
        """插入

        [description]

        Arguments:
            id int -- 主键
            param dict -- [description]

        return:
            True | JsonError
        """
        param.pop('_xsrf', None)
        try:
            data = AdvertisingCategory(**param)
            AdvertisingCategory.session.add(data)
            AdvertisingCategory.session.commit()
            return True
        except Exception as e:
            AdvertisingCategory.session.rollback()
            SysLogger.error(e)
            raise JsonError('insert error')

    @staticmethod
    def data_list_valid():
        res_data = []
        query = AdvertisingCategory.Q.filter(AdvertisingCategory.status==1).all()
        AdvertisingCategory.session.commit()
        for val in query:
            res_data.append(val.as_dict())
        return res_data
