#!/usr/bin/env python
# -*- coding: utf-8 -*-
from trest.exception import JsonError
from applications.common.models.base import ClientVsn
from applications.common.models.base import ApiVsn


class ApiVsnService:
    @staticmethod
    def pubkeyser(apivsn):
        pubkeyser = ApiVsn.session.query(ApiVsn.pubkeyser).filter(ApiVsn.master_vsn==apivsn).scalar()
        return pubkeyser

    @staticmethod
    def prikeyser(apivsn):
        prikeyser = ApiVsn.session.query(ApiVsn.prikeyser).filter(ApiVsn.master_vsn==apivsn).scalar()
        return prikeyser

class ClientVsnService:
    @staticmethod
    def pubkey(client, vsn):
        pubkey = ClientVsn.session.query(ClientVsn.pubkeycli).filter(ClientVsn.vsn==vsn, ClientVsn.client==client).scalar()
        return pubkey

    @staticmethod
    def signkey(client, vsn):
        signkey = ClientVsn.session.query(ClientVsn.signkey).filter(ClientVsn.vsn==vsn, ClientVsn.client==client).scalar()
        return signkey

    @staticmethod
    def get_latest_version(client):
        """
        获取最新版本号
        :param client:
        :return:
        """
        status = 1  # 启用
        version = ClientVsn.session.query(ClientVsn.vsn).filter(ClientVsn.client == client,ClientVsn.status == status) \
            .order_by(ClientVsn.id.desc()).scalar()
        return version
