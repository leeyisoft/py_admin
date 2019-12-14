#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT

from trest.db import Model as Base


class Message(Base):
    __tablename__ = 'message'

    id = Column(BIGINT(20), primary_key=True, comment='主键')
    msgtype = Column(String(20), comment='消息类型: 后台管理员消息 admin ； 前端贷款用户消息  user')
    message = Column(String(200), server_default=text("''"), comment='附加消息')
    from_user_id = Column(String(32), comment='user or admin_user 用户ID 消息发送者 0表示为系统消息')
    to_user_id = Column(String(32), comment='消息接收者 user ID or admin_user id')
    read_at = Column(BIGINT(13), comment='读消息Unix时间戳毫秒单位')
    status = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='状态:( 0 未读；1 已读, 默认0)')
    created_at = Column(BIGINT(13), nullable=False, server_default=text("'0'"), comment='创建记录Unix时间戳毫秒单位')
