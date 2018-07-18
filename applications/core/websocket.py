#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import functools

from tornado import gen
from tornado import httpclient
from tornado import httputil
from tornado import ioloop
from tornado import websocket


APPLICATION_JSON = 'application/json'

DEFAULT_CONNECT_TIMEOUT = 30
DEFAULT_REQUEST_TIMEOUT = 30


class WebSocketClient(object):
    """Base for web socket clients.
    """

    DISCONNECTED = 0
    CONNECTING = 1
    CONNECTED = 2

    def __init__(self, io_loop=None,
                 connect_timeout=DEFAULT_CONNECT_TIMEOUT,
                 request_timeout=DEFAULT_REQUEST_TIMEOUT):

        self.connect_timeout = connect_timeout
        self.request_timeout = request_timeout
        self._io_loop = io_loop or ioloop.IOLoop.current()
        self._ws_connection = None
        self._connect_status = self.DISCONNECTED

    def connect(self, url):
        """Connect to the server.
        :param str url: server URL.
        """
        self._connect_status = self.CONNECTING
        headers = httputil.HTTPHeaders({'Content-Type': APPLICATION_JSON})
        request = httpclient.HTTPRequest(url=url,
                                         connect_timeout=self.connect_timeout,
                                         request_timeout=self.request_timeout,
                                         headers=headers)
        ws_conn = websocket.WebSocketClientConnection(self._io_loop, request)
        ws_conn.connect_future.add_done_callback(self._connect_callback)

    def send(self, data):
        """Send message to the server
        :param str data: message.
        """

        if self._ws_connection:
            self._ws_connection.write_message(json.dumps(data))

    def close(self, reason=''):
        """Close connection.
        """

        if self._connect_status != self.DISCONNECTED:
            self._connect_status = self.DISCONNECTED
            self._ws_connection and self._ws_connection.close()
            self._ws_connection = None
            self.on_connection_close(reason)

    def _connect_callback(self, future):
        if future.exception() is None:
            self._connect_status = self.CONNECTED
            self._ws_connection = future.result()
            self.on_connection_success()
            self._read_messages()
        else:
            self.close(future.exception())

    def is_connected(self):
        return self._ws_connection is not None

    @gen.coroutine
    def _read_messages(self):
        while True:
            msg = yield self._ws_connection.read_message()
            if msg is None:
                self.close()
                break

            self.on_message(msg)

    def on_message(self, msg):
        """This is called when new message is available from the server.
        :param str msg: server message.
        """

        pass

    def on_connection_success(self):
        """This is called on successful connection ot the server.
        """

        pass

    def on_connection_close(self, reason):
        """This is called when server closed the connection.
        """
        pass
