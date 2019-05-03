#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
用户管理
"""
from pyrestful.rest import JsonError
from applications.core.utils.encrypter import RSAEncrypter
from applications.core.utils import utime
from applications.core.utils import sys_config
from applications.core.settings_manager import settings
from applications.core.utils.hasher import make_password
from ..models import AdminUser
from ..models import AdminUserLoginLog


class AdminUserService:
    @staticmethod
    def login_success(user, handler):
        """
        后台用户登录成功之后事物处理函数
        """
        # 设置登录用户cookie信息
        handler.set_curent_user(user)

        user_id = user.id
        login_count = user.login_count if user.login_count else 0
        params = {
            'login_count': login_count + 1,
            'last_login_at': utime.timestamp(),
            'last_login_ip': handler.request.remote_ip,
        }
        AdminUser.Q.filter(AdminUser.id==user_id).update(params)

        params = {
            'id': 0,
            'user_id': user.id,
            'client': 'web',
            'ip': handler.request.remote_ip,
        }
        log = AdminUserLoginLog(**params)
        AdminUserLoginLog.session.add(log)
        AdminUserLoginLog.session.commit()
        return True

    @staticmethod
    def get_data(limit, page):
        """
        获取数据列表
        :param limit:
        :param page:
        :return:
        """
        pagelist_obj = AdminUser.Q.filter().paginate(page=page, per_page=limit)
        if pagelist_obj is None:
            raise JsonError('暂无数据')
        return pagelist_obj

    @staticmethod
    def get_info(uid):
        """
        根据id获取详情
        :param id:
        :return:
        """
        if not uid:
            raise JsonError('用户ID不能为空')

        user = AdminUser.Q.filter(AdminUser.id == uid).first()
        user.mobile = user.mobile if user.mobile else None
        user.email = user.email if user.email else None
        data_info = user.as_dict()
        return user

    @staticmethod
    def delete_data(uid):
        """
        删除用户
        :param uid: 用户ID
        :return:
        """
        if not uid:
            raise JsonError('用户ID不能为空')
        param = {
            'status': -1,
            'permission': '[]',
        }
        return AdminUserService.save_data(param, rsa_encrypt=0, user_id=uid)

    @staticmethod
    def check_username(username, user_id):
        """
        检查用户名是否已被占用
        :param username: 用户名
        :param user_id: 用户ID
        :return:
        """
        if user_id:
            count = AdminUser.Q.filter(AdminUser.id != user_id).filter(AdminUser.username == username).count()
        else:
            count = AdminUser.Q.filter(AdminUser.username == username).count()
        if count > 0:
            return True
        return False

    @staticmethod
    def check_email(email, user_id):
        """
        检查邮箱是否已被占用
        :param email: 邮箱
        :param user_id: 用户ID
        :return:
        """
        if user_id:
            count = AdminUser.Q.filter(AdminUser.id != user_id).filter(AdminUser.email == email).count()
        else:
            count = AdminUser.Q.filter(AdminUser.email == email).count()
        if count > 0:
            return True
        return False

    @staticmethod
    def check_mobile(mobile, user_id):
        """
        检查手机号是否已被占用
        :param mobile: 手机号
        :param user_id: 用户ID
        :return:
        """
        if user_id:
            count = AdminUser.Q.filter(AdminUser.id != user_id).filter(AdminUser.mobile == mobile).count()
        else:
            count = AdminUser.Q.filter(AdminUser.mobile == mobile).count()
        if count > 0:
            return True
        return False

    @staticmethod
    def save_data(user, rsa_encrypt, user_id):
        """
        保存用户数据
        :param user: 用户数据字典
        :param rsa_encrypt:
        :param user_id:
        :return:
        """
        if user['username']:
            if AdminUserService.check_username(user['username'], user_id):
                raise JsonError('名称已被占用')
        else:
            del user['username']

        # if user['password']:
        #     if settings.login_pwd_rsa_encrypt and int(rsa_encrypt) == 1 and len(user['password']) > 4:
        #         private_key = sys_config('sys_login_rsa_priv_key')
        #         user['password'] = RSAEncrypter.decrypt(user['password'], private_key)
        #     user['password'] = make_password(user['password'])
        # else:
            # del user['password']

        if user['email']:
            if AdminUserService.check_email(user['email'], user_id):
                raise JsonError('邮箱已被占用')
        else:
            user['email'] = None

        if user['mobile']:
            if AdminUserService.check_mobile(user['mobile'], user_id):
                raise JsonError('电话号码已被占用')
        else:
            user['mobile'] = None

        try:
            if user_id:
                AdminUser.Q.filter(AdminUser.id == user_id).update(user)
            else:
                user = AdminUser(**user)
                AdminUser.session.add(user)
        except Exception as e:
            raise e
        else:
            AdminUser.session.flush()
            AdminUser.session.commit()
        return user

    @staticmethod
    def change_pwd(param,rsa_encrypt,admin_id):
        """
        修改密码
        :param password:
        :param rsa_encrypt:
        :param admin_id:
        :return:
        """
        password=param['password']
        if param['password'] is not None:
            if int(rsa_encrypt) == 1 and len(param['password']) > 4:
                private_key = sys_config('sys_login_rsa_priv_key')
                password = RSAEncrypter.decrypt(param['password'], private_key)
            password= make_password(password)
        else:
            raise JsonError('参数无效')

        AdminUser.Q.filter(AdminUser.id==admin_id)\
            .update({'password':password})
        AdminUser.session.commit()
        return True
