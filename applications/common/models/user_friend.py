#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT

from trest.db import Model as Base


class UserFriend(Base):
    __tablename__ = 'user_friend'

    id = Column(BIGINT(20), primary_key=True, comment='主键')
    from_user_id = Column(BIGINT(20), nullable=False, comment='发起人')
    to_user_id = Column(BIGINT(20), nullable=False, comment='接受人')
    group_id = Column(BIGINT(20), server_default=text("'0'"), comment='用户分组ID friendgroup主键')
    status = Column(String(16), nullable=False, server_default=text("'0'"), comment='状态 0 请求中 1 接受 2 拒绝请求')
    updated_at = Column(BIGINT(13), comment='记录更新时间')
    created_at = Column(BIGINT(13), nullable=False, comment='创建记录UTC时间')
    remark = Column(String(200), nullable=False, server_default=text("''"), comment='申请好友的验证消息')
