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

from applications.admin.utils import required_permissions
from applications.admin.utils import admin_required_login

from applications.admin.services.uploader import UploaderService

from .common import CommonHandler


class UploaderHandler(CommonHandler):
    @post('/admin/uploader')
    @admin_required_login
    @required_permissions()
    def post(self, *args, **kwargs):
        """上传图片"""
        current_uid = self.current_user.get('id')

        next = self.get_argument('next', '')
        imgfile = self.request.files.get('file')
        action = self.get_argument('action', None)
        path = self.get_argument('path', 'default_path')
        ip = self.request.remote_ip
        resp_data = UploaderService.upload(current_uid, ip, action, imgfile, path)
        if len(imgfile) == 1:
            resp_data = resp_data[0]
        return self.success(data=resp_data)
