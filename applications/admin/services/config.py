#!/usr/bin/env python
# -*- coding: utf-8 -*-
from trest.utils import utime
from trest.logger import SysLogger
from trest.config import settings
from trest.exception import JsonError
from applications.common.models.config import Config


class ConfigService(object):
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
        query = Config.Q

        if 'key' in where.keys():
            query = query.filter(Config.key == where['key'])
        if 'tab' in where.keys():
            query = query.filter(Config.tab == where['tab'])
        if 'status' in where.keys():
            query = query.filter(Config.status == where['status'])
        else:
            query = query.filter(Config.status != -1)

        pagelist_obj = query.paginate(page=page, per_page=per_page)
        return pagelist_obj

    @staticmethod
    def get(key):
        """获取单条记录

        [description]

        Arguments:
            key string -- 主键

        return:
            Config Model 实例 | None
        """
        if not key:
            raise JsonError('key不能为空')
        obj = Config.Q.filter(Config.key == key).first()
        return obj

    @staticmethod
    def update(key, param):
        """更新记录

        [description]

        Arguments:
            key string -- 主键
            param dict -- [description]

        return:
            True | JsonError
        """
        columns = [i for (i, _) in Config.__table__.columns.items()]
        param = {k:v for k,v in param.items() if k in columns}
        if 'updated_at' in columns:
            param['updated_at'] = utime.timestamp(3)

        if not key:
            raise JsonError('key 不能为空')

        try:
            Config.Update.filter(Config.key == key).update(param)
            Config.session.commit()
            return True
        except Exception as e:
            Config.session.rollback()
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
        columns = [i for (i, _) in Config.__table__.columns.items()]
        param = {k:v for k,v in param.items() if k in columns}
        if 'created_at' in columns:
            param['created_at'] = utime.timestamp(3)
        try:
            obj = Config(**param)
            Config.session.add(obj)
            Config.session.commit()
            return True
        except Exception as e:
            Config.session.rollback()
            SysLogger.error(e)
            raise JsonError('insert error')
