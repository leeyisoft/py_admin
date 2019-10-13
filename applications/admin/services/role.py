#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
角色管理
"""
from trest.exception import JsonError
from trest.config import settings
from trest.utils import func
from applications.admin.models import Role


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
        try:
            Role.Q.filter(Role.id == role_id).update({'status': -1})
            Role.session.commit()
        except:
            raise JsonError('删除失败')
        return True

    @staticmethod
    def get_data(params, limit, page):
        """
        获取数据列表
        :param limit:
        :param page:
        :return:
        """
        query = Role.Q.filter(Role.status != -1)
        if params.get('id'):
            query = query.filter(Role.id == params['id'])

        if params.get('rolename'):
            query = query.filter(Role.rolename.like(f'%{params["rolename"]}%'))

        if params.get('status'):
            query = query.filter(Role.status == params['status'])

        # 查询非组角色
        query = query.order_by(Role.sort.desc()).order_by(Role.id.desc())
        pagelist_obj = query.paginate(page=page, per_page=limit)

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
        data = []
        role = Role.Q.filter(Role.status==1).all()
        for val in role:
            # val=val.as_dict()
            # val.pop('permission')
            data.append({'id': val.id, 'rolename': val.rolename})
        return data


    @staticmethod
    def status_options():
        """
        状态列表
        :return:
        """
        options = Role.status_options
        return (options, func.option_change(options))
