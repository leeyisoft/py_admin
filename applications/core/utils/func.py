#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pytz
import datetime
import time
import dateutil.parser
import hashlib
import hmac
import random
import uuid
import re

from ..settings_manager import settings

from .sendmail import sendmail
from .string import String

"""
常用函数
"""
class Func():
    @staticmethod
    def sendmail(params):
        return sendmail(params);

    @staticmethod
    def md5(val):
        if type(val)!=bytes:
            val = val.encode('utf-8')
        return hashlib.md5(val).hexdigest()

    @staticmethod
    def uuid32():
        return str(uuid.uuid4()).replace('-','')

    @staticmethod
    def pbkdf2(password, salt, iterations, dklen=0, digest=None):
        """Return the hash of password using pbkdf2."""
        if digest is None:
            digest = hashlib.sha256
        if not dklen:
            dklen = None
        password = String.force_bytes(password)
        salt = String.force_bytes(salt)
        return hashlib.pbkdf2_hmac(digest().name, password, salt, iterations, dklen)

    @staticmethod
    def is_email(email):
        regex = r'^[0-9a-zA-Z_\-\.]{0,19}@[0-9a-zA-Z_\-]{1,13}\.[a-zA-Z\.]{1,7}$'
        return True if re.match(regex, email) else False

    @staticmethod
    def is_mobile(mobile):
        regex = r'^1[0-9]{10}$'
        return True if re.match(regex, mobile) else False

    @staticmethod
    def is_phone(phone):
        """
        #写一个正则表达式，能匹配出多种格式的电话号码，包括
        #(021)88776543   010-55667890 02584453362  0571 66345673
        #\(?0\d{2,3}[) -]?\d{7,8}
        # import re
        # phone="(021)88776543 010-55667890 02584533622 057184720483 837922740"
        """
        m = re.findall(r"\(?0\d{2,3}[) -]?\d{7,8}",phone)
        if m:
            return True
        else:
            return False

    @staticmethod
    def is_phone_or_mobile(phone):
        return Func.is_mobile(phone) or Func.is_phone(phone)

    @staticmethod
    def unix_time():
        return int(time.mktime(datetime.datetime.now().timetuple()))

    @staticmethod
    def local_now():
        """获取附带tzinfo的当前时间
        Returns:
            datetime.datetime -- 例如 datetime.datetime(2018, 5, 8, 11, 50, 50, 627882, tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>)
        """
        tz = pytz.timezone(settings.TIME_ZONE)
        return datetime.datetime.now(tz)

    @staticmethod
    def utc_now():
        """获取当前UTC时间
        Returns:
            datetime.datetime -- 例如 datetime.datetime(2018, 5, 8, 3, 50, 50, 356945, tzinfo=<UTC>)
        """
        tz = pytz.timezone('UTC')
        return datetime.datetime.now(tz)

    @staticmethod
    def str_to_datetime(str_dt, to_tz='UTC'):
        """字符串格式的时间转换为datetime格式的时间

        [description]

        Arguments:
            str_dt {str} -- 字符串格式的时间， 例如 2018-02-27 02:13:02.087558+08:00 or 2018-02-27

        Keyword Arguments:
            to_tz {str} -- [description] (default: {'UTC'})

        Returns:
            [datetime.datetime] -- [description]
        """

        tz = pytz.timezone(to_tz)
        dt = dateutil.parser.parse(str_dt)
        return dt.astimezone(tz)

    @staticmethod
    def dt_to_timezone(dt, to_tz=None):
        """[summary]
        把datetime时间转换成特定时间的时间
        Arguments:
            dt {datetime.datetime} -- 时间 例如 2018-02-27 02:13:02.087558+08:00
        Keyword Arguments:
            to_tz {str} -- 指定的时区 (default: {None})
        Returns:
            datetime.datetime -- 指定时区的时间 例如 2018-02-27 10:13:02.087558+08:00
        """
        if not isinstance(dt, datetime.datetime):
            return dt
        to_tz = to_tz if to_tz else settings.TIME_ZONE
        tz = pytz.timezone(to_tz)
        dt = dt.replace(tzinfo=pytz.utc)
        return dt.astimezone(tz)

    @staticmethod
    def dateformat(value, format="%Y-%m"):
        if type(value)==str:
            value = Func.str_to_datetime(value)
        return value.strftime(format)

    @staticmethod
    def function():
        pass

