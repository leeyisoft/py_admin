#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import or_
from trest.utils import utime
from trest.logger import SysLogger
from trest.config import settings
from trest.exception import JsonError
from applications.common.models.advertising import Advertising
from applications.common.models.advertising_category import AdvertisingCategory

from applications.admin.filters.advertising  import AdvertisingFilter
from applications.admin.services.advertising_category import AdvertisingCategoryService


class AdvertisingService(object):
    @staticmethod
    def list_for_category(category, limit):
        """列表记录
        Arguments:
            where dict -- 查询条件
            page int -- 当前页
            per_page int -- 每页记录数

        return:
            Paginate 对象 | None
        """
        category_id = AdvertisingCategory.session.query(AdvertisingCategory.id) \
            .filter(AdvertisingCategory.name == category).scalar()
        now_time = utime.timestamp(3)
        rows = Advertising.Q \
            .filter(Advertising.category_id == category_id) \
            .filter(Advertising.start_at <= now_time) \
            .filter(or_(Advertising.end_at > now_time, Advertising.end_at == 0)) \
            .filter(Advertising.status == 1) \
            .order_by(Advertising.sort.desc()) \
            .limit(limit).all()
        return rows if rows else []
