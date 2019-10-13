#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""后台会员管理

[description]
"""

from trest.router import get
from trest.router import put
from trest.router import post
from trest.router import delete
from trest.exception import JsonError
from trest.config import settings

from applications.admin.utils import required_permissions
from applications.admin.utils import admin_required_login
from applications.common.models.content import Article
from applications.admin.services.content import ArticleService

from .common import CommonHandler


# from ..models import Team
# from ..models import Role
# from ..models import AdminMenu

from .common import CommonHandler


class ArticleHandler(CommonHandler):
    """docstring for Article"""
    @get('article/(?P<article_id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def article_detail_get(self, article_id):
        obj = ArticleService.detail(article_id)
        data = obj.as_dict() if obj else {}
        return self.success(data = data)

    @get(['article','article/?(?P<category>[a-zA-Z0-9_]*)'])
    @admin_required_login
    @required_permissions()
    def article_list_get(self, category = '', *args, **kwargs):
        page = int(self.get_argument('page',1))
        limit = int(self.get_argument('limit',10))
        title = self.get_argument('title',None)
        status = self.get_argument('status',None)

        print('category ', category)
        param = {}
        if category:
            param['category'] = category
        if title:
            param['title'] = title
        if status:
            param['status'] = status

        pagelist_obj = ArticleService.data_list(param,page,limit)
        items = []
        for val in pagelist_obj.items:
            data = val.as_dict()
            # category_info = ArticleCategory.Q.filter(ArticleCategory.id==data['category_id']).first()
            # if category_info is not None:
            #     data['category'] = category_info.as_dict()['name']
            # else:
            #     data['category'] = ''
            items.append(data)
        resp = {
            'page':page,
            'per_page':limit,
            'total':pagelist_obj.total,
            'items':items,
        }
        return self.success(data = resp)


    @put('article')
    @admin_required_login
    @required_permissions()
    def article_detail_put(self, *args, **kwargs):
        article_id = int(self.get_argument('id', 0))

        param = self.params()
        ArticleService.put_data(param, article_id)
        return self.success(data = param)

    @delete('article')
    @admin_required_login
    @required_permissions()
    def article_detail_delete(self, *args, **kwargs):
        article_id = int(self.get_argument('article_id', 0))
        param = {
            'status':-1
        }
        ArticleService.put_data(param, article_id)
        return self.success()
