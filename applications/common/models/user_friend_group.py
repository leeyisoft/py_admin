#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT

from trest.db import Model as Base


class UserFriendGroup(Base):
    __tablename__ = 'user_friend_group'

    id = Column(BIGINT(20), primary_key=True, comment='主键')
    name = Column(String(40), nullable=False, server_default=text("''"), comment='分组名称')
    created_at = Column(BIGINT(13), nullable=False, comment='创建记录UTC时间')
    owner_user_id = Column(BIGINT(20), nullable=False, server_default=text("'0'"), comment='分组所属用户ID')
