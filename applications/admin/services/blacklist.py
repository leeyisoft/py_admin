#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
黑名单管理
"""
from applications.admin.models import BlackList


class BlackListService:

    @staticmethod
    def data_list(param, page, limit):
        """
        数据列表
        :param param:
        :param page:
        :param limit:
        :return:
        """
        code = 0
        msg = ''
        res_data = (0, [])

        query = BlackList.Q
        if param['value']:
            query = query.filter(BlackList.value == param['value'])
        if param['type']:
            query = query.filter(BlackList.type == param['type'])
        if param['admin_id']:
            query = query.filter(BlackList.admin_id == param['admin_id'])
        if param['order_number']:
            query = query.filter(BlackList.order_number == param['order_number'])

        pagelist_obj = query.paginate(page=page, per_page=limit)
        if pagelist_obj is None:
            code = 1
            msg = "暂无数据"
        else:
            items = []
            for val in pagelist_obj.items:
                items.append(val.as_dict())
            res_data = (pagelist_obj.total, items)
        return (code, msg, res_data)

    @staticmethod
    def detail_info(id):
        """
        详情
        :param d:
        :return:
        """
        code = 0
        msg = ''
        res_data = []
        if not id:
            return (1,'未找到记录', res_data)
        data = BlackList.Q.filter(BlackList.id == id).first()
        BlackList.session.commit()
        if not data:
            return (1, '未找到记录', res_data)
        data = data.as_dict()
        return (code, msg, data)

    @staticmethod
    def add_data(param):
        """
        新增数据
        :param param:
        :return:
        """
        code = 0
        msg = ''
        res_data = []
        if BlackListService.check_value(param['value'], None):
            code = 1
            msg = "该黑名单已存在"
            return (code, msg, res_data)
        try:
            data = BlackList(**param)
            BlackList.session.add(data)
            BlackList.session.commit()
        except Exception:
            BlackList.session.rollback()
            code = 1
            msg = '出错'
        return (code, msg, res_data)

    @staticmethod
    def put_data(param):
        """
        更新数据
        :param param:
        :return:
        """
        code = 0
        msg = ''
        res_data = []
        if not param['id']:
            code = 1
            msg = '参数缺失'
            return (code, msg, res_data)
        (code, msg, res_data) = BlackListService.is_exist(param['id'])
        if code > 0:
            return (code, msg, res_data)
        try:
            BlackList.Q.filter(BlackList.id == param['id']).update(param)
            BlackList.session.commit()
        except Exception:
            BlackList.session.rollback()
            code = 1
            msg = '出错'
        return (code, msg, res_data)

    @staticmethod
    def delete_data(id):
        """
        删除
        :param id:
        :return:
        """
        (code, msg, res_data) = BlackListService.is_exist(id)
        if code > 0:
            return (code, msg, res_data)
        BlackList.Q.filter(BlackList.id == id).delete()
        BlackList.session.commit()
        return (code, msg, res_data)

    @staticmethod
    def is_exist(id):
        """
        更具id查询数据是否存在
        :param id:
        :return:
        """
        code = 0
        msg = ""
        res_data = []
        BlackList_id = BlackList.session.query(BlackList.id) \
            .filter(BlackList.id == id).scalar()
        if not BlackList_id:
            code = 1
            msg = '该公司不存在'
        return (code, msg, res_data)

    @staticmethod
    def check_value(value, id):
        """
        检查是否已存在
        """
        if id:
            count = BlackList.Q.filter(BlackList.id != id).filter(BlackList.value == value).count()
        else:
            count = BlackList.Q.filter(BlackList.value == value).count()
        if count > 0:
            return True
        return False

    @staticmethod
    def status_options():
        """
        状态列表
        :return:
        """
        return BlackList.status_options

    @staticmethod
    def type_options():
        """
        类型列表
        :return:
        """
        return BlackList.type_options


