#!/usr/bin/env python
# -*- coding: utf-8 -*-
from trest.utils import utime
from trest.config import settings
from trest.logger import SysLogger
from trest.exception import JsonError
from trest.utils.encrypter import RSAEncrypter
from trest.utils.hasher import make_password
from applications.common.utils import sys_config
from applications.common.models.admin_user import AdminUser
from applications.common.models.admin_user_login_log import AdminUserLoginLog

from applications.admin.assemblers.admin_user  import AdminUserAssembler


class AdminUserService(object):
    @staticmethod
    def page_list(where, page, per_page):
        """列表记录
        Arguments:
            where dict -- 查询条件
            page int -- 当前页
            per_page int -- 每页记录数

        return:
            Paginate 对象 | None
        """
        query = AdminUser.Q

        if 'mobile' in where.keys():
            query = query.filter(AdminUser.mobile == where['mobile'])
        if 'username' in where.keys():
            query = query.filter(AdminUser.username == where['username'])
        if 'role_id' in where.keys():
            query = query.filter(AdminUser.role_id == where['role_id'])
        if 'status' in where.keys():
            query = query.filter(AdminUser.status == where['status'])
        else:
            query = query.filter(AdminUser.status != -1)

        pagelist_obj = query.paginate(page=page, per_page=per_page)

        if pagelist_obj is None:
            raise JsonError('暂无数据')
        return AdminUserAssembler.page_list(pagelist_obj, page, per_page)

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
    def update(user_id, param, rsa_encrypt = 0):
        """
        保存用户数据
        :param user: 用户数据字典
        :param rsa_encrypt:
        :param user_id:
        :return:
        """
        columns = [i for (i, _) in AdminUser.__table__.columns.items()]
        param = {k:v for k,v in param.items() if k in columns}
        if 'updated_at' in columns:
            param['updated_at'] = utime.timestamp(3)

        if 'username' in param.keys():
            if param['username']:
                if AdminUserService.check_username(param['username'], user_id):
                    raise JsonError('名称已被占用')
            else:
                del param['username']

        if 'password' in param.keys():
            if param['password']:
                if settings.login_pwd_rsa_encrypt and int(rsa_encrypt) == 1 and len(param['password']) > 4:
                    private_key = sys_config('login_rsa_priv_key')
                    param['password'] = RSAEncrypter.decrypt(param['password'], private_key)
                param['password'] = make_password(param['password'])
            else:
                del param['password']

        if 'email' in param.keys():
            if param['email']:
                if AdminUserService.check_email(param['email'], user_id):
                    raise JsonError('邮箱已被占用')
            else:
                param['email'] = None

        if 'mobile' in param.keys():
            if param['mobile']:
                if AdminUserService.check_mobile(param['mobile'], user_id):
                    raise JsonError('电话号码已被占用')
            else:
                param['mobile'] = None

        try:
            if user_id:
                AdminUser.Update.filter(AdminUser.id == user_id).update(param)
            else:
                obj = AdminUser(**param)
                AdminUser.session.add(obj)
        except Exception as e:
            raise e
        else:
            AdminUser.session.commit()
        return True

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
        columns = [i for (i, _) in AdminUser.__table__.columns.items()]
        param = {k:v for k,v in param.items() if k in columns}
        if 'created_at' in columns:
            param['created_at'] = utime.timestamp(3)
        try:
            obj = AdminUser(**param)
            AdminUser.session.add(obj)
            AdminUser.session.commit()
            return True
        except Exception as e:
            AdminUser.session.rollback()
            SysLogger.error(e)
            raise JsonError('insert error')

    @staticmethod
    def is_super_role(uid, role_id=0):
        """"判断当前用户是否超级用户"""
        if not uid:
            raise JsonError('用户ID不能为空')
        if not role_id:
            user = AdminUserService.get(uid)
            role_id = user.role_id if user else 0
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
        AdminUser.Update.filter(AdminUser.id==user_id).update(params)

        params = {
            'id': 0,
            'user_id': user.id,
            'client': 'web',
            'ip': handler.request.remote_ip,
            'created_at': utime.timestamp(3),
        }
        log = AdminUserLoginLog(**params)
        AdminUserLoginLog.session.add(log)
        AdminUserLoginLog.session.commit()
        return True

    @staticmethod
    def change_pwd(password, rsa_encrypt, admin_id):
        """
        修改密码
        :param password:
        :param rsa_encrypt:
        :param admin_id:
        :return:
        """
        admin = AdminUser.Q.filter(AdminUser.id == admin_id).first()
        if admin is None:
            raise JsonError('参数无效')

        if password :
            if int(rsa_encrypt) == 1 and password:
                private_key = sys_config('login_rsa_priv_key')
                password = RSAEncrypter.decrypt(password, private_key)
            password= make_password(password)
        else:
            raise JsonError('参数无效')

        AdminUser.Update.filter(AdminUser.id==admin_id)\
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
        return True if count > 0 else False

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
        return True if count > 0 else False

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
        return True if count > 0 else False

    @staticmethod
    def admin_init(xsrf_token):
        rsa_encrypt = sys_config('login_pwd_rsa_encrypt')
        public_key = sys_config('login_rsa_pub_key')

        return {
            'rsa_encrypt': int(rsa_encrypt),
            'public_key': public_key,
            'xsrf_token': xsrf_token,
        }

    @staticmethod
    def unlock_user(user_id, password):
        is_rsa = sys_config('login_pwd_rsa_encrypt')
        if  int(is_rsa) == 1:
            private_key = sys_config('login_rsa_priv_key')
            try:
                password = RSAEncrypter.decrypt(password, private_key)
            except Exception as e:
                raise JsonError(msg='签名失败', code=11)
        user = AdminUser.Q.filter(AdminUser.id == user_id).first()
        if user is None:
            raise JsonError('用户信息出错')

        if check_password(password, user.password) == False:
            raise JsonError('密码错误')
        return True
