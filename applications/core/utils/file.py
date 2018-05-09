#!/usr/bin/env python
# -*- coding: utf-8  -*-

import os
import io
import hashlib
import mimetypes

from PIL import Image

from applications.core.settings_manager import settings
from applications.core.logger.client import SysLogger
from applications.core.db.dbalchemy import Attach

class Uploader():
    @staticmethod
    def upload_img(img, save_name, path, param):
        prefix = settings.STATIC_PATH + '/upload/'
        path = prefix + path
        if not os.path.exists(path):
            os.makedirs(path)
        path_file = path + save_name

        file_ext = FileUtil.file_ext(img['filename'])

        with open(path_file, 'wb') as f:
            # image有多种打开方式，一种是 Image.open('xx.png')
            # 另一种就是 Image.open(StringIO(buffer))
            im = Image.open(io.BytesIO(img['body']))
            # 修改图片大小resize接受两个参数, 第一个是宽高的元组数据,第二个是对图片细节的处理，本文表示抗锯齿
            # im = im.resize((248, 248), Image.ANTIALIAS)
            #创建一个文件流
            imgio = io.BytesIO()
            im.save(imgio, format=file_ext)
            # 这是获取io中的内容
            im_data = imgio.getvalue()
            f.write(im_data)

        path = path_file.replace(settings.STATIC_PATH, '')
        path = path[1:] if path[0:1]=='/' else path

        file_md5 = FileUtil.file_md5(path_file)
        param.update({
            'file_md5': file_md5,
            'file_ext': file_ext,
            'file_size': FileUtil.file_size(path_file),
            'file_mimetype': FileUtil.file_mimetype(path_file),
            'origin_name': img['filename'],
            'path_file': path,
        })
        count = Attach.Q.filter(Attach.file_md5==file_md5).count()
        if not(count>0):
            attach = Attach(**param)
            Attach.session.add(attach)
            Attach.session.commit()

        return param

    @staticmethod
    def upload_file2(file, path):
        code = 0
        msg = ''

        if not os.path.exists(path):
            os.makedirs(path)

        try:
            file_name = '%s%s' % (str(uuid.uuid4()).replace('-',''), FileUtil.file_ext(file.name))
            save_file = os.path.join(path, file_name)
            with open(save_file, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            code = 0
            msg = save_file
        except Exception as e:
            code = 1
            msg = e
        return (status, msg)

class FileUtil(object):
    """docstring for FileUtil"""

    @staticmethod
    def file_name(fname):
        return fname.split("/")[-1]

    @staticmethod
    def file_md5(fname):
        """
        from http://stackoverflow.com/quest-
        ions/3431825/generating-a-md5-checksum-of-a-file
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
