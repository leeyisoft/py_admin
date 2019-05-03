#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
消息模板管理
"""
from applications.admin.models import MessageTemplate


class MessageTemplateService:

    @staticmethod
    def data_list(param, page, limit):
        """
        模板列表
        :param param:
        :param page:
        :param limit:
        :return:
        """
        code = 0
        msg = ''
        res_data = (0, [])

        query = MessageTemplate.Q
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
    def get_info(category='default'):
        """
        根据模板类型查找模板内容
        :param category:
        :return:
        """
        code = 0
        msg = ''
        res_data = MessageTemplate.session.query(MessageTemplate.content)\
            .filter(MessageTemplate.category == category, MessageTemplate.status == 1).scalar()
        if not res_data:
            return (1, '未找到记录', res_data)
        return (code, msg, res_data)

    @staticmethod
    def add_data(param):
        code = 0
        msg = ''
        res_data = []
        try:
            data = MessageTemplate(**param)
            MessageTemplate.session.add(data)
            MessageTemplate.session.commit()
        except Exception:
            MessageTemplate.session.rollback()
            code = 1
            msg = '出错'
        return (code, msg, res_data)


