#!/usr/bin/env python
# -*- coding: utf-8 -*-
from trest.utils import utime
from trest.config import settings
from trest.logger import SysLogger
from trest.exception import JsonError
from trest.utils import func
from trest.utils.file import FileUtil
from trest.utils.file import Uploader


class UploaderService(object):
    @staticmethod
    def upload(current_uid, ip, action, imgfile, path):
        action_set = (
            'advertising',
            'avatar',
            'article/thumb',
            'article/regulation',
            'article/news',
            'product',
            'friendlink',
        )
        if action not in action_set:
            raise JsonError('不支持的action')
        resp_data = []
        for img in imgfile:
            # 对文件进行重命名
            file_ext = FileUtil.file_ext(img['filename'])
            path = '%s/' % path
            file_md5 = func.md5(img['body'])
            save_name =  f'{file_md5}.{file_ext}'
            try:
                param = Uploader.upload_img(file_md5, img, save_name, path, {
                    'user_id': current_uid,
                    'ip': ip,
                })
                resp_data.append(param)
            except Exception as e:
                if settings.debug:
                    raise e
                SysLogger.error(e)
                raise JsonError('上传失败')
        return resp_data
