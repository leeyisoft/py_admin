#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from ast import literal_eval

from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.types import Text
from sqlalchemy import Column, Enum
from sqlalchemy import ForeignKey

from applications.core.settings_manager import settings
from applications.common.models.base import BaseModel
from applications.core.utils import utime
from applications.core.db import mysqldb


class Role(BaseModel):
    """
    系统管理员角色表
    """
    __tablename__ = 'sys_admin_role'

    id          = Column(Integer, primary_key=True, nullable=False, default=None)
    rolename    = Column(String(40), nullable=False)
    description = Column(String(100), nullable=False, default='')
    permission  = Column(Text, default='')
    sort        = Column(Integer, nullable=False, default=20)
    status      = Column(Integer, nullable=False, default=1)  # 状态:( 0 禁用；1 启用, 默认1)
    category    = Column(Integer, nullable=False, default=0)
    company_id     = Column(Integer, nullable=False, default=1)
    created_at  = Column(Integer, default=utime.timestamp)

    @classmethod
    def option_html(cls, role_id=None):
        query   = cls.session.query(Role)
        query   = query.filter(Role.status == 1)
        rows    = query.order_by(Role.sort.asc()).all()
        option_str = ''
        for row in rows:
            selected = 'selected' if role_id==row.id else ''
            option_str += '<option value="%s" %s>%s</option>' % (row.id, selected, row.rolename)
        return option_str

    status_options = {
        '1': '激活',
        '0': '待激活'
    }


class AdminUser(BaseModel):
    """
    系统管理员表
    """
    __tablename__ = 'sys_admin_user'

    id = Column(Integer, primary_key=True, nullable=False, default=None)
    role_id       = Column(Integer, ForeignKey('sys_admin_role.id'))
    password      = Column(String(128), nullable=False, default='')
    username      = Column(String(40), nullable=False)
    mobile        = Column(String(11), nullable=True)
    email         = Column(String(80), nullable=True)
    permission    = Column(Text, default='')
    login_count   = Column(Integer, nullable=False, default=0)
    last_login_ip = Column(String(128), nullable=False, default='')
    last_login_at = Column(Integer, nullable=True)
    status        = Column(Integer, nullable=False, default=1)  # 用户状态:(0 锁定, 1正常, 默认1)
    created_at    = Column(Integer, default=utime.timestamp)
    lang          = Column(String(2), nullable=False, default='')  # 默认语言

    @property
    def role_permission(self):
        query = "select permission from sys_admin_role where id='%s'" % self.role_id
        permission = AdminUser.session.execute(query).scalar()
        try:
            p2 = json.loads(permission) if permission else []
            return p2 if type(p2)==list else literal_eval(p2)
        except Exception as e:
            pass
            # raise e
        return []

    @property
    def user_permission(self):
        try:
            p2 = json.loads(self.permission)
            return p2 if type(p2)==list else literal_eval(p2)
        except Exception as e:
            pass
            # raise e
        return []

class AdminUserLoginLog(BaseModel):
    """
    系统管理员登录日志表
    """
    __tablename__ = 'sys_admin_user_login_log'

    id          = Column(Integer, primary_key=True, nullable=False, default=None)
    user_id     = Column(Integer, ForeignKey('sys_admin_user.id'))
    ip          = Column(String(40), nullable=False)
    client      = Column(String(20), nullable=True)
    created_at  = Column(Integer, default=utime.timestamp)


class AdminMenu(BaseModel):
    """
    后台菜单表
    """
    __tablename__ = 'sys_admin_menu'

    id          = Column(Integer, primary_key=True, nullable=False, default=None)
    user_id     = Column(Integer, ForeignKey('sys_admin_user.id'), nullable=False, default='0')
    parent_id   = Column(Integer, nullable=False, default=0)
    code        = Column(String(64), nullable=True)
    title       = Column(String(20), nullable=False)
    icon        = Column(String(20), nullable=False)
    path        = Column(String(200), nullable=False)
    param       = Column(String(200), nullable=False)
    target      = Column(String(20), nullable=False, default='_self')
    nav         = Column(Integer, nullable=False)
    sort        = Column(Integer, nullable=False, default=20)
    system      = Column(Integer, nullable=False)
    status      = Column(Integer, nullable=False)
    created_at  = Column(Integer, default=utime.timestamp)

    @classmethod
    def info(cls, id=None, path=None) -> dict:
        """
        获取对应菜单信息
        :param id:      对应菜单id
        :param path:    对应菜单地址
        :return:
        """
        query = cls.session.query(AdminMenu)
        if id:
            query = query.filter(AdminMenu.id == id)
        if path:
            path = path.split('?')[0]
            if path[-1:]=='/':
                path = path[0:-1]
            if path[-5:]=='.html':
                path = path[0:-5]

            query = query.filter(AdminMenu.path == path)

        row = query.first()
        row = row.as_dict() if row else None
        return row

    @classmethod
    def brand_crumbs(cls, id):
        """获取当前节点的面包屑

        [description]

        Arguments:
            id {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        menu = []
        row = cls.info(id=id)
        if row['parent_id']>0:
            menu.append(row)
            child = cls.brand_crumbs(row['parent_id'])
            if len(child):
                menu.extend(child)
        return menu


    @classmethod
    def main_menu(cls, parent_id=0, status=1, level=0, user=None):
        """获取后台主菜单(一级 > 二级 > 三级)
            后台顶部和左侧使用

            Keyword Arguments:
                parent_id {str} -- 父ID (default: {'0'})
                level {number} -- 层级数 (default: {0})
            Returns:
                [type] -- [description]
        """
        trees = []
        if not len(trees):
            filds = ['id', 'code', 'parent_id', 'title', 'path', 'param', 'target', 'icon']
            query = cls.session.query(AdminMenu)
            if status is not None:
                query = query.filter(AdminMenu.status == status)
            query = query.filter(AdminMenu.nav == 1)
            rows = query.order_by(AdminMenu.sort.asc()).all()
            # print('query.statement: ', query.statement)
            permission = user.user_permission + user.role_permission if user else []
            for row in rows:
                row = row.as_dict(filds)
                if row.get('parent_id')!=parent_id:
                    continue

                if level==5:
                    return trees

                if user and int(user.id) not in settings.SUPER_ADMIN and row['code'] not in permission:
                    continue
                row['children'] = cls.main_menu(row.get('id'), status, level+1, user=user)
                trees.append(row)
        return trees


    @staticmethod
    def children(parent_id=0, status=None, level=0,is_nav=None,permission=None,user_id=0):
        """获取指定节点下的所有子节点(不含快捷收藏的菜单)
        """
        trees = []
        if not len(trees):
            filds = ['id', 'code', 'parent_id', 'title', 'path', 'param', 'target', 'icon', 'sort', 'status','system','nav']
            query = AdminMenu.session.query(AdminMenu)
            if user_id>0:
                query = query.filter(AdminMenu.user_id == user_id)
            query = query.filter(AdminMenu.parent_id == parent_id)
            if status in [1,0]:
                query = query.filter(AdminMenu.status == status)
            if is_nav is not None and int(is_nav)==1:
                query = query.filter(AdminMenu.nav == is_nav)
            if permission is not None:
                query=query.filter(AdminMenu.code.in_(permission))
            rows = query.order_by(AdminMenu.sort.asc()).all()
            data = []
            for row in rows:
                if level==5:
                    return trees
                # row.append()
                row = row.as_dict(filds)
                row['label']=row['title']
                row['children'] = AdminMenu.children(row.get('id'), status, level+1,is_nav,permission=permission)
                trees.append(row)
        return trees


    @staticmethod
    def menu_option(id=''):
        """菜单选项"""
        menus = AdminMenu.main_menu(status=None)
        if not len(menus)>0:
            return ''
        option1 = '<option level="1" value="%s" %s>— %s</option>'
        option2 = '<option level="2" value="%s" %s>—— %s</option>'
        option3 = '<option level="3" value="%s" %s>——— %s</option>'
        html = ''
        for menu in menus:
            selected = 'selected' if id==menu.get('id', '') else ''
            title1 = menu.get('title', '')
            children1 = menu.get('children', [])
            html += option1 % (menu.get('id', ''), selected, title1)
            if not len(children1)>0:
                continue
            for menu2 in children1:
                selected2 = 'selected' if id==menu2.get('id', '') else ''
                title2 = menu2.get('title', '')
                children2 = menu2.get('children', [])
                html += option2 % (menu2.get('id', ''), selected2, title2)
                if not len(children2)>0:
                    continue
                for menu3 in children2:
                    selected3 = 'selected' if id==menu3.get('id', '') else ''
                    title3 = menu3.get('title', '')
                    html += option3 % (menu3.get('id', ''), selected3, title3)
        return html


    @staticmethod
    def get_user_menu(user_id):

        user_info=AdminUser.Q.filter(AdminUser.id==user_id).first()
        user=user_info.as_dict(['permission','status','role_id'])
        role_info=Role.Q.filter(Role.id==user['role_id']).first()
        role={
            'permission':''
        }
        if role_info:
            role=role_info.as_dict(['permission'])

        role_permission=[]
        user_permission=[]
        if role['permission'] and user['permission']:
            role_permission=json.loads(role['permission'])
            user_permission=json.loads(user['permission'])
        elif role['permission'] and not user['permission']:
            role_permission=json.loads(role['permission'])
        elif not role['permission'] and user['permission']:
            user_permission=json.loads(user['permission'])

        permission=role_permission + user_permission
        str_permission='('
        for val in permission:
            str_permission+="'"+val+"'"+','
        if len(str_permission)>2:
            str_permission=str_permission.rstrip(',')+')'
        else:
            str_permission=''

        db_conn = mysqldb()
        sql='select `id`,`user_id`,`parent_id`,`code`,`title`,`icon`,`path`,`param`,`target`,`sort`,`system`,`nav`,`status`,`created_at` from `sys_admin_menu` where status=1 and nav=1 and code in %s' %(str_permission)
        data=db_conn.execute(sql).fetchall()
        db_conn.commit()
        menu_list=[]
        for val in data:
            middle={}
            (id,user_id,parent_id,code,title,icon,path,param,target,sort,system,nav,status,created_at)=val
            middle['id']=id
            middle['user_id']=user_id
            middle['parent_id']=parent_id
            middle['code']=code
            middle['title']=title
            middle['icon']=icon
            middle['path']=path
            middle['param']=param
            middle['target']=target
            middle['sort']=sort
            middle['system']=system
            middle['nav']=nav
            middle['status']=status
            middle['created_at']=created_at
            middle['children']=[]
            middle['children']=AdminMenu.children(parent_id=id, status=1, level=1,is_nav=1,permission=permission)
            menu_list.append(middle)
        return menu_list

class Company(BaseModel):
    """
    公司表
    """
    __tablename__ = 'sys_company'
    id = Column(Integer, primary_key=True, nullable=False, default=None)
    company_name = Column(String(50), nullable=True, default='')
    description = Column(String(50), nullable=True, default='')
    type = Column(Enum('outer', 'inner'))  # 类型：（外部委派；内部)
    status = Column(Integer, default=1)  # 状态:( 0 待激活；1 激活)
    module = Column(Enum('review', 'collection', 'manage', 'service'))  # 业务：（审批；催收；管理；客服）
    created_at = Column(Integer, default=utime.timestamp)

    status_options = {
        '1': '激活',
        '0': '待激活'
    }

    type_options = {
        'outer': '外部委派',
        'inner': '内部'
    }

    module_options = {
        'review': '审批',
        'collection': '催收',
        'manage': '管理',
        'service': '客服'
    }

class BlackList(BaseModel):
    """
    黑名单表
    """
    __tablename__ = 'sys_blacklist'
    id = Column(Integer, primary_key=True, nullable=False, default=None)
    admin_id = Column(Integer)  # 管理员id
    order_number = Column(String(40))  # 贷款编号
    type = Column(Enum('ktp', 'mobile', 'full_name', 'company_name', 'company_phone'))  # 类型
    value = Column(String(100), nullable=True, default='')
    reason = Column(String(100), nullable=True, default='')
    status = Column(Integer, default=1)  # 0 禁用；1 启用, 默认1 删除 -1
    created_at = Column(Integer, default=utime.timestamp)

    status_options = {
        '1': '激活',
        '0': '待激活'
    }

    type_options = {
        'ktp': '身份证',
        'mobile': '手机号',
        'full_name': '姓名',
        'company_name': '公司名',
        'company_phone': '公司电话'
    }

class MessageTemplate(BaseModel):
    """
    消息模板表
    """
    __tablename__ = 'sys_message_template'
    id = Column(Integer, primary_key=True, nullable=False, default=None)
    category = Column(String(20))  # 模板类型
    content = Column(String(400))  # 内容
    status = Column(Integer, default=1)  # 状态:( 0 禁用；1 启用, 默认1 删除 -1)
    updated_at = Column(Integer, default=None)
    created_at = Column(Integer, default=utime.timestamp)


