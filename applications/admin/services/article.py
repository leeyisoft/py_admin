#!/usr/bin/env python
# -*- coding: utf-8 -*-
from trest.utils import utime
from trest.logger import SysLogger
from trest.config import settings
from trest.exception import JsonError
from applications.common.models.article import Article
from applications.common.models.article_category import ArticleCategory


class ArticleService:
    @staticmethod
    def data_list(where, page, per_page):
        """列表记录
        Arguments:
            where dict -- 查询条件
            page int -- 当前页
            per_page int -- 每页记录数

        return:
            Paginate 对象 | None
        """

        if 'category' in where.keys():
            where['category_id'] = ArticleCategory.session.query(ArticleCategory.id) \
            .filter(ArticleCategory.name == where['category']).scalar()
        query = Article.Q

        if 'category_id' in where.keys():
            query = query.filter(Article.category_id == where['category_id'])

        if 'id' in where.keys():
            query = query.filter(Article.id == where['id'])

        if 'title' in where.keys():
            query = query.filter(Article.title == where['title'])

        if 'status' in where.keys():
            query = query.filter(Article.status == where['status'])
        else:
            query = query.filter(Article.status != -1)

        pagelist_obj = query.paginate(page=page, per_page=per_page)

        if pagelist_obj is None:
            raise JsonError('暂无数据')
        return pagelist_obj

    @staticmethod
    def get(id):
        """获取单条记录

        [description]

        Arguments:
            id int -- 主键

        return:
            Article Model 实例 | None
        """
        if not id:
            raise JsonError('ID不能为空')
        obj = Article.Q.filter(Article.id == id).first()
        return obj

    @staticmethod
    def update(id, param):
        """更新记录

        [description]

        Arguments:
            id int -- 主键
            param dict -- [description]

        return:
            True | JsonError
        """
        columns = [i for (i, _) in Article.__table__.columns.items()]
        for key in param.keys():
            if key not in columns:
                param.pop(key, None)

        if 'updated_at' in columns:
            param['updated_at'] = utime.timestamp(3)
        if not id:
            raise JsonError('ID 不能为空')

        status = param.get('status', None)
        category_id = param.get('category_id', 0)
        if status != -1 and not(int(category_id) > 0):
            raise JsonError('文章分类缺失')
        try:
            Article.Update.filter(Article.id == id).update(param)
            Article.session.commit()
            return True
        except Exception as e:
            Article.session.rollback()
            SysLogger.error(e)
            raise JsonError('update error')

    @staticmethod
    def insert(param):
        """插入

        [description]

        Arguments:
            id int -- 主键
            param dict -- [description]

        return:
            True | JsonError
        """
        columns = [i for (i, _) in Article.__table__.columns.items()]
        for key in param.keys():
            if key not in columns:
                param.pop(key, None)
        if 'created_at' in columns:
            param['created_at'] = utime.timestamp(3)

        category_id = param.get('category_id', 0)
        if not(int(category_id) > 0):
            raise JsonError('文章分类缺失')
        try:
            data = Article(**param)
            Article.session.add(data)
            Article.session.commit()
            return True
        except Exception as e:
            Article.session.rollback()
            SysLogger.error(e)
            raise JsonError('insert error')
