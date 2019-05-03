#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
公司管理
"""
from pyrestful.rest import JsonError
from applications.admin.models import Company
from applications.core.utils import func


class CompanyService:
    @staticmethod
    def data_list(param, page, limit):
        """
        数据列表
        :param param:
        :param page:
        :param limit:
        :return:
        """
        query = Company.Q
        if param['module']:
            query = query.filter(Company.module == param['module'])

        if param['status']:
            query = query.filter(Company.status == param['status'])

        if param['type']:
            query = query.filter(Company.type == param['type'])

        pagelist_obj = query.paginate(page=page, per_page=limit)
        if pagelist_obj is None:
            raise JsonError('暂无数据')
        return pagelist_obj

    @staticmethod
    def detail_info(company_id):
        """
        详情
        :param company_id:
        :return:
        """
        data = Company.Q.filter(Company.id == company_id).first()
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
        if CompanyService.check_name(param['company_name'], None):
            raise JsonError('名称已被占用')
        try:
            data = Company(**param)
            Company.session.add(data)
        except Exception as e:
            Company.session.rollback()
            raise e
        else:
            Company.session.commit()
        return True

    @staticmethod
    def put_data(param):
        """
        更新数据
        :param param:
        :return:
        """
        if 'company_id' not in param.keys():
            raise JsonError('参数缺失')
        is_exist = CompanyService.is_exist(param['company_id'])
        if is_exist is False:
            raise JsonError('不存在的企业ID')

        if CompanyService.check_name(param['company_name'], param['company_id']):
            raise JsonError('名称已被占用')
        try:
            Company.Q.filter(Company.id == param['company_id']).update(param)
            Company.session.commit()
        except Exception as e:
            Company.session.rollback()
            raise e
        return True

    @staticmethod
    def delete_data(company_id):
        """
        删除公司
        :param company_id:
        :return:
        """
        if int(company_id) == 1:
            raise JsonError('默认公司不可删除')

        is_exist = CompanyService.is_exist(company_id)
        if is_exist is False:
            raise JsonError('不存在的企业ID')
        Company.Q.filter(Company.id == company_id).delete()
        Company.session.commit()
        return True

    @staticmethod
    def is_exist(company_id):
        """
        更具id查询数据是否存在
        :param company_id:
        :return:
        """
        check = Company.session.query(Company.id)\
            .filter(Company.id == company_id).scalar()
        return True if check>0 else False

    @staticmethod
    def check_name(company_name, company_id):
        """
        检查名称是否已被占用
        """
        if company_id:
            count = Company.Q.filter(Company.id != company_id)\
                .filter(Company.company_name == company_name).count()
        else:
            count = Company.Q.filter(Company.company_name == company_name).count()
        return True if count>0 else False

    @staticmethod
    def company_options():
        """
        公司选项列表
        :return:
        """
        data = Company.session.query(Company.id, Company.company_name).filter(Company.status == 1).all()
        item_dict = {}
        item_list = []
        if not data:
            return (item_dict, item_list)
        else:
            for raw in data:
                temp = {}
                (temp['value'], temp['label']) = raw
                item_list.append(temp)
                item_dict[temp['value']] = temp['label']
        return (item_dict, item_list)

    @staticmethod
    def status_options():
        """
        状态列表
        :return:
        """
        options = Company.status_options
        return (options, func.option_change(options))

    @staticmethod
    def type_options():
        """
        类型列表
        :return:
        """
        options = Company.type_options
        return (options, func.option_change(options))


    @staticmethod
    def module_options():
        """
        业务选项列表
        :return:
        """
        options = Company.module_options
        return (options, func.option_change(options))


