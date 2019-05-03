#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
菜单管理
"""
from pyrestful.rest import JsonError
from applications.admin.models import AdminMenu


class MenuService:
    @staticmethod
    def delete_data(menu_id, super_role):
        """
        删除菜单
        :param menu_id:
        :param super_role: Boolean 是否为超级管理员
        :return:
        """
        code = 0
        msg = ""
        resdata = []
        menu = AdminMenu.Q.filter(AdminMenu.id == menu_id).first()
        if (not super_role) and menu.system == 1:
            raise JsonError('系统菜单，无法删除')

        count = AdminMenu.Q.filter(AdminMenu.parent_id == menu_id).count()
        if count > 0:
            raise JsonError('请先删除子菜单')

        AdminMenu.Q.filter(AdminMenu.id == menu_id).delete()
        AdminMenu.session.commit()
        return True

    @staticmethod
    def save_data(params, menu_id):
        """
        保存菜单
        :param params: 数据字典
        :param menu_id: 菜单ID
        :return:
        """
        code = 0
        msg = ""
        resdata = []
        if menu_id:
            try:
                AdminMenu.Q.filter(AdminMenu.id == menu_id).update(params)
                AdminMenu.session.commit()
            except Exception:
                raise JsonError()
        else:
            menu = AdminMenu(**params)
            AdminMenu.session.add(menu)
            AdminMenu.session.commit()
        return True

    @staticmethod
    def check_code(code):
        """
        检查授权码是否已被占用
        :param code: Code
        :return:
        """
        count = AdminMenu.Q.filter(AdminMenu.code==code).count()
        if count > 0:
            return True
        return False
