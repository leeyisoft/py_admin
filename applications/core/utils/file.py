#!/usr/bin/env python
# -*- coding: utf-8  -*-

import os
import hashlib
import mimetypes
import oss2
import tornado.httputil

from applications.core.settings_manager import settings
from applications.core.utils.image import download_img


class Uploader():

    @staticmethod
    def oss(upload_file, upload_path='test', headers=None, protocol='http'):
        """
        上传文件到阿里oss
        :param upload_file:    上传的文件
        :param upload_path:    上传的地址
        :param headers:        当网络文件时的下载头
        :param protocol:       返回文件的协议
        :return:
        """
        # oss 配置
        accesskeyid = settings.oss_config.get('accesskeyid')
        accesskey   = settings.oss_config.get('accesskey')
        endpoint    = settings.oss_config.get('endpoint')
        bucket_name = settings.oss_config.get('bucket_name')
        auth        = oss2.Auth(accesskeyid, accesskey)
        bucket      = oss2.Bucket(auth, '%s://%s' % (protocol, endpoint,), bucket_name)

        # 文件类型
        if not isinstance(upload_file, tornado.httputil.HTTPFile):
            # 本地文件
            if os.path.isfile(upload_file):
                file_path = upload_file
                ext = upload_file.split('.')[-1]
            # 网络文件
            else:
                (file_path, ext) = download_img(upload_file, headers=headers)
            upload_name = '%s/%s.%s' % (upload_path, FileUtil.file_md5(file_path), ext)
            bucket.put_object_from_file(upload_name, file_path)
        # 数据流类型
        else:
            hash = hashlib.md5()
            hash.update(upload_file['body'])
            ext = upload_file['filename'].split('.')[-1]
            file_name = hash.hexdigest()
            upload_name = '%s/%s.%s' % (upload_path, file_name, ext)
            bucket.put_object(upload_name, upload_file['body'])
        return '%s://%s.%s/%s' % (protocol, bucket_name, endpoint, upload_name)

    @staticmethod
    def upload_img(file_md5, img, save_name, path, param):
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
