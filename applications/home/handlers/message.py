#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.websocket

from tornado.escape import json_decode

from applications.core.logger.client import SysLogger
from applications.core.utils import Func

from .common import CommonHandler
from ..models import Member
from ..models import MemberFriend
from ..models import Message


class IndexHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        """Home首页
        """
        params = {
            'active': {'index':'layui-this'},
        }
        self.render('message/index.html', **params)
