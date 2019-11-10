#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""AdminUser控制器
"""
import json
from trest.router import get
from trest.router import put
from trest.router import post
from trest.router import delete
from trest.exception import JsonError
from trest.config import settings
from trest.logger import SysLogger
from trest.utils import func
from trest.utils.hasher import make_password
from trest.utils.file import Uploader
from trest.utils.file import FileUtil

from applications.common.utils import sys_config

from applications.admin.utils import required_permissions
from applications.admin.utils import admin_required_login

from applications.admin.services.admin_user import AdminUserService
from applications.admin.services.admin_menu import AdminMenuService

from .common import CommonHandler


class AdminUserHandler(CommonHandler):

    @post('admin_user')
    @admin_required_login
    @required_permissions()
    def admin_user_post(self, *args, **kwargs):
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
            raise JsonError('用户名不能为空')
        if not password:
            raise JsonError('密码不能为空')
        param = {
            'status': status,
            'username': username,
            'password': password,
            'mobile': mobile,
            'email': email,
            'permission':permission,
            'role_id':role_id
        }

        AdminUserService.insert(param)
        return self.success()

    @get('admin_user/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def admin_user_get(self, id):
        """获取单个记录
        """
        obj = AdminUserService.get(id)
        data = obj.as_dict() if obj else {}
        return self.success(data = data)

    @get(['admin_user','admin_user/?(?P<category>[a-zA-Z0-9_]*)'])
    @admin_required_login
    @required_permissions()
    def admin_user_list_get(self, category = '', *args, **kwargs):
        """列表、搜索记录
        """
        page = int(self.get_argument('page', 1))
        per_page = int(self.get_argument('limit', 10))
        title = self.get_argument('title', None)
        status = self.get_argument('status', None)
        mobile = self.get_argument('mobile', None)
        username = self.get_argument('username', None)
        role_id = self.get_argument('role_id', None)

        param = {}
        if category:
            param['category'] = category
        if title:
            param['title'] = title
        if status:
            param['status'] = status
        if mobile:
            param['mobile'] = mobile
        if username:
            param['username'] = username
        if role_id:
            param['role_id'] = role_id

        pagelist_obj = AdminUserService.data_list(param, page, per_page)
        items = []
        for val in pagelist_obj.items:
            data = val.as_dict()
            if not data['permission'] or data['permission']=='':
                data['permission']=[]
            else:
                data['permission']=data['permission'].replace('\\','').replace('[','').replace(']','').replace('"','').split(',')
            items.append(data)
        resp = {
            'page':page,
            'per_page':per_page,
            'total':pagelist_obj.total,
            'items':items,
        }
        return self.success(data = resp)

    @put('admin_user/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def admin_user_put(self, id, *args, **kwargs):
        role_id = self.get_argument('role_id', None)
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        rsa_encrypt = self.get_argument('rsa_encrypt', '0')
        email = self.get_argument('email', None)
        mobile = self.get_argument('mobile', None)
        status = self.get_argument('status', '0')
        permission = self.get_argument('permission',[])

        if not id:
            raise JsonError('Edit用户ID不能为空')
        param = {
            'id': id,
            'status': status,
            'username': username,
            'mobile': mobile,
            'email': email
        }
        param['permission'] = '[]'
        try:
            param['permission'] = json.dumps(permission)
        except Exception as e:
            pass
        if role_id:
            param['role_id'] = role_id
        AdminUserService.update(id, param, rsa_encrypt)
        return self.success(data = param)

    @delete('admin_user/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def admin_user_delete(self, id, *args, **kwargs):
        param = {
            'status':-1
        }
        AdminUserService.update(id, param)
        return self.success()

    @get('/admin/init')
    def admin_init_get(self):
        """系统配置信息"""
        rsa_encrypt = sys_config('login_pwd_rsa_encrypt')
        public_key = sys_config('login_rsa_pub_key')
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


class UnlockAdminHandler(CommonHandler):
    @put('/admin/admin/unlocked')
    @admin_required_login
    def unlock_user(self):
        """锁屏解锁"""
        password = self.get_argument('password', None)

        if not password:
            raise JsonError('请输入密码')

        is_rsa=sys_config('login_pwd_rsa_encrypt')
        if  int(is_rsa) == 1:
            private_key = sys_config('login_rsa_priv_key')
            try:
                password = RSAEncrypter.decrypt(password, private_key)
            except Exception as e:
                raise JsonError(msg='签名失败',code=11)
        user_info=self.get_current_user()
        check=AdminUser.Q.filter(AdminUser.id == user_info['id']).first()
        if check is None:
            raise JsonError('用户信息出错')

        if check_password(password,check.password)==False:
            raise JsonError('密码错误')

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
            raise JsonError('参数必须')
        check = AdminUser.Q.filter(AdminUser.id == admin_id).first()
        if check is None:
            raise JsonError('参数无效')
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
            raise JsonError('不支持的action')

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
                raise JsonError('上传失败')

        raise JsonError('参数错误')
