#!/usr/bin/env python
# -*- coding: utf-8 -*-
from trest.utils import utime
from trest.logger import SysLogger
from trest.config import settings
from trest.exception import JsonError
from applications.common.models.admin_role import AdminRole


class AdminRoleService:
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
        query = AdminRole.Q

        if 'status' in where.keys():
            query = query.filter(AdminRole.status == where['status'])
        else:
            query = query.filter(AdminRole.status != -1)

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
            AdminRole Model 实例 | None
        """
        if not id:
            raise JsonError('ID不能为空')
        obj = AdminRole.Q.filter(AdminRole.id == id).first()
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
        columns = [i for (i, _) in AdminRole.__table__.columns.items()]
        for key in param.keys():
            if key not in columns:
                param.pop(key, None)

        if 'updated_at' in columns:
            param['updated_at'] = utime.timestamp(3)

        if not id:
            raise JsonError('ID 不能为空')

        try:
            AdminRole.Q.filter(AdminRole.id == id).update(param)
            AdminRole.session.commit()
            return True
        except Exception as e:
            AdminRole.session.rollback()
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
        columns = [i for (i, _) in AdminRole.__table__.columns.items()]
        for key in param.keys():
            if key not in columns:
                param.pop(key, None)
        if 'created_at' in columns:
            param['created_at'] = utime.timestamp(3)
        try:
            data = AdminRole(**param)
            AdminRole.session.add(data)
            AdminRole.session.commit()
            return True
        except Exception as e:
            AdminRole.session.rollback()
            SysLogger.error(e)
            raise JsonError('insert error')

    @staticmethod
    def get_valid_role():
        """获取有效的角色"""
        data = []
        role = AdminRole.Q.filter(AdminRole.status==1).all()
        for val in role:
            # val=val.as_dict()
            # val.pop('permission')
            data.append({'id': val.id, 'rolename': val.rolename})
        return data
