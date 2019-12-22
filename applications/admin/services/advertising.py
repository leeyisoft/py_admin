#!/usr/bin/env python
# -*- coding: utf-8 -*-
from trest.utils import utime
from trest.logger import SysLogger
from trest.config import settings
from trest.exception import JsonError
from applications.common.models.advertising import Advertising

from applications.admin.filters.advertising  import AdvertisingFilter
from applications.admin.services.advertising_category import AdvertisingCategoryService


class AdvertisingService(object):
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
        query = Advertising.Q

        if 'status' in where.keys():
            query = query.filter(Advertising.status == where['status'])
        else:
            query = query.filter(Advertising.status != -1)

        pagelist_obj = query.paginate(page=page, per_page=per_page)

        if pagelist_obj is None:
            raise JsonError('暂无数据')
        category_map = {}
        category_ids = [obj.category_id for obj in pagelist_obj.items]
        category_list = AdvertisingCategoryService.category_list(category_ids)
        for category in category_list:
            category_map[category.id] = category
        return AdvertisingFilter.page_list(pagelist_obj, page, per_page, category_map)

    @staticmethod
    def get(id):
        """获取单条记录

        [description]

        Arguments:
            id int -- 主键

        return:
            Advertising Model 实例 | None
        """
        if not id:
            raise JsonError('ID不能为空')
        obj = Advertising.Q.filter(Advertising.id == id).first()
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
        columns = [i for (i, _) in Advertising.__table__.columns.items()]
        param = {k:v for k,v in param.items() if k in columns}

        if 'updated_at' in columns:
            param['updated_at'] = utime.timestamp(3)

        if not id:
            raise JsonError('ID 不能为空')

        try:
            Advertising.Update.filter(Advertising.id == id).update(param)
            Advertising.session.commit()
            return True
        except Exception as e:
            Advertising.session.rollback()
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
        columns = [i for (i, _) in Advertising.__table__.columns.items()]
        param = {k:v for k,v in param.items() if k in columns}
        if 'created_at' in columns:
            param['created_at'] = utime.timestamp(3)
        try:
            obj = Advertising(**param)
            Advertising.session.add(obj)
            Advertising.session.commit()
            return True
        except Exception as e:
            Advertising.session.rollback()
            SysLogger.error(e)
            raise JsonError('insert error')
