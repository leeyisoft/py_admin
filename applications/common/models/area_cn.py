#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import MEDIUMINT, TINYINT

from trest.db import Model as Base


class AreaCn(Base):
    __tablename__ = 'area_cn'

    code = Column(MEDIUMINT(6), primary_key=True, server_default=text("'0'"), comment='政区划代码')
    parent_code = Column(MEDIUMINT(6), nullable=False, server_default=text("'0'"), comment='父节点code')
    title = Column(String(64), nullable=False)
    type = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='0 省、直辖市；1 市、市辖区； 2 区、县')
