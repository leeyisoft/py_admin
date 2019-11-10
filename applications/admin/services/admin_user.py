#!/usr/bin/env python
# -*- coding: utf-8 -*-
from trest.utils import utime
from trest.logger import SysLogger
from trest.config import settings
from trest.exception import JsonError
from trest.utils.encrypter import RSAEncrypter
from trest.utils.hasher import make_password
from applications.common.utils import sys_config
from applications.common.models.admin_user import AdminUser
from applications.common.models.admin_user_login_log import AdminUserLoginLog



class AdminUserService:
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
        query = AdminUser.Q

        if 'status' in where.keys():
            query = query.filter(AdminUser.status == where['status'])
        else:
            query = query.filter(AdminUser.status != -1)

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
            AdminUser Model 实例 | None
        """
        if not id:
            raise JsonError('ID不能为空')
        obj = AdminUser.Q.filter(AdminUser.id == id).first()
        return obj

    @staticmethod
    def update(user_id, user, rsa_encrypt = 0):
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
                    private_key = sys_config('login_rsa_priv_key')
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
            AdminUser.session.commit()
        return user

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
        param.pop('_xsrf', None)
        param['created_at'] = utime.timestamp(3)
        try:
            data = AdminUser(**param)
            AdminUser.session.add(data)
            AdminUser.session.commit()
            return True
        except Exception as e:
            AdminUser.session.rollback()
            SysLogger.error(e)
            raise JsonError('insert error')

    @staticmethod
    def is_super_role(uid, role_id=0):
        """"判断当前用户是否超级用户"""
        if not (uid>0):
            raise JsonError('用户ID不能为空')
        if not(role_id>0):
            user = AdminUserService.get(uid)
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
                private_key = sys_config('login_rsa_priv_key')
                password = RSAEncrypter.decrypt(param['password'], private_key)
            password= make_password(password)
        else:
            raise JsonError('参数无效')

        AdminUser.Q.filter(AdminUser.id==admin_id)\
            .update({'password':password})
        AdminUser.session.commit()
        return True

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
