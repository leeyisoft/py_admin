#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advertising 响应过滤器
"""


class GoodsFilter(object):
    @staticmethod
    def page_list(pagelist_obj, page, per_page):
        items = []
        for item in pagelist_obj.items:
            data = {}
            data['id'] = item.id
            data['title'] = item.title
            data['external_url'] = item.external_url
            data['inventory_quantity'] = item.inventory_quantity
            data['sales_quantity'] = item.sales_quantity

            data['hits'] = item.hits
            data['thumb'] = item.thumb.get('left', '')
            if  not data['thumb']:
                data['thumb'] = item.thumb.get('right', '')
            data['market_price'] = "{:.2f} 元".format(int(item.market_price)/100)
            data['price'] = "{:.2f} 元".format(int(item.price)/100)
            data['created_at'] = item.created_at

            items.append(data)
        return {
            'page':page,
            'per_page':per_page,
            'total':pagelist_obj.total,
            'items':items,
        }
