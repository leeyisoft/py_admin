#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .handlers import index
from .handlers import passport
from .handlers import member
from .handlers import chat
from .handlers import company

# 其他 URL 通过 acl 获取
urls = [
    # index
    (r"/?(.html)?", index.IndexHandler),

    # passport
    (r"/passport/login/?(.html)?", passport.LoginHandler),
    (r"/passport/logout/?(.html)?", passport.LogoutHandler),
    (r"/passport/reg/?(.html)?", passport.RegisterHandler),
    (r"/passport/forget/?(.html)?", passport.ForgetHandler),
    (r"/passport/captcha/?(.png)?", passport.CaptchaHandler),

    # memeber
    (r"/member/?(.html)?", member.IndexHandler),
    (r"/member/index/?(.html)?", member.IndexHandler),
    (r"/member/set/?(.html)?", member.SetHandler),
    (r"/member/sendmail/?(.html)?", member.SendmailHandler),
    (r"/member/activate/?(.html)?", member.ActivateHandler),
    (r"/member/repass/?(.html)?", member.ResetPasswordHandler),
    (r"/member/upload/?(.html)?", member.UploadHandler),
    (r"/member/message/?(.html)?", member.MessageHandler),
    (r"/member/invite/?(.html)?", member.InviteHandler),
    (r"/member/home/?(.html)?", member.HomeHandler),
    (r"/member/unlocked/?(.html)?", member.MemberUnlockedHandler),

    # chat
    (r"/chat/websocket/?(.html)?", chat.ChatServerHandler),
    (r"/chat/room/?(.html)?", chat.ChartRoomHandler),
    (r"/chat/init/?(.html)?", chat.ChartInitHandler),
    (r"/chat/msgbox/?(.html)?", chat.ChartMsgboxHandler),
    (r"/chat/notice/?(.html)?", chat.ChartNoticeHandler),

    # company
    (r"/company/about/?(.html)?", company.AboutHandler),
    (r"/company/activity/?(.html)?", company.ActivityHandler),
    (r"/company/product/?(.html)?", company.ProductHandler),
    (r"/company/contact/?(.html)?", company.ContactHandler),
    (r"/regulations/?(.html)?", company.RegulationsHandler),

]