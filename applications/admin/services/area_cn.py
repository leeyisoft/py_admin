#!/usr/bin/env python
# -*- coding: utf-8 -*-
from trest.utils import utime
from trest.logger import SysLogger
from trest.config import settings
from trest.exception import JsonError
from applications.common.models.area_cn import AreaCn


class AreaCnService:
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
        query = AreaCn.Q

        if 'status' in where.keys():
            query = query.filter(AreaCn.status == where['status'])
        else:
            query = query.filter(AreaCn.status != -1)

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
            AreaCn Model 实例 | None
        """
        if not id:
            raise JsonError('ID不能为空')
        obj = AreaCn.Q.filter(AreaCn.id == id).first()
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
        columns = [i for (i, _) in AreaCn.__table__.columns.items()]
        for key in param.keys():
            if key not in columns:
                param.pop(key, None)

        if 'updated_at' in columns:
            param['updated_at'] = utime.timestamp(3)

        if not id:
            raise JsonError('ID 不能为空')

        try:
            AreaCn.Update.filter(AreaCn.id == id).update(param)
            AreaCn.session.commit()
            return True
        except Exception as e:
            AreaCn.session.rollback()
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
        columns = [i for (i, _) in AreaCn.__table__.columns.items()]
        for key in param.keys():
            if key not in columns:
                param.pop(key, None)
        if 'created_at' in columns:
            param['created_at'] = utime.timestamp(3)
        try:
            data = AreaCn(**param)
            AreaCn.session.add(data)
            AreaCn.session.commit()
            return True
        except Exception as e:
            AreaCn.session.rollback()
            SysLogger.error(e)
            raise JsonError('insert error')
