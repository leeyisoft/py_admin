#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import unittest

# 把当前目录添加到 sys.path 开头
root_path = os.getcwd()
sys.path.insert(0, os.path.dirname(root_path))

if __name__ == "__main__":
    print('root_path : ', os.path.dirname(root_path))
    try:
        ws_url = 'ws://localhost:6080/chat/websocket/?1&token=test_wsc'
        from websocket import create_connection
        import json
        ws = create_connection(ws_url)

        data = {
            "token": "",
            "type": "dialog",
            "mine": {
                "username": "system",
                "avatar": "",
                "id": "0",
                "mine": True,
                "content": "hello leeyi"
            },
            "to": {
                "id": "1",
                "username": "leeyi",
                "status": "online",
                "sign": "",
                "avatar": "",
                "name": "",
                "type": "friend"
            }
        }
        data = json.dumps(data)
        ws.send(data)##发送消息
        # result = ws.recv()##接收消息
        ws.close()
    except KeyboardInterrupt:
        sys.exit(0)