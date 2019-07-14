#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
处理配置管理
"""
from trest.exception import JsonError
from applications.common.models.base import Config
from trest.settings_manager import settings
from trest.utils import sys_config

class ConfigService:
    @staticmethod
    def get_data(param,limit, page):
        """
        获取配置数据列表
        :param limit:
        :param page:
        :return:
        """
        query=Config.Q.order_by(Config.sort.desc())
        if param['key']:
            query=query.filter(Config.key==param['key'])
        pagelist_obj = query.paginate(page=page, per_page=limit)
        if pagelist_obj is None:
            raise JsonError('暂无数据')
        return pagelist_obj

    @staticmethod
    def delete_data(key):
        """
        删除系统配置
        :param key:
        :return:
        """
        config = Config.Q.filter(Config.key == key).first()
        if not config:
            raise JsonError('配置不存在')
        if config.system == 1:
            raise JsonError('系统配置不可删除')
        Config.Q.filter(Config.key == key).delete()
        Config.session.commit()
        # 同时删除对应缓存
        sys_config(key, 'delete_key_value')
        return True

    @staticmethod
    def check_key(key, old_key=None):
        """
        检查key是否已被占用
        :param key:
        :param old_key:
        :return:
        """
        if old_key:
            count = Config.Q.filter(Config.key != old_key).filter(Config.key == key).count()
        else:
            count = Config.Q.filter(Config.key == key).count()
        if count > 0:
            return True
        return False

    @staticmethod
    def check_title(title, old_key=None):
        """
        检查title是否被占用
        :param title:
        :param old_key:
        :return: boolean
        """
        if old_key:
            count = Config.Q.filter(Config.key!=old_key).filter(Config.title==title).count()
        else:
            count = Config.Q.filter(Config.title == title).count()
        if count > 0:
            return True
        return False

    @staticmethod
    def save_data(title, key, param):
        """
        保存配置信息
        :param title:
        :param key:
        :param param:
        :return:
        """
        if ConfigService.check_title(title):
            raise JsonError('名称已被占用')

        if ConfigService.check_key(key):
            raise JsonError('KEY已被占用')

        obj=Config(**param)
        Config.session.add(obj)
        Config.session.commit()
        # 同时删除对应缓存
        sys_config(key, 'delete_key_value')
        return obj

    @staticmethod
    def update_data(param):
        key = param.get('key', '')
        if ConfigService.check_key(key) is False:
            raise JsonError('不能修改key')
        try:
            Config.Q.filter(Config.key==key).update(param)
        except Exception as e:
            raise e
        else:
            sys_config(key, 'delete_key_value')
        return True
