#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import or_
from trest.utils import utime
from trest.logger import SysLogger
from trest.config import settings
from trest.exception import JsonError
from applications.common.models.goods import Goods
from applications.common.models.goods_category import GoodsCategory

from applications.admin.filters.goods  import GoodsFilter


class GoodsService(object):
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
