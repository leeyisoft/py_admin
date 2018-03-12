#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .handlers.dashboard import DashboardHandler
from .handlers.passport import LoginHandler
from .handlers.passport import LogoutHandler

# 其他 URL 通过 acl 获取
urls = [
    (r"/admin/?", DashboardHandler),
    (r"/admin/index?", DashboardHandler),
    (r"/admin/dashboard/?", DashboardHandler),
    (r"/admin/login/?(.html)?", LoginHandler),
    (r"/admin/logout/?(.html)?", LogoutHandler),
]