#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT

from trest.db import Model as Base


class UserCertification(Base):
    __tablename__ = 'user_certification'

    user_id = Column(BIGINT(20), primary_key=True, server_default=text('0'), comment='主键，user表 id')
    realname = Column(String(40), nullable=False, server_default=text(''), comment='登录名、昵称')
    idcardno = Column(String(40), nullable=False, server_default=text(''), comment='身份证号码')
    idcard_img = Column(String(200), nullable=False, server_default=text(''), comment='手持身份证照片一张（要求头像清晰，身份证号码清晰）')
    authorized = Column(TINYINT(1), nullable=False, server_default=text('0'), comment='认证状态:( 0 待审核；1 审核通过, 2 审核失败)')
    client = Column(String(20), comment='客户端：web wechat android ios mobile')
    ip = Column(String(40), comment='添加记录的IP地址')
    updated_at = Column(BIGINT(13), comment='更新记录UTC时间')
    created_at = Column(BIGINT(13), comment='创建记录UTC时间')
    status = Column(TINYINT(1), nullable=False, server_default=text('1'), comment='状态:( 0 禁用；1 启用, 默认1)')
    remark = Column(String(200), comment='备注；如果审核不通过，填写原因')
    authorized_user_id = Column(BIGINT(20), comment='审核管理员ID，user 表 uuid')
