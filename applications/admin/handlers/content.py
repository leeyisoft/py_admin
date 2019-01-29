#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""后台会员管理

[description]
"""
import re
import os
import json
import tornado

from applications.core.settings_manager import settings
from applications.core.logger.client import SysLogger
from applications.core.cache import sys_config
from applications.core.decorators import required_permissions
from applications.core.utils.encrypter import RSAEncrypter
from applications.core.utils.hasher import make_password
from applications.core.utils import Func
from applications.core.utils import FileUtil
from applications.core.utils import Uploader

from ..models import Article
from ..models import Team
from ..models import Role
from ..models import AdminMenu

from .common import CommonHandler


class ArticleHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    @required_permissions('admin:article:index')
    def get(self, *args, **kwargs):
        """后台首页
        """
        # return self.show('<script type="text/javascript">alert(1)</script>')
        category = self.get_argument('category', '')
        params = {
            'category': category,
            'category_option_html': Article.category_option_html(),
        }
        self.render('article/index.html', **params)

    @tornado.web.authenticated
    @required_permissions('admin:article:delete')
    def delete(self, *args, **kwargs):
        """删除文章
        """
        # return self.show('<script type="text/javascript">alert(1)</script>')
        id = self.get_argument('id', None)

        article = Article.Q.filter(Article.id==id).first()
        if article.thumb:
            try:
                os.remove(settings.STATIC_PATH+'/'+article.thumb)
            except Exception as e:
                pass
        if article.content:
            pic_url = re.findall('img src="(.*?)"',article.content,re.S)
            pic_url = [settings.STATIC_PATH+pic[7:] for pic in pic_url if pic.startswith('/static')]
            for imgfile in pic_url:
                try:
                    os.remove(imgfile.split('?')[0])
                except Exception as e:
                    pass

        Article.Q.filter(Article.id==id).delete()
        Article.session.commit()
        return self.success()

class ArticleListHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    @required_permissions('admin:article:index')
    def get(self, *args, **kwargs):
        limit = self.get_argument('limit', 10)
        page = self.get_argument('page', 1)
        title = self.get_argument('title', None)
        category = self.get_argument('category', None)

        query = Article.Q
        # query = Article.Q.filter(Article.status==1)
        if title:
            query = query.filter(Article.title.like('%'+title+'%'))
        if category:
            query = query.filter(Article.category==category)

        pagelist_obj = query.paginate(page=page, per_page=limit)

        if pagelist_obj is None:
            return self.error('暂无数据')

        total = pagelist_obj.total
        page = pagelist_obj.page
        items = pagelist_obj.items
        data = []
        for item in items:
            item2 = item.as_dict()
            item2['category_option'] = item.category_option
            data.append(item2)
        # print('data ', data)
        params = {
            'count': total,
            'uri': self.request.uri,
            'path': self.request.path,
            'data': data,
        }
        return self.success(**params)

class ArticleAddHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    @required_permissions('admin:article:add')
    def get(self, *args, **kwargs):
        category = self.get_argument('category', '')
        menu_list = AdminMenu.children(status=1)
        article = Article(status=1, deleted=0)

        data_info = article.as_dict()

        params = {
            'category': category,
            'article': article,
            'menu_list': menu_list,
            'data_info': data_info,
            'category_option_html': Article.category_option_html(),
        }
        self.render('article/save.html', **params)

    @tornado.web.authenticated
    @required_permissions('admin:article:add')
    def post(self, *args, **kwargs):
        params = self.params()

        params['status'] = params.get('status', 0)
        params['hits'] = params.get('hits', 0)
        params['user_id'] = 1
        params['ip'] = self.request.remote_ip
        if not params.get('title', None):
            return self.error('文章标题不能为空')
        if not params.get('content', None):
            return self.error('内容不能为空')

        count = Article.Q.filter(Article.title==params['title']).count()
        if count>0:
            return self.error('文章标题已被占用')


        params.pop('_xsrf', None)
        params.pop('rsa_encrypt', None)
        article = Article(**params)
        Article.session.add(article)
        Article.session.commit()
        # print('article ', type(article), article.id)
        return self.success()
        # return self.success(data=article.as_dict())

class ArticleEditHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    @required_permissions('admin:article:edit')
    def get(self, *args, **kwargs):
        id = self.get_argument('id', None)
        category = self.get_argument('category', '')
        menu_list = AdminMenu.children(status=1)
        article = Article.Q.filter(Article.id==id).first()

        data_info = article.as_dict()
        data_info.pop('password', None)
        params = {
            'category': category,
            'article': article,
            'menu_list': menu_list,
            'data_info': data_info,
            'category_option_html': Article.category_option_html(article.category),
        }
        self.render('article/save.html', **params)

    @tornado.web.authenticated
    @required_permissions('admin:article:edit')
    def post(self, *args, **kwargs):
        id = self.get_argument('id', None)

        params = self.params()

        params['status'] = params.get('status', 0)

        if not id:
            return self.error('用户ID不能为空')

        title = params.get('title', None)
        if title:
            count = Article.Q.filter(Article.id!=id).filter(Article.title==title).count()
            if count>0:
                return self.error('文章标题已被占用')

        params.pop('_xsrf', None)
        params.pop('file', None)
        Article.Q.filter(Article.id==id).update(params)
        Article.session.commit()

        # update article cache info
        article = Article.Q.filter(Article.id==id).first()

        return self.success(data=params)

class ArticleInfoHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    @required_permissions('admin:article:info')
    def get(self, *args, **kwargs):
        id = self.current_user.get('id', None)
        user = Article.Q.filter(Article.id==id).first()
        data_info = user.as_dict()
        params = {
            'user': user,
            'data_info': data_info,
            'public_key': sys_config('sys_login_rsa_pub_key'),
            'rsa_encrypt': sys_config('login_pwd_rsa_encrypt'),
        }
        self.render('article/info.html', **params)

    @tornado.web.authenticated
    @required_permissions('admin:article:info')
    def post(self, *args, **kwargs):
        title = self.get_argument('title', None)
        password = self.get_argument('password', None)
        rsa_encrypt = self.get_argument('rsa_encrypt', 0)
        email = self.get_argument('email', None)
        mobile = self.get_argument('mobile', None)

        id = self.current_user.get('id', None)
        user = {}

        if title:
            user['title'] = title
            count = Article.Q.filter(Article.id!=id).filter(Article.title==title).count()
            if count>0:
                return self.error('文章标题已被占用')
        if password:
            if settings.login_pwd_rsa_encrypt and int(rsa_encrypt)==1 and len(password)>10:
                private_key = sys_config('sys_login_rsa_priv_key')
                password = RSAEncrypter.decrypt(password, private_key)
            user['password'] = make_password(password)

        if mobile:
            user['mobile'] = mobile
            count = Article.Q.filter(Article.id!=id).filter(Article.mobile==mobile).count()
            if count>0:
                return self.error('电话号码已被占用')
        if email:
            user['email'] = email
            count = Article.Q.filter(Article.id!=id).filter(Article.email==email).count()
            if count>0:
                return self.error('Email已被占用')


        Article.Q.filter(Article.id==id).update(user)
        Article.session.commit()

        return self.success(data=user)


class CompanyTeamHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    @required_permissions('admin:company:team')
    def get(self, *args, **kwargs):
        category = self.get_argument('category', '')
        params = {
            'category': category,
            'category_option_html': Article.category_option_html(),
        }
        self.render('company/team/index.html', **params)

class TeamListHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    @required_permissions('admin:company:team')
    def get(self, *args, **kwargs):
        limit = self.get_argument('limit', 10)
        page = self.get_argument('page', 1)
        name = self.get_argument('name', None)
        title = self.get_argument('title', None)

        query = Team.Q
        # query = Team.Q.filter(Team.status==1)
        if name:
            query = query.filter(Team.name.like('%'+name+'%'))
        if title:
            query = query.filter(Team.title.like('%'+title+'%'))

        query = query.order_by(Team.order.asc())
        pagelist_obj = query.paginate(page=page, per_page=limit)

        if pagelist_obj is None:
            return self.error('暂无数据')

        total = pagelist_obj.total
        page = pagelist_obj.page
        items = pagelist_obj.items
        data = []
        for item in items:
            item2 = item.as_dict()
            data.append(item2)
        # print('data ', data)
        params = {
            'count': total,
            'uri': self.request.uri,
            'path': self.request.path,
            'data': data,
        }
        return self.success(**params)

    @tornado.web.authenticated
    @required_permissions('admin:article:delete')
    def delete(self, *args, **kwargs):
        """删除
        """
        id = self.get_argument('id', None)

        team = Team.Q.filter(Team.id==id).first()
        if team.avatar:
            try:
                os.remove(settings.STATIC_PATH+'/'+team.avatar)
            except Exception as e:
                pass
        Team.Q.filter(Team.id==id).delete()
        Team.session.commit()
        return self.success()

class TeamAddHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    @required_permissions('admin:team:add')
    def get(self, *args, **kwargs):
        team = Team(status=1, avatar='')

        data_info = team.as_dict()

        print('team ', type(team), team)
        params = {
            'team': team,
            'data_info': data_info,
        }
        self.render('company/team/save.html', **params)

    @tornado.web.authenticated
    @required_permissions('admin:team:add')
    def post(self, *args, **kwargs):
        params = self.params()

        params['status'] = params.get('status', 0)

        name = params.get('name', None)

        count = Team.Q.filter(Team.name==name).count()
        if count>0:
            return self.error('名称已被占用')

        params.pop('_xsrf', None)
        params.pop('file', None)
        team = Team(**params)
        Team.session.add(team)
        Team.session.commit()
        # print('team ', type(team), team.id)
        return self.success()

class TeamEditHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    @required_permissions('admin:team:edit')
    def get(self, *args, **kwargs):
        id = self.get_argument('id', None)
        team = Team.Q.filter(Team.id==id).first()

        data_info = team.as_dict()
        params = {
            'team': team,
            'data_info': data_info,
        }
        self.render('company/team/save.html', **params)

    @tornado.web.authenticated
    @required_permissions('admin:team:edit')
    def post(self, *args, **kwargs):
        id = self.get_argument('id', None)

        params = self.params()

        params['status'] = params.get('status', 0)

        if not id:
            return self.error('用户ID不能为空')

        name = params.get('name', None)
        if name:
            count = Team.Q.filter(Team.id!=id).filter(Team.name==name).count()
            if count>0:
                return self.error('名称已被占用')

        params.pop('_xsrf', None)
        params.pop('file', None)
        Team.Q.filter(Team.id==id).update(params)
        Team.session.commit()

        # update team cache info
        team = Team.Q.filter(Team.id==id).first()

        return self.success(data=params)

class UploadHandler(CommonHandler):
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        """上传图片"""
        user_id = self.current_user.get('id')

        next = self.get_argument('next', '')
        imgfile = self.request.files.get('file')
        action = self.get_argument('action', None)
        path = self.get_argument('path', 'default_path')

        if action not in ['article', 'arc_thumb', 'avatar']:
            return self.error('不支持的action')

        for img in imgfile:
            print('img', type(img))
            # 对文件进行重命名
            file_ext = FileUtil.file_ext(img['filename'])
            path = '%s/' % path
            save_name = img['filename']
            file_md5 = Func.md5(img['body'])
            if action=='avatar':
                save_name = '%s.%s' %(file_md5, file_ext)
            try:
                param = Uploader.upload_img(file_md5, img, save_name, path, {
                    'user_id': user_id,
                    'ip': self.request.remote_ip,
                })
                param['src'] = self.static_url(param.get('path_file'))
                param['title'] = param.get('origin_name')
                return self.success(data=param)
            except Exception as e:
                if settings.debug:
                    raise e
                SysLogger.error(e)
                return self.error('上传失败')

        return self.error('参数错误')
