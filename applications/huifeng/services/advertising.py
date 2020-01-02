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
        """
        Arguments:
            category string -- category 唯一标识
            limit int -- 查询记录数

        return:
            list
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

    @staticmethod
    def get_for_category(category):
        """
        Arguments:
            category string -- category 唯一标识
            limit int -- 查询记录数

        return:
            list
        """
        category_id = AdvertisingCategory.session.query(AdvertisingCategory.id) \
            .filter(AdvertisingCategory.name == category).scalar()
        now_time = utime.timestamp(3)
        row = Advertising.Q \
            .filter(Advertising.category_id == category_id) \
            .filter(Advertising.start_at <= now_time) \
            .filter(or_(Advertising.end_at > now_time, Advertising.end_at == 0)) \
            .filter(Advertising.status == 1) \
            .order_by(Advertising.sort.desc()) \
            .first()
        return row
