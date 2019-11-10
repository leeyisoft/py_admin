#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import CHAR, Column, Enum, String, text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT

from trest.db import Model as Base


class User(Base):
    __tablename__ = 'user'

    id = Column(BIGINT(20), primary_key=True, comment='主键')
    level_id = Column(BIGINT(20), nullable=False, server_default=text('0'), comment='会员等级ID')
    password = Column(String(128), nullable=False)
    username = Column(String(40), comment='登录名、昵称')
    mobile = Column(String(11))
    email = Column(String(80))
    experience = Column(BIGINT(20), nullable=False, server_default=text('0'), comment='经验值')
    sex = Column(Enum('hide', 'male', 'female', 'other'), nullable=False, server_default=text('hide'), comment='性别(男 male ，女 female 隐藏 hide)')
    avatar = Column(String(255), nullable=False, server_default=text(''), comment='头像')
    sign = Column(String(255), server_default=text(''), comment='会员签名')
    login_count = Column(BIGINT(20), nullable=False, server_default=text('0'), comment='登陆次数')
    last_login_ip = Column(String(40), nullable=False, server_default=text(''), comment='最后登陆IP')
    last_login_at = Column(BIGINT(13), comment='最后登录UTC时间')
    ref_user_id = Column(CHAR(32), comment='推荐人ID，空字符串表示为推荐人')
    status = Column(TINYINT(1), nullable=False, server_default=text('1'), comment='状态:( 0 禁用；1 启用, 默认1)')
    deleted = Column(TINYINT(1), nullable=False, server_default=text('0'), comment='已删除的 1 是 0 否 默认 0')
    created_at = Column(BIGINT(13), comment='创建记录UTC时间')
    reg_ip = Column(String(40), comment='注册IP')
    reg_client = Column(String(20), comment='客户端：web wechat android ios mobile')
