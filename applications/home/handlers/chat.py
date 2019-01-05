#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.websocket

from tornado.escape import json_decode

from sqlalchemy import desc

from applications.core.settings_manager import settings
from applications.core.logger.client import SysLogger
from applications.core.utils import Func
from applications.core.cache import cache

from .common import CommonHandler
from ..models import Member
from ..models import MemberFriend
from ..models import MemberFriendNotice
from ..models import Online


class ChartRoomHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        params = {
            'limit': 20,
            'token': self.current_user.get('id'),
        }
        self.render('chat/room.html', **params)


class ChartInitHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        user_id = self.current_user.get('id')
        mine = Member.Q.filter(Member.id==user_id).first()
        friend = MemberFriend.friends_by_group(user_id, static_url=self.static_url)
        # print('friend: ', type(friend), friend)
        data = {
            'mine': {
                'id': mine.id,
                'username': mine.username,
                # 'status': Online.get_online(mine.id),
                'status': 1,
                'sign': mine.sign,
                'avatar': self.static_url(mine.avatar),
            },
            'friend': friend,
        }
        return self.success(data=data)


class ChartMsgboxHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        user_id = self.current_user.get('id')

        params = {
        }
        self.render('chat/msgbox.html', **params)


class ChartNoticeHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        # return self.error('333aaa')
        user_id = self.current_user.get('id')
        data = []
        query = MemberFriendNotice.Q.filter(MemberFriendNotice.status==0)
        query = query.filter(MemberFriendNotice.msgtype!=None)
        query = query.filter(MemberFriendNotice.to_user_id==user_id)
        query = query.filter(MemberFriendNotice.to_user_id==user_id)
        query = query.order_by(desc(MemberFriendNotice.utc_created_at))
        msg_li = query.all()
        # print(query.statement)
        data = []
        for msg in msg_li:
            from_user = Member.get_info(msg.from_user_id)
            from_user['avatar'] = self.static_url(from_user['avatar']);
            item = {
                'id': msg.id,
                'msgtype': msg.msgtype,
                'related_id': msg.related_id,
                'message': msg.message,
                'from_user': from_user,
                'status': msg.status,
                'created_at': str(msg.created_at),
                'read_at': str(msg.read_at) if msg.read_at else '',
            }
            data.append(item)

        tplfile= '%s/common/tpl/add_friend.tpl' % self.get_template_path()
        tpl = ''
        with open(tplfile) as openfile:
            tpl = openfile.read()
        params = {
            'tpl': tpl,
            'data': data,
            'pages': 1,
            'curr_user_id': user_id,
        }
        return self.success(**params)


class ChatServerHandler(tornado.websocket.WebSocketHandler):
    current_user_id = ''
    waiters = {}
    cache = []
    cache_size = 200

    def __init__(self, application, request, **kwargs):
        super(ChatServerHandler, self).__init__(application, request, **kwargs)
        self.current_user = self.get_current_user()
        if self.current_user is None:
            self.current_user = {}

        self.current_user_id = int(self.current_user.get('id', 0))

    def get_current_user(self):
        cache_key = self.get_secure_cookie(settings.front_session_key)
        if cache_key is None:
            return None
        try:
            cache_key = str(cache_key, encoding='utf-8')
            # print('cache_key: ', cache_key)
            user = cache.get(cache_key)
            # print('user: ', type(user), user)
            if user:
                return user
            member_id = cache_key[len(settings.member_cache_prefix):]
            # print('member_id: ', member_id)
            member = Member.Q.filter(Member.id==member_id).first()
            if member is None:
                return None
            self.set_curent_user(member)
            user = cache.get(cache_key)
            # print('user: ', type(user), user)
            return user
        except Exception as e:
            raise e


    def set_curent_user(self, member):
        cache_key = member.cache_info(self)
        self.set_secure_cookie(settings.front_session_key, cache_key, expires_days=1)


    def _change_state_notify(self, state):
        """
        当前用户状态改变，通知在线好友
        Arguments:
            state {string} -- [hide|online|offline]
        """
        curr_username = self.current_user.get('username', '')
        # 设置用户状态
        Online.set_online(self.current_user_id, state)
        for friend in MemberFriend.online_list(self.current_user_id):
            msg_dict = {
                'type': 'online',
                # token nouse
                'token': 'curr_token',
                'uid': self.current_user_id,
                'status': state,
            }
            waiter = self.waiters.get(friend.get('id', ''), None)
            if waiter:
                waiter.write_message(msg_dict)


    def open(self, *args, **kwargs):
        # SysLogger.debug('self.current_user_id %s' % (str(self.current_user_id)))
        self.waiters[self.current_user_id] = self
        self._change_state_notify('online')


    def on_close(self, *args, **kwargs):
        self.waiters.pop(self.current_user_id, None)
        self._change_state_notify('offline')

    def on_message(self, message):
        """
        message 是如下格式的字符串
        {
            "token": "",
            "type": "dialog",
            "mine": {
                "username": "",
                "avatar": "",
                "id": "",
                "mine": True,
                "content": ""
            },
            "to": {
                "id": "",
                "username": "",
                "status": "online",
                "sign": "",
                "avatar": "",
                "name": "",
                "type": "friend"
            }
        }
        """
        try:
            message = message.replace('\'', '"')
            SysLogger.debug('%s : %s' % ('chat on message ', message))
            print('chat on message ', message)
            data = json_decode(message)
        except ValueError:
            SysLogger.debug("ws message isn't json text, message is: %s", message)
            return

        chat_type = data.get('type', 'dialog')
        SysLogger.debug('chat_type: %s' % chat_type)
        # curr_id = data.get('mine').get('id')

        if chat_type=='dialog':
            # 两人聊天
            old_uid = data.get('to').get('id')
            new_to = data.get('mine')
            # 消息的发送者id（比如群组中的某个消息发送者），可用于自动解决浏览器多窗口时的一些问题
            new_to['fromid'] = new_to.get('id')
            # 没有type=friend ，同一对话，会有两个对话框
            new_to['type'] = data.get('to').get('type')
            # 删除 mine 使得消息显示在左边
            del new_to['mine']

            msg_dict = {
                'type': chat_type,
                'to': new_to,
            }
            # SysLogger.info("msg_dict %s ", msg_dict)
            waiter = self.waiters.get(int(old_uid), None)
            # print('waiter', type(waiter), waiter, msg_dict)
            SysLogger.debug('waiter: %s %s %s' % (old_uid, type(waiter), waiter))
            if waiter:
                waiter.write_message(msg_dict)
            return

        elif chat_type=='forum':
            # 聊天组 opponent_uid 应该是一个 列表 '[a,b,c]' 字符串
            pass
        elif chat_type=='apply_friend':
            print(message)
            pass
        else:
            SysLogger.debug('invalid ws path=%s', message['path'])
            return

    def check_origin(self, origin):
        # 允许跨域访问
        return True


class WebRtcRoomHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        user_id = self.current_user.get('id')
        member = Member.Q.filter(Member.id==user_id).first()
        fields = ['id', 'username', 'avatar', 'sign']
        curr_user = member.as_dict(fields)
        items = Member.Q.filter(Member.status==1).all()
        user_list = []
        if items:
            for row in items:
                user_list.append(row.as_dict(['id', 'username', 'avatar', 'sign']))
        params = {
            'def_avator': self.static_url('image/default_avatar.jpg'),
            'timestamp': Func.unix_time(),
            # 'opponent_uid': opponent_uid,
            'limit': 20,
            'curr_user': curr_user,
            'user_list': user_list,
            'token': user_id,
        }
        self.render('chat/webrtc.html', **params)


class WebRTCServerHandler(tornado.websocket.WebSocketHandler):
    # 用户集合
    users = set()

    def open(self):
        # 连接建立时往房间添加用户
        self.users.add(self)

    def on_message(self, message):
        # 接收到消息时进行广播，除了自己
        for user in self.users:
            if user != self:
                user.write_message(message)

    def on_close(self):
        # 链接断开时移除用户
        self.users.remove(self)

    def check_origin(self, origin):
        # 允许跨域访问
        return True
