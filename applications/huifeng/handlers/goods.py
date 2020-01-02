#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""
from trest.router import get

from .common import CommonHandler

from ..services.goods import GoodsService

class GoodsHandler(CommonHandler):
    @get('/goods')
    def goods_list_get(self, *args, **kwargs):
        """列表、搜索记录
        """
        page = int(self.get_argument('page', 1))
        per_page = int(self.get_argument('limit', 6))

        param = {}
        param['status'] = 1

        resp_data = GoodsService.page_list(param, page, per_page)
        return self.success(data=resp_data)
