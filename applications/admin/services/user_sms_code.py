#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
短信验证码
"""
from applications.common.models.user import UserSmsCode
class UserSmsCodeService:

    @staticmethod
    def data_list(param,page,limit):
        code=0
        msg=''
        res_data=[]

        query=UserSmsCode.Q
        if param['mobile']:
            query=query.filter(UserSmsCode.mobile==param['mobile'])
        pagelist_obj = query.paginate(page=page, per_page=limit)
        if pagelist_obj is None:
            code = 1
            msg = "暂无数据"
        else:
            resdata = (pagelist_obj.total, pagelist_obj.items)
        return (code, msg, resdata)
