#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .handlers import passport
from .handlers import dashboard
from .handlers import user
from .handlers import role
from .handlers import menu
from .handlers import config
from .handlers import advertise
from .handlers import advertise_cat
from .handlers import user_sms_code
from .handlers import company
from .handlers import blacklist


# 其他 URL 通过 acl 获取
urls = [
    # passport
    (r"/admin/login/?(.html)?", passport.LoginHandler),
    (r"/admin/logout/?(.html)?", passport.LogoutHandler),
    (r"/admin/captcha/?(.png)?", passport.CaptchaHandler),

    # dashboard
    (r"/admin/?(.html)?", dashboard.MainHandler),
    (r"/admin/index/?(.html)?", dashboard.MainHandler),
    (r"/admin/main/?(.html)?", dashboard.MainHandler),
    (r"/admin/welcome/?(.html)?", dashboard.WelcomeHandler),

    dashboard.MainHandler,
    config.ConfigHandler,
    menu.MenuHandler,
    user.UserHandler,
    role.RoleHandler,
    advertise.AdvertiseHandler,
    advertise_cat.AdvertiseCatHandler,
    user_sms_code.UserSmsCodeHandler,
    company.IndexHandler,
    blacklist.IndexHandler,
]
