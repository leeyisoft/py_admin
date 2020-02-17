#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import or_
from trest.utils import utime
from trest.logger import SysLogger
from trest.config import settings
from trest.exception import JsonError
from applications.common.models.goods import Goods
from applications.common.models.goods_category import GoodsCategory

from ..assemblers.goods  import GoodsAssembler


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
        if 'recommended' in where.keys():
            query = query.filter(Goods.recommended == where['recommended'])

        pagelist_obj = query.paginate(page=page, per_page=per_page)

        if pagelist_obj is None:
            raise JsonError('暂无数据')

        return GoodsAssembler.page_list(pagelist_obj, page, per_page)

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
        obj = Goods.Q.filter(Goods.id == id).filter(Goods.status == 1).first()
        return obj

    @staticmethod
    def list_most_importance(limit):
        """
        Arguments:
            limit int -- 查询记录数

        return:
            list
        """
        rows = Goods.Q \
            .filter(Goods.status == 1) \
            .filter(Goods.recommended == 1) \
            .filter(Goods.thumb['left'] != '') \
            .filter(Goods.thumb['right'] != '') \
            .order_by(Goods.importance.desc()) \
            .limit(limit).all()
        return rows if rows else []

    @staticmethod
    def increase_hits(id):
        try:
            goods = Goods.Update.filter(Goods.id == id).first()
            goods.hits += 1
            Goods.session.commit()
        except Exception as e:
            pass
        return True

