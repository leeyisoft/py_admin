#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
文章管理
"""
from applications.common.models.content import Article
from applications.common.models.content import ArticleCategory


class ArticleCategoryService:
    @staticmethod
    def add_data(param):
        pass

class ArticleService:
    @staticmethod
    def detail(article_id):
        code = 0
        msg = ""
        resdata = []
        if not article_id:
            raise JsonError('角色ID不能为空')
        obj = Article.Q.filter(Article.id == article_id).first()
        return obj

    @staticmethod
    def add_data(param):
        code=0
        msg=''
        try:
            data = Article(**param)
            Article.session.add(data)
            Article.session.commit()
            return (code,msg)
        except Exception:
            Article.session.rollback()
            code=1
            msg='出错'
            return (code,msg)

    @staticmethod
    def data_list(param,page,limit):

        if 'category' in param.keys():
            param['category_id'] = ArticleCategory.session.query(ArticleCategory.id) \
            .filter(ArticleCategory.name == param['category']).scalar()

        query = Article.Q
        if 'category_id' in param.keys():
            query = query.filter(Article.category_id == param['category_id'])
        if 'title' in param.keys():
            query = query.filter(Article.title == param['title'])

        if 'status' in param.keys():
            query = query.filter(Article.status == param['status'])

        if 'lang' in param.keys():
            query = query.filter(Article.lang == param['lang'])

        query = query.filter(Article.status != -1)
        pagelist_obj = query.paginate(page=page, per_page=limit)

        if pagelist_obj is None:
            raise JsonError('暂无数据')
        return pagelist_obj

    @staticmethod
    def put_data(param, article_id):
        param.pop('_xsrf', None)
        param.pop('file', None)
        param.pop('id', None)

        if not article_id:
            raise JsonError('Article ID 不能为空')

        title = param.get('title', None)
        if title:
            count = Article.Q.filter(Article.id!=article_id).filter(Article.title==title).count()
            if count>0:
                raise JsonError('文章标题已被占用')
        try:
            Article.Q.filter(Article.id == article_id).update(param)
            Article.session.commit()
            return True
        except Exception:
            Article.session.rollback()
            raise JsonError('update error')
