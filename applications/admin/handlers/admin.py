#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""
import json
import tornado

from trest.router import get
from trest.router import put
from trest.router import post
from trest.router import delete
from trest.exception import JsonError
from trest.config import settings
from trest.logger.client import SysLogger
from trest.utils import func
from trest.utils.hasher import make_password
from trest.utils.file import Uploader
from trest.utils.file import FileUtil

from applications.common.utils import sys_config
from applications.admin.utils import required_permissions
from applications.admin.utils import admin_required_login

from ..services.user import AdminUserService
from ..services.menu import AdminMenuService
from ..models import AdminUser

from .common import CommonHandler


class AdminHandler(CommonHandler):
    @get('/admin/init')
    def admin_init_get(self):
        """系统配置信息"""
        rsa_encrypt = sys_config('login_pwd_rsa_encrypt')
        public_key = sys_config('sys_login_rsa_pub_key')
        region_code = {}
        # for k in const.region_code:
        #     val = const.region_code[k]
        #     val['region'] = self.locale.translate(str(val['region']))
        #     region_code[k] = val

        data = {
            'rsa_encrypt': int(rsa_encrypt),
            # 'region_code': region_code,
            'public_key': public_key,
            'xsrf_token': self.xsrf_token.decode("utf-8"),
        }
        return self.success(msg='成功', data=data)

    @get('/admin/info')
    @admin_required_login
    def admin_info_get(self, *args, **kwargs):
        data = {
            'name': 'admin',
            'avatar' : self.static_url('image/default_avatar.jpg'),
            'menus': AdminMenuService.menu_list(1),
        }
        return self.success(data = data)

    @get('/admin/admin')
    @admin_required_login
    @required_permissions()
    def admin_get(self, *args, **kwargs):
        """管理员列表"""
        params = {
            'mobile': self.get_argument('phone', None),
            'status': self.get_argument('status', None),
            'username': self.get_argument('username', None),
            'role_id': self.get_argument('role_id', None),
        }
        limit = self.get_argument('limit', '10')
        page = self.get_argument('page', '1')

        pagelist_obj = AdminUserService.get_data(params, limit, page)
        items2=[]
        for item in pagelist_obj.items:
            val = item.as_dict()
            if not val['permission'] or val['permission']=='':
                val['permission']=[]
            else:
                val['permission']=val['permission'].replace('\\','').replace('[','').replace(']','').replace('"','').split(',')
            items2.append(val)

        params = {
            'page':page,
            'per_page':limit,
            'total':pagelist_obj.total,
            'items': items2,
        }
        return self.success(data=params)


    @post('/admin/admin')
    @admin_required_login
    @required_permissions()
    def admin_post(self):
        """新增管理员"""
        role_id = self.get_argument('role_id', None)
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        email = self.get_argument('email', None)
        mobile = self.get_argument('mobile', None)
        status = self.get_argument('status', '1')
        permission = self.get_argument('permission',[])
        rsa_encrypt = self.get_argument('rsa_encrypt',1)

        if not username:
            return self.error('用户名不能为空')
        if not password:
            return self.error('密码不能为空')
        user = {
            'status': status,
            'username': username,
            'password': password,
            'mobile': mobile,
            'email': email,
            'permission':permission,
            'role_id':role_id
        }

        AdminUserService.save_data(user, rsa_encrypt, None)
        return self.success()

    @put('/admin/admin')
    @admin_required_login
    @required_permissions()
    def admin_put(self):
        role_id = self.get_argument('role_id', None)
        uid = self.get_argument('user_id', None)
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        rsa_encrypt = self.get_argument('rsa_encrypt', '0')
        email = self.get_argument('email', None)
        mobile = self.get_argument('mobile', None)
        status = self.get_argument('status', '0')
        permission = self.get_argument('permission',[])

        if not uid:
            raise JsonError('Edit用户ID不能为空')
        user = {
            'id': uid,
            'status': status,
            'username': username,
            'mobile': mobile,
            'email': email
        }
        user['permission'] = '[]'
        try:
            user['permission'] = json.dumps(permission)
        except Exception as e:
            pass
        if role_id:
            user['role_id'] = role_id
        AdminUserService.save_data(user, rsa_encrypt, uid)
        return self.success()

    @delete('/admin/admin')
    @admin_required_login
    @required_permissions()
    def admin_delete(self):
        """删除用户
        """
        uid = self.get_argument('user_id', None)
        AdminUserService.delete_data(uid)
        return self.success()


class UnlockAdminHandler(CommonHandler):
    @put('/admin/admin/unlocked')
    @admin_required_login
    def unlock_user(self):
        """锁屏解锁"""
        password = self.get_argument('password', None)

        if not password:
            return self.error('请输入密码')

        is_rsa=sys_config('login_pwd_rsa_encrypt')
        if  int(is_rsa) == 1:
            private_key = sys_config('sys_login_rsa_priv_key')
            try:
                password = RSAEncrypter.decrypt(password, private_key)
            except Exception:
                return self.error(msg='签名失败',code=11)
        user_info=self.get_current_user()
        check=AdminUser.Q.filter(AdminUser.id == user_info['id']).first()
        if check is None:
            return self.error('用户信息出错')

        if check_password(password,check.password)==False:
            return self.error('密码错误')

        return self.success()

class AdminChangePwdHandler(CommonHandler):
    @put('/admin/admin/change_pwd')
    @admin_required_login
    @required_permissions()
    def admin_change_pwd(self):
        """
        修改密码
        :return:
        """
        password = self.get_argument('password',None)
        rsa_encrypt = self.get_argument('rsa_encrypt',None)
        admin_id = self.get_argument('admin_id',None)
        if password is None or rsa_encrypt is None or admin_id is None:
            return self.error('参数必须')
        check = AdminUser.Q.filter(AdminUser.id == admin_id).first()
        if check is None:
            return self.error('参数无效')
        user = {
            'password':password
        }
        AdminUserService.change_pwd(user, rsa_encrypt, admin_id)
        return self.success()

class UploaderHandler(CommonHandler):
    @post('/admin/uploader')
    @admin_required_login
    @required_permissions()
    def post(self, *args, **kwargs):
        """上传图片"""
        user_id = self.current_user.get('id')

        next = self.get_argument('next', '')
        imgfile = self.request.files.get('file')
        action = self.get_argument('action', None)
        path = self.get_argument('path', 'default_path')

        action_set = (
            'advertising',
            'avatar',
            'article/thumb',
            'article/regulation',
            'article/news',
            'product',
        )
        if action not in action_set:
            return self.error('不支持的action')

        for img in imgfile:
            print('img', type(img))
            # 对文件进行重命名
            file_ext = FileUtil.file_ext(img['filename'])
            path = '%s/' % path
            save_name = img['filename']
            file_md5 = func.md5(img['body'])
            if action=='avatar':
                save_name = '%s.%s' %(user_id, file_ext)
            else:
                save_name = '%s.%s' %(file_md5, file_ext)
            try:
                param = Uploader.upload_img(file_md5, img, save_name, path, {
                    'user_id': user_id,
                    'ip': self.request.remote_ip,
                })
                return self.success(data=param)
            except Exception as e:
                if settings.debug:
                    raise e
                SysLogger.error(e)
                return self.error('上传失败')

        return self.error('参数错误')
