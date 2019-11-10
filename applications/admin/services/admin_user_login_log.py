#!/usr/bin/env python
# -*- coding: utf-8 -*-
from trest.utils import utime
from trest.logger import SysLogger
from trest.config import settings
from trest.exception import JsonError
from applications.common.models.admin_user_login_log import AdminUserLoginLog


class AdminUserLoginLogService:
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
        query = AdminUserLoginLog.Q

        if 'status' in where.keys():
            query = query.filter(AdminUserLoginLog.status == where['status'])
        else:
            query = query.filter(AdminUserLoginLog.status != -1)

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
            AdminUserLoginLog Model 实例 | None
        """
        if not id:
            raise JsonError('ID不能为空')
        obj = AdminUserLoginLog.Q.filter(AdminUserLoginLog.id == id).first()
        return obj

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
            data = AdminUserLoginLog(**param)
            AdminUserLoginLog.session.add(data)
            AdminUserLoginLog.session.commit()
            return True
        except Exception as e:
            AdminUserLoginLog.session.rollback()
            SysLogger.error(e)
            raise JsonError('insert error')
