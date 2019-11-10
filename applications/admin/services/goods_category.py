#!/usr/bin/env python
# -*- coding: utf-8 -*-
from trest.utils import utime
from trest.logger import SysLogger
from trest.config import settings
from trest.exception import JsonError
from applications.common.models.goods_category import GoodsCategory


class GoodsCategoryService:
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
        query = GoodsCategory.Q

        if 'status' in where.keys():
            query = query.filter(GoodsCategory.status == where['status'])
        else:
            query = query.filter(GoodsCategory.status != -1)

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
            GoodsCategory Model 实例 | None
        """
        if not id:
            raise JsonError('ID不能为空')
        obj = GoodsCategory.Q.filter(GoodsCategory.id == id).first()
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
        param['updated_at'] = utime.timestamp(3)

        if not id:
            raise JsonError('ID 不能为空')

        try:
            GoodsCategory.Q.filter(GoodsCategory.id == id).update(param)
            GoodsCategory.session.commit()
            return True
        except Exception as e:
            GoodsCategory.session.rollback()
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
        param['created_at'] = utime.timestamp(3)
        try:
            data = GoodsCategory(**param)
            GoodsCategory.session.add(data)
            GoodsCategory.session.commit()
            return True
        except Exception as e:
            GoodsCategory.session.rollback()
            SysLogger.error(e)
            raise JsonError('insert error')
