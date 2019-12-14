#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT

from trest.db import Model as Base


class UserLoginLog(Base):
    __tablename__ = 'user_login_log'

    id = Column(BIGINT(20), primary_key=True, comment='主键')
    user_id = Column(BIGINT(20), nullable=False, server_default=text("'0'"), comment='用户唯一标识')
    ip = Column(String(40), comment='登录IP')
    client = Column(String(20), comment='客户端：web wechat android ios ')
    created_at = Column(BIGINT(13), comment='创建记录UTC时间')
