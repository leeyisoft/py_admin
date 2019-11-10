#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Enum, String, text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT

from trest.db import Model as Base


class UserFriendNotice(Base):
    __tablename__ = 'user_friend_notice'

    id = Column(BIGINT(20), primary_key=True, comment='主键')
    msgtype = Column(Enum('apply_friend', 'system'), comment='消息类型')
    related_id = Column(BIGINT(20), comment='关联业务主键')
    message = Column(String(200), server_default=text(''), comment='附加消息')
    from_user_id = Column(BIGINT(20), comment='User 用户ID 消息发送者 0表示为系统消息')
    to_user_id = Column(BIGINT(20), comment='消息接收者 User 用户ID')
    read_at = Column(BIGINT(13), comment='读消息UTC时间')
    status = Column(TINYINT(1), nullable=False, server_default=text('0'), comment='状态:( 0 未读；1 已读 11 接受 12 拒绝请求)')
    created_at = Column(BIGINT(13), comment='创建记录UTC时间')
