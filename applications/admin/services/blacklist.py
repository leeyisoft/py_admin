#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
黑名单管理
"""
from trest.exception import JsonError
from applications.common.models import BlackList


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
        query = BlackList.Q

        if 'value' in param.keys():
            query = query.filter(BlackList.value == param['value'])
        if 'bltype' in param.keys():
            query = query.filter(BlackList.type == param['bltype'])
        if 'admin_id' in param.keys():
            query = query.filter(BlackList.admin_id == param['admin_id'])
        if 'loan_order_id' in param.keys():
            query = query.filter(BlackList.loan_order_id == param['loan_order_id'])

        pagelist_obj = query.paginate(page=page, per_page=limit)
        # print('query.statement: ', query.statement)
        if pagelist_obj is None:
            raise JsonError('暂无数据')
        return pagelist_obj

    @staticmethod
    def detail_info(id):
        """
        详情
        :param d:
        :return:
        """
        if not id:
            raise JsonError('参数缺失')
        data = BlackList.Q.filter(BlackList.id == id).first()
        BlackList.session.commit()
        if not data:
            raise JsonError('未找到记录')
        return data

    @staticmethod
    def add_data(param):
        """
        新增数据
        :param param:
        :return:
        """
        if BlackListService.check_value(param['value'], None):
            raise JsonError('该黑名单已存在')
        try:
            data = BlackList(**param)
            BlackList.session.add(data)
            BlackList.session.commit()
        except Exception as e:
            BlackList.session.rollback()
            raise e
        return data

    @staticmethod
    def put_data(param):
        """
        更新数据
        :param param:
        :return:
        """
        if not param['id']:
            raise JsonError('参数缺失')
        is_exist = BlackListService.is_exist(param['id'])
        if is_exist is False:
            raise JsonError('记录不存在')
        try:
            BlackList.Q.filter(BlackList.id == param['id']).update(param)
            BlackList.session.commit()
        except Exception as e:
            BlackList.session.rollback()
            raise e
        return True

    @staticmethod
    def delete_data(id):
        """
        删除
        :param id:
        :return:
        """
        is_exist = BlackListService.is_exist(id)
        if is_exist is False:
            raise JsonError('记录不存在')
        BlackList.Q.filter(BlackList.id == id).delete()
        BlackList.session.commit()
        return True

    @staticmethod
    def is_exist(id):
        """
        更具id查询数据是否存在
        :param id:
        :return:
        """
        is_exist = BlackList.session.query(BlackList.id) \
            .filter(BlackList.id == id).scalar()
        return True if is_exist else False

    @staticmethod
    def check_value(value, id):
        """
        检查是否已存在
        """
        if id:
            count = BlackList.Q.filter(BlackList.id != id).filter(BlackList.value == value).count()
        else:
            count = BlackList.Q.filter(BlackList.value == value).count()
        return True if count>0 else False

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
