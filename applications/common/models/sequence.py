#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT

from trest.db import Model as Base


class Sequence(Base):
    __tablename__ = 'sequence'

    key = Column(String(40), primary_key=True, server_default=text("''"))
    value = Column(BIGINT(20), nullable=False, server_default=text("'0'"))
