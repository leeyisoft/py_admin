#!/usr/bin/env python
# -*- coding: utf-8 -*-
from trest.utils import utime
from trest.config import settings
from trest.logger import SysLogger
from trest.exception import JsonError
from applications.common.models.friendlink import Friendlink


class FriendlinkService(object):
    @staticmethod
    def get(id):
        """获取单条记录

        [description]

        Arguments:
            id int -- 主键

        return:
            Friendlink Model 实例 | None
        """
        if not id:
            raise JsonError('ID不能为空')
        obj = Friendlink.Q.filter(Friendlink.id == id).first()
        return obj

    @staticmethod
    def get_list(where, limit = 12):
        """列表记录
        Arguments:
            where dict -- 查询条件
            page int -- 当前页
            per_page int -- 每页记录数

        return:
            Paginate 对象 | None
        """
        query = Friendlink.Q

        if 'status' in where.keys():
            query = query.filter(Friendlink.status == where['status'])
        else:
            query = query.filter(Friendlink.status != -1)

        query = query.order_by(Friendlink.sort.desc())
        rows = query.limit(limit).all()
        return rows if rows else []
