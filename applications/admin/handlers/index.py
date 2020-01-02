#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL处理器

[description]
"""
from trest.router import get

from .common import CommonHandler


class IndexHandler(CommonHandler):
    @get(['/pyadm/login', '/pyadm/login/'])
    def index_get(self, *args, **kwargs):
        """首页
        """
        params = {}
        self.render('index.html', **params)

