#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from tornado.options import define

from applications.core.webserver import run


if __name__ == "__main__":
    # 把当前目录添加到 sys.path 开头
    root_path = os.getcwd()
    sys.path.insert(0, root_path)

    template_path = os.path.join(root_path, "applications/admin/templates")
    define('template_path', default=template_path, help='run on the given template_path', type=str)

    try:
        run()
    except KeyboardInterrupt:
        sys.exit(0)
