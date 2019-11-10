#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT

from trest.db import Model as Base


class UserLevel(Base):
    __tablename__ = 'user_level'

    id = Column(BIGINT(20), primary_key=True, comment='主键')
    name = Column(String(80), nullable=False, comment='等级名称')
    min_exper = Column(BIGINT(20), nullable=False, server_default=text('0'), comment='最小经验值')
    max_exper = Column(BIGINT(20), nullable=False, server_default=text('0'), comment='最大经验值')
    intro = Column(String(255), nullable=False, comment='等级简介')
    default = Column(TINYINT(1), nullable=False, server_default=text('0'), comment='默认等级')
    expire = Column(BIGINT(20), nullable=False, server_default=text('0'), comment='会员有效期(天)')
    status = Column(TINYINT(1), nullable=False, server_default=text('1'), comment='状态:( 0 禁用；1 启用, 默认1)')
    created_at = Column(BIGINT(13), comment='创建记录UTC时间')
