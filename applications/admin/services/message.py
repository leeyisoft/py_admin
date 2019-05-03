#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
消息管理
"""
from pyrestful.rest import JsonError
from applications.common.models.base import Message


class MessageService:
    @staticmethod
    def add_data(param):
        code = 0
        msg = ''
        res_data = []
        try:
            data = Message(**param)
            Message.session.add(data)
            Message.session.commit()
        except Exception:
            Message.session.rollback()
            raise JsonError()
        return True


