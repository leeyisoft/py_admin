#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advertising 响应过滤器
"""


class AdvertisingAssembler(object):
    @staticmethod
    def page_list(pagelist_obj, page, per_page, category_map):
        items = []
        for item in pagelist_obj.items:
            data = item.as_dict()
            data['category'] = ''
            if data['category_id'] in category_map.keys():
                data['category_name'] = category_map[data['category_id']].name
                data['category_title'] = category_map[data['category_id']].title

            items.append(data)
        return {
            'page':page,
            'per_page':per_page,
            'total':pagelist_obj.total,
            'items':items,
        }
