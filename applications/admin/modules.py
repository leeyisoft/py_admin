#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""UI模块

[description]
"""

import tornado.web

class HelloModule(tornado.web.UIModule):
    def render(self):
        return '<h1>Hello, world!</h1>'
class LayuiNavModule(tornado.web.UIModule):
    def render(self, items):
        return self.render_string('modules/layui_nav.html', items=items)

class LayuiNavTreeModule(tornado.web.UIModule):
    def render(self):
        return ''''''

ui_modules = {
    'hello': HelloModule,
    'layui_nav_tree': LayuiNavTreeModule,
}