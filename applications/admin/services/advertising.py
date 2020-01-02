#!/usr/bin/env python
# -*- coding: utf-8 -*-
from trest.utils import utime
from trest.logger import SysLogger
from trest.config import settings
from trest.exception import JsonError
from applications.common.models.advertising import Advertising
from applications.common.models.advertising_category import AdvertisingCategory

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
        if 'category' in where.keys():
            where['category_id'] = AdvertisingCategory.session.query(AdvertisingCategory.id) \
            .filter(AdvertisingCategory.name == where['category']).scalar()

        query = Advertising.Q

        if 'category_id' in where.keys():
            query = query.filter(Advertising.category_id == where['category_id'])

        if 'id' in where.keys():
            query = query.filter(Advertising.id == where['id'])

        if 'title' in where.keys():
            query = query.filter(Advertising.title == where['title'])

        if 'status' in where.keys():
            query = query.filter(Advertising.status == where['status'])
        else:
            query = query.filter(Advertising.status != -1)

        query = query.order_by(Advertising.sort.desc())
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

        if 'start_at' in param.keys():
            param['start_at'] = param['start_at'] if param['start_at'].isnumeric() else 0
        if 'end_at' in param.keys():
            param['end_at'] = param['end_at'] if param['end_at'].isnumeric() else 0

        description = param.get('description', '')
        if len(description) > 255:
            raise JsonError('Data too long for \'description\'')
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

        description = param.get('description', '')
        if len(description) > 255:
            raise JsonError('Data too long for \'description\'')

        if 'start_at' in param.keys():
            param['start_at'] = param['start_at'] if param['start_at'].isnumeric() else 0
        if 'end_at' in param.keys():
            param['end_at'] = param['end_at'] if param['end_at'].isnumeric() else 0
        try:
            obj = Advertising(**param)
            Advertising.session.add(obj)
            Advertising.session.commit()
            return True
        except Exception as e:
            Advertising.session.rollback()
            SysLogger.error(e)
            raise JsonError('insert error')
