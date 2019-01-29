#!/usr/bin/env python
# -*- coding: utf-8  -*-

import os
import io
import hashlib
import mimetypes

from PIL import Image

from applications.core.settings_manager import settings
from applications.core.logger.client import SysLogger
from applications.core.models import Attach
from applications.core.utils import Func

class Uploader():
    @staticmethod
    def upload_img(file_md5, img, save_name, path, param):
        attach = Attach.Q.filter(Attach.file_md5==file_md5).first()
        if attach is not None:
            path_file = settings.STATIC_PATH+'/'+attach.path_file
            if os.path.isfile(path_file):
                return attach.as_dict()

        prefix = settings.STATIC_PATH + '/upload/'
        path = prefix + path
        if not os.path.exists(path):
            os.makedirs(path)
        path_file = path + save_name

        file_ext = FileUtil.file_ext(img['filename'])

        with open(path_file, 'wb') as f:
            f.write(img['body'])

        path = path_file.replace(settings.STATIC_PATH, '')
        path = path[1:] if path[0:1]=='/' else path

        param.update({
            'file_md5': file_md5,
            'file_ext': file_ext,
            'file_size': FileUtil.file_size(path_file),
            'file_mimetype': FileUtil.file_mimetype(path_file),
            'origin_name': img['filename'],
            'path_file': path,
        })
        attach = Attach(**param)
        Attach.session.merge(attach)
        Attach.session.commit()
        # print('param', param)
        return param


class FileUtil(object):
    """docstring for FileUtil"""

    @staticmethod
    def file_name(fname):
        return fname.split("/")[-1]

    @staticmethod
    def file_md5(fname):
        """
        from http://stackoverflow.com/questions/3431825/generating-a-md5-checksum-of-a-file
        """
        hash = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(40960), b""):
                hash.update(chunk)
        return hash.hexdigest()

    @staticmethod
    def file_ext(fname):
        ext = os.path.splitext(fname)[1]
        return ext[1:] if ext[0:1]=='.' else ext

    @staticmethod
    def file_mimetype(fname):
        return mimetypes.guess_type(fname)[0] or 'application/octet-stream'

    @staticmethod
    def file_size(fname):
        """获取文件的大小,结果保留两位小数，单位为Byte(1Byte=8Bit)
        """
        return os.path.getsize(fname)
