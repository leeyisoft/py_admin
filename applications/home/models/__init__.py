#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .member import MemberCertification
from .member import MemberOperationLog
from .member import MemberLoginLog
from .member import Member
from .member import MemberFriend
from .member import Friendgroup
from .member import MemberFriendNotice
from .member import Online

from applications.core.models import Message

class PeriodicCallbackDemo(object):
    @staticmethod
    def demo_test(user_id):
        pass
