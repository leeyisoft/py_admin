#!/usr/bin/env python
# -*- coding: utf-8 -*-
from trest.utils import utime
from trest.logger import SysLogger
from trest.config import settings
from trest.exception import JsonError
from applications.common.models.admin_user_login_log import AdminUserLoginLog


class AdminUserLoginLogService(object):
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
        query = AdminUserLoginLog.Q

        if 'status' in where.keys():
            query = query.filter(AdminUserLoginLog.status == where['status'])
        else:
            query = query.filter(AdminUserLoginLog.status != -1)

        pagelist_obj = query.paginate(page=page, per_page=per_page)
        return pagelist_obj

    @staticmethod
    def get(id):
        """获取单条记录

        [description]

        Arguments:
            id int -- 主键

        return:
            AdminUserLoginLog Model 实例 | None
        """
        if not id:
            raise JsonError('ID不能为空')
        obj = AdminUserLoginLog.Q.filter(AdminUserLoginLog.id == id).first()
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
        columns = [i for (i, _) in AdminUserLoginLog.__table__.columns.items()]
        param = {k:v for k,v in param.items() if k in columns}
        if 'updated_at' in columns:
            param['updated_at'] = utime.timestamp(3)

        if not id:
            raise JsonError('ID 不能为空')

        try:
            AdminUserLoginLog.Update.filter(AdminUserLoginLog.id == id).update(param)
            AdminUserLoginLog.session.commit()
            return True
        except Exception as e:
            AdminUserLoginLog.session.rollback()
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
        columns = [i for (i, _) in AdminUserLoginLog.__table__.columns.items()]
        param = {k:v for k,v in param.items() if k in columns}
        if 'created_at' in columns:
            param['created_at'] = utime.timestamp(3)
        try:
            obj = AdminUserLoginLog(**param)
            AdminUserLoginLog.session.add(obj)
            AdminUserLoginLog.session.commit()
            return True
        except Exception as e:
            AdminUserLoginLog.session.rollback()
            SysLogger.error(e)
            raise JsonError('insert error')
