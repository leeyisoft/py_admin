#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""AdminUser 响应过滤器
"""


class AdminUserFilter(object):
    @staticmethod
    def page_list(pagelist_obj, page, per_page):
        items = []
        for item in pagelist_obj.items:
            data = item.as_dict()
            if not data['permission'] or data['permission']=='':
                data['permission']=[]
            else:
                data['permission']=data['permission'].replace('\\','').replace('[','').replace(']','').replace('"','').split(',')
            items.append(data)
        return {
            'page':page,
            'per_page':per_page,
            'total':pagelist_obj.total,
            'items':items,
        }

