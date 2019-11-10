#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ArticleCategory控制器
"""
from trest.router import get
from trest.router import put
from trest.router import post
from trest.router import delete
from trest.exception import JsonError

from applications.admin.utils import required_permissions
from applications.admin.utils import admin_required_login

from applications.admin.services.article_category import ArticleCategoryService

from .common import CommonHandler


class ArticleCategoryHandler(CommonHandler):

    @post('article_category')
    @admin_required_login
    @required_permissions()
    def article_category_post(self, *args, **kwargs):
        param = self.params()
        ArticleCategoryService.insert(param)
        return self.success()

    @get('article_category/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def article_category_get(self, id):
        """获取单个记录
        """
        obj = ArticleCategoryService.get(id)
        data = obj.as_dict() if obj else {}
        return self.success(data = data)

    @put('article_category/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def article_category_put(self, id, *args, **kwargs):
        param = self.params()
        ArticleCategoryService.update(id, param)
        return self.success(data = param)

    @delete('article_category/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def article_category_delete(self, id, *args, **kwargs):
        param = {
            'status':-1
        }
        ArticleCategoryService.update(id, param)
        return self.success()

    @get('article_category/valid')
    @admin_required_login
    # @required_permissions()
    def article_category_valid_get(self):
        """
        有效的分类列表
        :return:
        """
        data = ArticleCategoryService.data_list_valid()
        return self.success(data=data)
