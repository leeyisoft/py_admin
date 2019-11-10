#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Enum, String, text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT

from trest.db import Model as Base


class Company(Base):
    __tablename__ = 'company'

    id = Column(BIGINT(20), primary_key=True)
    company_name = Column(String(50), nullable=False, server_default=text(''), comment='公司名')
    description = Column(String(100), nullable=False, server_default=text(''), comment='公司简介')
    type = Column(Enum('outer', 'inner'), comment='类型：（outer外部委派；inner内部）')
    module = Column(Enum('review', 'collection', 'manage', 'service'), comment='业务：（review 审批；collection 催收；manage管理；service客服）')
    status = Column(TINYINT(1), nullable=False, server_default=text('1'), comment='状态:( 0 禁用；1 启用； 删除 -1)')
    created_at = Column(BIGINT(13), comment='创建Unix时间戳毫秒单位')
