#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Enum, String
from sqlalchemy.dialects.mysql import BIGINT

from trest.db import Model as Base


class UserBinding(Base):
    __tablename__ = 'user_binding'

    id = Column(BIGINT(20), primary_key=True, comment='主键')
    user_id = Column(BIGINT(20), comment='用户ID')
    type = Column(Enum('QQ', 'WECHAT', 'MOBILE', 'EMAIL', 'ALIPAY'), comment='绑定类型')
    openid = Column(String(80), comment='第三方平台openid')
