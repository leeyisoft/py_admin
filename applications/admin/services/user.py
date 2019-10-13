#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
用户管理
"""
from trest.exception import JsonError

from trest.config import settings
from trest.utils.encrypter import RSAEncrypter
from trest.utils import utime
from applications.common.utils import sys_config
from trest.utils.hasher import make_password
from ..models import AdminUser, Role
from ..models import AdminUserLoginLog


class AdminUserService:
    @staticmethod
    def is_super_role(uid, role_id=0):
        """"判断当前用户是否超级用户"""
        if not (uid>0):
            raise JsonError('用户ID不能为空')
        if not(role_id>0):
            user = AdminUserService.detail(uid)
            role_id = user.role_id
        return True if (int(uid) in settings.SUPER_ADMIN) or (int(role_id)==settings.SUPER_ROLE_ID) else False

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
            'last_login_at': utime.timestamp(3),
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
    def get_data(params, limit, page):
        """
        获取数据列表
        :param limit:
        :param page:
        :return:
        """
        query = AdminUser.Q
        if params['username']:
            query = query.filter(AdminUser.username.like(f"%{params.get('username')}%"))
        if params['mobile']:
            query = query.filter(AdminUser.mobile.like(f"%{params.get('mobile')}%"))
        if 'status' in params and params['status'] is not None:
            query = query.filter(AdminUser.status == params['status'])
        if params['role_id']:
            query = query.filter(AdminUser.role_id == params['role_id'])
        query = query.filter(AdminUser.status != -1).order_by(AdminUser.id.desc())
        pagelist_obj = query.paginate(page=page, per_page=limit)
        if pagelist_obj is None:
            raise JsonError('暂无数据')
        return pagelist_obj

    @staticmethod
    def detail(uid):
        """
        根据id获取详情
        :param id:
        :return:
        """
        if not (uid>0):
            raise JsonError('Detail用户ID不能为空')
        user = AdminUser.Q.filter(AdminUser.id == uid).first()
        user.mobile = user.mobile if user.mobile else None
        user.email = user.email if user.email else None
        return user

    @staticmethod
    def delete_data(uid):
        """
        删除用户
        :param uid: 用户ID
        :return:
        """
        if not uid:
            raise JsonError('DEL用户ID不能为空')
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
        if 'username' in user.keys():
            if user['username']:
                if AdminUserService.check_username(user['username'], user_id):
                    raise JsonError('名称已被占用')
            else:
                del user['username']

        if 'password' in user.keys():
            if user['password']:
                if settings.login_pwd_rsa_encrypt and int(rsa_encrypt) == 1 and len(user['password']) > 4:
                    private_key = sys_config('sys_login_rsa_priv_key')
                    user['password'] = RSAEncrypter.decrypt(user['password'], private_key)
                user['password'] = make_password(user['password'])
            else:
                del user['password']

        if 'email' in user.keys():
            if user['email']:
                if AdminUserService.check_email(user['email'], user_id):
                    raise JsonError('邮箱已被占用')
            else:
                user['email'] = None

        if 'mobile' in user.keys():
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
