#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""
import tornado
from applications.core.db.dbalchemy import Connector
from applications.core.settings_manager import settings
from applications.core.logger.client import SysLogger
from applications.core.cache import sys_config
from applications.core.utils import Func

from .common import CommonHandler

from ..utils import tpl_params
from ..models.content import Contact
from ..models.content import Article

class AboutHandler(CommonHandler):
    def get(self, *args, **kwargs):
        """
        关于我们
        """
        field = ['title', 'subtitle', 'value']
        about_us_a = sys_config('about_us_a', field)
        about_us_b = sys_config('about_us_b', field)
        # teams = get_teams({'limit':8})
        query = "SELECT `id`, `title`, `description`, `name`, `avatar` FROM `home_team` WHERE `status`=1 ORDER BY `order` ASC LIMIT 8"
        session = Connector.get_session()
        # print('session', type(session),session)
        teams = session.get('master').execute(query).fetchall()
        # print('teams', type(teams),teams)
        about_us_b['value'] = about_us_b['value'].replace("\n\n", "\n").replace("\n", "<br/>")
        params = {
            'about_us_a': about_us_a,
            'about_us_b': about_us_b,
            'teams': teams,
            'new_right':{},
            'flatpage': {'title':'关于我们',},
        }
        # 合并字典
        params.update(tpl_params())

        self.render_html('singlepage/about.htm', **params)

class ActivityHandler(CommonHandler):
    def get(self, *args, **kwargs):
        """
        新闻活动
        """
        breadcrumb = [
            {'title': '新闻活动', 'url': '/company/activity/'},
            {'title': 'List', 'url': '#'},
        ]
        params = self.params()

        params['category'] = 'activity'
        pagelist_obj = Article.lists(params)

        cur_page = params.get('page', 1)
        params = {
            'breadcrumb': breadcrumb,
            'cur_page': int(cur_page),
            'pagelist_obj': pagelist_obj,
            'dateformat': Func.dateformat,
            'flatpage': {'title':'新闻活动',},
        }

        # 合并字典
        params.update(tpl_params())
        self.render_html('article/list1.htm', **params)

class RegulationsHandler(CommonHandler):
    def get(self, *args, **kwargs):
        """
        政策法规
        """
        breadcrumb = [
            {'title': '政策法规', 'url': '/regulation/'},
            {'title': 'List', 'url': '#'},
        ]
        params = self.params()

        params['category'] = 'regulation'
        pagelist_obj = Article.lists(params)

        cur_page = params.get('page', 1)
        params = {
            'breadcrumb': breadcrumb,
            'cur_page': int(cur_page),
            'pagelist_obj': pagelist_obj,
            'dateformat': Func.dateformat,
            'flatpage': {'title':'政策法规',},
        }
        # 合并字典
        params.update(tpl_params())
        self.render_html('article/list1.htm', **params)

class ProductHandler(CommonHandler):
    def get(self, *args, **kwargs):
        """
        产品展示
        """
        breadcrumb = [
            {'title': '产品展示', 'url': '/company/product/'},
            {'title': 'List', 'url': '#'},
        ]
        params = self.params()
        params['per_page'] = 3
        params['category'] = 'product'
        pagelist_obj = Article.lists(params)

        cur_page = params.get('page', 1)
        params = {
            'breadcrumb': breadcrumb,
            'cur_page': int(cur_page),
            'pagelist_obj': pagelist_obj,
            'dateformat': Func.dateformat,
            'flatpage': {'title':'产品展示',},
        }
        # 合并字典
        params.update(tpl_params())
        self.render_html('article/list2.htm', **params)

class ContactHandler(CommonHandler):
    def get(self, *args, **kwargs):
        """
        联系我们
        """
        contact = sys_config('contact', ['title', 'subtitle', 'value'])

        params = {
            'contact': contact,
            'flatpage': {'title':'联系我们',},
            'csrf_input': self.xsrf_form_html(),
        }        # 合并字典
        params.update(tpl_params())
        self.render_html('singlepage/contact.htm', **params)


    def post(self, *args, **kwargs):
        # return self.success(data={'id':22, 'groupname':'leeyitest'})
        try:
            real_name = self.get_argument('real_name', '')
            phone = self.get_argument('phone', '')
            message = self.get_argument('message', '')

            if not real_name:
                return self.error('请输入用户名')
            if not phone:
                return self.error('请输入联系电话')
            if not message:
                return self.error('请输入留言内容')


            if not Func.is_phone_or_mobile(phone):
                return self.error('联系电话格式不正确')

            if not (1<len(message) and len(message)<321):
                return self.error('留言信息 至少2个字符,最多320个字符！')
            client_ip = self.request.remote_ip
            now = Func.utc_now()
            today = '%d-%d-%d' % (now.year, now.month, now.day)
            check = Contact.Q.filter(Contact.phone, Contact.utc_created_at>=today).count()
            # print('check0', check)
            if check>5:
                query = ''
                return self.error('每天只能够提交5次留言')

            check = Contact.Q.filter(Contact.phone==phone, Contact.message==message).count()
            # print('check', check)
            if check>0:
                return self.error('已经有相同的留言了，请不要重复！')

            params = {
                'real_name': real_name,
                'phone': phone,
                'message': message,
                'ip': client_ip,
                # 'real_name':real_name,
                # 'real_name':real_name,
            }
            obj = Contact(**params)
            Contact.session.add(obj)
            Contact.session.commit()
        except Exception as e:
            SysLogger.error('post contact error: %s' % e)
            # print(e)
            return self.error(msg='操作失败')
        return self.success(data=obj.as_dict(), msg='感谢你的留言')


class ArticleDetailHandler(CommonHandler):
    def get(self, aid, *args):
        """
        文章内容页
        """
        aid = int(aid)
        if not (aid>0):
            self.redirect('/')

        arc = Article.detail(aid)
        # print('arc', type(arc), arc)

        flatpage_title = '文章内容页'
        templte = 'article/detail.htm'
        breadcrumb = []
        if arc.get('category', '')=='activity':
            breadcrumb += [{'title': '新闻活动', 'url': '/company/activity/'},]
        elif arc.get('category', '')=='regulation':
            breadcrumb += [{'title': '政策法规', 'url': '/regulation/'},]
        elif arc.get('category', '')=='product':
            breadcrumb += [{'title': '产品展示', 'url': '/company/product/'},]
            templte = 'article/detail2.htm'
            flatpage_title = '产品内容页'

        breadcrumb += [{'title': 'Detail', 'url': '#'},]

        params = {
            'arc': arc,
            'breadcrumb': breadcrumb,
            'flatpage': {'title':flatpage_title,},
        }
        # 合并字典
        params.update(tpl_params())

        self.render_html(templte, **params)
