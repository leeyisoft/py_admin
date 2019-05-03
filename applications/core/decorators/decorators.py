#!/usr/bin/env python
# -*- coding: utf-8  -*-
from tornado.util import import_object

from applications.core.utils.encrypter import RSAEncrypter
from applications.core.settings_manager import settings


def required_permissions(*dargs, **dkargs):
    """权限控制装饰器
    """
    AdminUser = import_object('applications.admin.models.AdminUser')
    SUPER_ADMIN = import_object('applications.configs.settings.SUPER_ADMIN')
    def wrapper(method):
        # @functools.wraps(method)
        def _wrapper(*args, **kargs):
            code = dargs[0]
            self = args[0]
            user_id = self.current_user.get('id')
           
            if int(user_id) in SUPER_ADMIN:
                return method(*args, **kargs)

            obj = AdminUser.Q.filter(AdminUser.id==user_id).first()
           
            if not obj:
                return self.error('未授权', 401)
            if not code:
                return self.error('未授权', 401)

            permission = obj.user_permission + obj.role_permission
            if type(code)==str:
                permission.append('admin:menu:web_admin_list')
                if code in permission:
                    return method(*args, **kargs)
            elif type(code)==list:
                if any([cd in permission for cd in code]):
                    return method(*args, **kargs)
            return self.error('未授权', 401)

        return _wrapper
    return wrapper
