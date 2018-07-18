#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

import unittest

from applications.core.websocket import WebSocketClient


# 把当前目录添加到 sys.path 开头
root_path = os.getcwd()
sys.path.insert(0, os.path.dirname(root_path))


if __name__ == "__main__":
    print('root_path : ', os.path.dirname(root_path))
    try:
        io_loop = ioloop.IOLoop.instance()

        client = WebSocketClient(io_loop)
        ws_url = 'ws://127.0.0.1:5080/chat/websocket/'
        # ws_url = 'ws://echo.websocket.org'
        client.connect(ws_url, auto_reconnet=True, reconnet_interval=10)
        data = {

        }
        client.send(data)
    except KeyboardInterrupt:
        sys.exit(0)