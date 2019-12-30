#!/usr/bin/env python
# -*- coding: utf-8 -*-
from trest.utils import utime
from trest.logger import SysLogger
from trest.config import settings
from trest.exception import JsonError
from applications.common.models.goods import Goods
from applications.admin.services.goods_category import GoodsCategoryService
from applications.admin.filters.goods  import GoodsFilter


class GoodsService(object):
    @staticmethod
    def page_list(where, page, per_page):
        """列表记录
        Arguments:
            where dict -- 查询条件
            page int -- 当前页
            per_page int -- 每页记录数

        return:
            Paginate 对象 | None
        """
        query = Goods.Q

        if 'id' in where.keys():
            query = query.filter(Goods.id == where['id'])
        if 'title' in where.keys():
            query = query.filter(Goods.title == where['title'])
        if 'status' in where.keys():
            query = query.filter(Goods.status == where['status'])
        else:
            query = query.filter(Goods.status != -1)

        pagelist_obj = query.paginate(page=page, per_page=per_page)

        if pagelist_obj is None:
            raise JsonError('暂无数据')
        category_map = {}
        category_ids = [obj.category_id for obj in pagelist_obj.items]
        category_list = GoodsCategoryService.category_list(category_ids)
        for category in category_list:
            category_map[category.id] = category
        return GoodsFilter.page_list(pagelist_obj, page, per_page, category_map)

    @staticmethod
    def get(id):
        """获取单条记录

        [description]

        Arguments:
            id int -- 主键

        return:
            Goods Model 实例 | None
        """
        if not id:
            raise JsonError('ID不能为空')
        obj = Goods.Q.filter(Goods.id == id).first()
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
        columns = [i for (i, _) in Goods.__table__.columns.items()]
        param = {k:v for k,v in param.items() if k in columns}
        if 'updated_at' in columns:
            param['updated_at'] = utime.timestamp(3)

        if not id:
            raise JsonError('ID 不能为空')

        try:
            Goods.Update.filter(Goods.id == id).update(param)
            Goods.session.commit()
            return True
        except Exception as e:
            Goods.session.rollback()
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
        columns = [i for (i, _) in Goods.__table__.columns.items()]
        param = {k:v for k,v in param.items() if k in columns}
        if 'created_at' in columns:
            param['created_at'] = utime.timestamp(3)
        try:
            obj = Goods(**param)
            Goods.session.add(obj)
            Goods.session.commit()
            return True
        except Exception as e:
            Goods.session.rollback()
            SysLogger.error(e)
            raise JsonError('insert error')
