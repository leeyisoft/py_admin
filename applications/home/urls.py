#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .handlers import index
from .handlers import company

# 其他 URL 通过 acl 获取
urls = [
    # index
    (r"/?(.html)?", index.IndexHandler),

    (r"/article/(\d*)/?(.html)?", company.ArticleDetailHandler),
    (r"/product/(\d*)/?(.html)?", company.ArticleDetailHandler),
    # company
    (r"/company/about/?(.html)?", company.AboutHandler),
    (r"/company/activity/?(.html)?", company.ActivityHandler),
    (r"/company/product/?(.html)?", company.ProductHandler),
    (r"/company/contact/?(.html)?", company.ContactHandler),
    (r"/regulation/?(.html)?", company.RegulationsHandler),

]