#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
角色管理
"""
from pyrestful.rest import JsonError
from applications.admin.models import Role, Company
from applications.core.settings_manager import settings
from applications.core.utils import func


class RoleService:
    @staticmethod
    def delete_data(role_id):
        """
        删除角色
        :param role_id:
        :return:
        """
        # 系统角色，非超级管理员不允许编辑权限和删除
        if role_id is None:
            raise JsonError('角色ID缺失')
        if int(role_id) in settings.SYS_ROLE:
            raise JsonError('角色不允许删除')
        Role.Q.filter(Role.id == role_id).delete()
        Role.session.commit()
        return True

    @staticmethod
    def get_data(limit, page):
        """
        获取数据列表
        :param limit:
        :param page:
        :return:
        """
        code = 0
        msg = ""
        resdata = (0, None)
        pagelist_obj = Role.Q.filter().paginate(page=page, per_page=limit)
        if pagelist_obj is None:
            raise JsonError('暂无数据')
        return pagelist_obj

    @staticmethod
    def check_rolename(rolename, roleid):
        """
        检查角色名是否已被占用
        :param rolename: 角色名
        :param roleid: 角色ID
        :return:
        """
        if roleid:
            count = Role.Q.filter(Role.id!=roleid).filter(Role.rolename==rolename).count()
        else:
            count = Role.Q.filter(Role.rolename==rolename).count()
        return True if count > 0 else  False

    @staticmethod
    def save_data(is_super_role,role,roleid=None):
        """
        保存角色
        :param role:
        :return:
        """

        if roleid is None:
            if not role['rolename']:
                raise JsonError('分组名称不能为空')
            if RoleService.check_rolename(role['rolename'], roleid):
                raise JsonError('名称已被占用')
            # 添加催收员默认分配collector的权限
            permission = RoleService.collector_role(role, roleid)
            if permission:
                role['permission'] = permission
            role = Role(**role)
            Role.session.add(role)
            Role.session.commit()
        else:
            # 当编辑的是collector角色时，同时更新所有催收员角色
            if int(roleid) in settings.SYS_ROLE:
                if not is_super_role:
                    raise JsonError('系统角色只有超级管理员可编辑')
                RoleService.collector_role(role, roleid)
            if role['rolename']:
                if RoleService.check_rolename(role['rolename'], roleid):
                    raise JsonError('名称已被占用')
            else:
                del role['rolename']
            Role.Q.filter(Role.id==roleid).update(role)
            Role.session.commit()
        return True

    @staticmethod
    def get_info(roleid):
        code = 0
        msg = ""
        resdata = []
        if not roleid:
            raise JsonError('角色ID不能为空')
        role = Role.Q.filter(Role.id == roleid).first()
        return role

    @staticmethod
    def get_valid_role():
        """获取有效的角色"""
        data=[]
        role=Role.Q.filter(Role.status==1).all()
        for val in role:
            val=val.as_dict()
            if not val['permission'] or val['permission']=='':
                val['permission']=[]
            else:
                val['permission']=val['permission'].replace('\\','').replace('[','').replace(']','').replace('"','').split(',')
            data.append(val)
        return data

    @staticmethod
    def data_list(param, page, limit):
        """
        催收组数据列表
        :param param:
        :param page:
        :param limit:
        :return:
        """
        query = Role.session \
            .query(Role.id, Role.rolename, Role.category, Role.description, Role.status,Company.id, Company.company_name) \
            .join(Company, Company.id == Role.company_id)
        if param['company_id']:
            query = query.filter(Role.company_id == param['company_id'])

        if param['status']:
            query = query.filter(Role.status == param['status'])

        if param['category']:
            query = query.filter(Role.category == param['category'])

        pagelist_obj = query.paginate(page=page, per_page=limit)
        if pagelist_obj is None:
            raise JsonError('暂无数据')
        return pagelist_obj

    @staticmethod
    def role_options():
        """
        催收组选项列表
        :return:
        """
        data = Role.session.query(Role.id, Role.rolename) \
            .filter(Role.status == 1).all()
        item_dict = {}
        item_list = []
        if not data:
            return (item_dict, item_list)
        for raw in data:
            temp = {}
            (temp['value'], temp['label']) = raw
            item_list.append(temp)
            item_dict[temp['value']] = temp['label']
        return (item_dict, item_list)


    @staticmethod
    def status_options():
        """
        状态列表
        :return:
        """
        options = Role.status_options
        return (options, func.option_change(options))

    @staticmethod
    def collector_role(role,id):
        """
        催收员角色权限与 collector角色权限同步
        :param role:
        :return:
        """
        permission = None
        if id is None:
            # 新增
            if 'category' not in role.keys():
                return False
            if int(role['category']) == 1:
                # 催收员
                permission = Role.session.query(Role.permission).filter(Role.id == 4).scalar()
            else:
                # 管理员
                # permission = Role.session.query(Role.permission).filter(Role.id == 5).scalar()
                pass
        else:
            if int(id) == 4:
                permission = role['permission']
                Role.Q.filter(Role.category == 1).update({'permission': permission})
                Role.session.commit()
        return permission
