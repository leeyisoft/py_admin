#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.websocket

from tornado.escape import json_decode

from applications.core.logger.client import SysLogger
from applications.core.utils import Func

from .common import CommonHandler
from ..models import Member
from ..models import MemberFriend
from ..models import MemberFriendNotice


class FindHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        user_id = self.current_user.get('id')
        find_type = self.get_argument('type', None)
        value = self.get_argument('value', None)
        limit = self.get_argument('limit', 12)
        page = self.get_argument('page', 1)
        if find_type=='friend' or find_type=='recommend':
            return self._find_friend(value, page, limit)
        else:
            params = {
            }
            self.render('friend/find.html', **params)

    def _find_friend(self, value, page, limit):
        # print("value: ", type(value), value)
        user_id = self.current_user.get('id')
        query = Member.Q
        if value:
            if Func.is_mobile(value):
                query = query.filter(Member.mobile==value)
            elif Func.is_email(value):
                query = query.filter(Member.email==value)
            else:
                query = query.filter(Member.username.like('%' +value+ '%'))

        pagelist_obj = query.filter(Member.status==1).paginate(page=page, per_page=limit)
        total = pagelist_obj.total
        page = pagelist_obj.page
        items = pagelist_obj.items

        user_list = []
        if items:
            for row in items:
                item = row.as_dict(['id', 'username', 'avatar', 'sign'])
                item['avatar'] = self.static_url(item['avatar'])
                user_list.append(item)
        return self.success(data=user_list, total=total, limit=limit, page=page)


class ApplyAddFriendHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        user_id = self.current_user.get('id')
        to_user_id = self.get_argument('to_user_id', None)
        group_id = self.get_argument('group_id', None)
        remark = self.get_argument('remark', None)

        query = MemberFriend.Q.filter(MemberFriend.from_user_id==user_id)
        friend = query.first()
        params = {
            'from_user_id': user_id,
            'to_user_id': to_user_id,
            'group_id': group_id,
            'remark': remark,
            'status': 0,
        }
        if friend is None:
            friend = MemberFriend(**params)
            MemberFriend.session.add(friend)
        elif friend.status==1:
            return self.success()
        elif friend.status==2:
            return self.error('拒绝请求')
        # end if
        MemberFriend.Q.filter(MemberFriend.id==friend.id).update(params)

        # for notice
        query = MemberFriendNotice.Q.filter(MemberFriendNotice.status==0)
        query = query.filter(MemberFriendNotice.related_id==friend.id)
        notice = query.first()
        params2 = {
            'msgtype': 'apply_friend',
            'related_id': friend.id,
            'message': remark,
            'from_user_id': user_id,
            'to_user_id': to_user_id,
            'status': 0,
        }
        if notice is None:
            notice = MemberFriendNotice(**params2)
            MemberFriendNotice.session.add(notice)
        else:
            MemberFriendNotice.Q.filter(MemberFriendNotice.id==notice.id).update(params2)

        MemberFriend.session.commit()
        return self.success()


class AddFriendHandler(CommonHandler):
    """docstring for Passport"""
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        user_id = self.current_user.get('id')
        friend_id = self.get_argument('friend_id', None)
        group_id = self.get_argument('group_id', '0')
        action = self.get_argument('action', None)
        # return self.success()
        if action not in ['agree', 'refuse']:
            return self.error('error action')

        query = MemberFriend.Q.filter(MemberFriend.id==friend_id)
        friend = query.first()
        if friend is None:
            return self.error('不存在的添加好友申请')
        elif friend.status==1:
            return self.success()
        elif friend.status==2:
            return self.error('拒绝请求')
        # end if
        status = 1 if action=='agree' else 2
        params = {
            'id': friend_id,
            'utc_updated_at': Func.utc_now(),
            'status': status,
        }
        MemberFriend.Q.filter(MemberFriend.id==friend_id).update(params)

        if action=='agree':
            query = MemberFriend.Q
            query = query.filter(MemberFriend.from_user_id==friend.to_user_id)
            query = query.filter(MemberFriend.to_user_id==friend.from_user_id)
            to_friend = query.first()
            if to_friend:
                params = {
                    'group_id': group_id,
                    'remark': '',
                    'status': status,
                }
                MemberFriend.Q.filter(MemberFriend.id==to_friend.id).update(params)
            else:
                params = {
                    'from_user_id': friend.to_user_id,
                    'to_user_id': friend.from_user_id,
                    'group_id': group_id,
                    'remark': '',
                    'status': status,
                }
                to_friend = MemberFriend(**params)
                MemberFriend.session.add(to_friend)
            # end if 2
        # end if

        # for notice
        status2 = '1%d' % (status)
        query = MemberFriendNotice.Q.filter(MemberFriendNotice.msgtype=='apply_friend')
        query = query.filter(MemberFriendNotice.related_id==friend_id)
        notice = query.first()
        if notice is not None:
            params2 = {
                'status': status2,
            }
            MemberFriendNotice.Q.filter(MemberFriendNotice.id==notice.id).update(params2)

            params3 = {
                'msgtype': 'system',
                'related_id': friend_id,
                'message': 'remark',
                'from_user_id': friend.to_user_id,
                'to_user_id': friend.from_user_id,
                'status': 0,
            }
            notice = MemberFriendNotice(**params3)
            MemberFriendNotice.session.add(notice)
        MemberFriend.session.commit()
        return self.success()
