#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys
from decimal import Decimal

import pytz
import datetime
import time
import dateutil.parser
import hashlib
import hmac
import random
import uuid
import re
import requests

from applications.core.logger import SysLogger
from applications.core.db import mysqldb
from applications.core.utils import utime
from ..settings_manager import settings

from .sendmail import sendmail


"""
常用函数
"""
def sendmail(params):
    return sendmail(params);

def md5(val):
    if type(val)!=bytes:
        val = val.encode('utf-8')
    return hashlib.md5(val).hexdigest()

def uuid32():
    return str(uuid.uuid4()).replace('-','')

def is_email(email):
    regex = r'^[0-9a-zA-Z_\-\.]{0,19}@[0-9a-zA-Z_\-]{1,13}\.[a-zA-Z\.]{1,7}$'
    return True if re.match(regex, email) else False

def is_mobile(mobile, region):
    code_map = {
        'CN': ("中国","^(\\+?0?86\\-?)?1[345789]\\d{9}$"),
        'TW': ("台湾","^(\\+?886\\-?|0)?9\\d{8}$"),
        'HK': ("香港","^(\\+?852\\-?)?[569]\\d{3}\\-?\\d{4}$"),
        'MS': ("马来西亚","^(\\+?6?01){1}(([145]{1}(\\-|\\s)?\\d{7,8})|([236789]{1}(\\s|\\-)?\\d{7}))$"),
        'PH': ("菲律宾","^(\\+?0?63\\-?)?\\d{10}$"),
        'TH': ("泰国","^(\\+?0?66\\-?)?\\d{10}$"),
        'SG': ("新加坡","^(\\+?0?65\\-?)?\\d{10}$"),
        'DZ': ("阿尔及利亚", "^(\\+?213|0)(5|6|7)\\d{8}$"),
        'SY': ("叙利亚","^(!?(\\+?963)|0)?9\\d{8}$"),
        'SA': ("沙特阿拉伯","^(!?(\\+?966)|0)?5\\d{8}$"),
        'US': ("美国","^(\\+?1)?[2-9]\\d{2}[2-9](?!11)\\d{6}$"),
        'CZ': ("捷克共和国","^(\\+?420)? ?[1-9][0-9]{2} ?[0-9]{3} ?[0-9]{3}$"),
        'DE': ("德国","^(\\+?49[ \\.\\-])?([\\(]{1}[0-9]{1,6}[\\)])?([0-9 \\.\\-\\/]{3,20})((x|ext|extension)[ ]?[0-9]{1,4})?$"),
        'DK': ("丹麦","^(\\+?45)?(\\d{8})$"),
        'GR': ("希腊","^(\\+?30)?(69\\d{8})$"),
        'AU': ("澳大利亚","^(\\+?61|0)4\\d{8}$"),
        'GB': ("英国","^(\\+?44|0)7\\d{9}$"),
        'CA': ("加拿大","^(\\+?1)?[2-9]\\d{2}[2-9](?!11)\\d{6}$"),
        'IN': ("印度","^(\\+?91|0)?[789]\\d{9}$"),
        'NZ': ("新西兰","^(\\+?64|0)2\\d{7,9}$"),
        'ZA': ("南非","^(\\+?27|0)\\d{9}$"),
        'ZM': ("赞比亚","^(\\+?26)?09[567]\\d{7}$"),
        'ES': ("西班牙","^(\\+?34)?(6\\d{1}|7[1234])\\d{7}$"),
        'FI': ("芬兰","^(\\+?358|0)\\s?(4(0|1|2|4|5)?|50)\\s?(\\d\\s?){4,8}\\d$"),
        'FR': ("法国","^(\\+?33|0)[67]\\d{8}$"),
        'IL': ("以色列","^(\\+972|0)([23489]|5[0248]|77)[1-9]\\d{6}"),
        'HU': ("匈牙利","^(\\+?36)(20|30|70)\\d{7}$"),
        'IT': ("意大利","^(\\+?39)?\\s?3\\d{2} ?\\d{6,7}$"),
        'JP': ("日本","^(\\+?81|0)\\d{1,4}[ \\-]?\\d{1,4}[ \\-]?\\d{4}$"),
        'NO': ("挪威","^(\\+?47)?[49]\\d{7}$"),
        'BE': ("比利时","^(\\+?32|0)4?\\d{8}$"),
        'PL': ("波兰","^(\\+?48)? ?[5-8]\\d ?\\d{3} ?\\d{2} ?\\d{2}$"),
        'BR': ("巴西","^(\\+?55|0)\\-?[1-9]{2}\\-?[2-9]{1}\\d{3,4}\\-?\\d{4}$"),
        'PT': ("葡萄牙","^(\\+?351)?9[1236]\\d{7}$"),
        'RU': ("俄罗斯","^(\\+?7|8)?9\\d{9}$"),
        'RS': ("塞尔维亚","^(\\+3816|06)[- \\d]{5,9}$"),
        'R': ("土耳其","^(\\+?90|0)?5\\d{9}$"),
        'VN': ("越南","^(\\+?84|0)?((1(2([0-9])|6([2-9])|88|99))|(9((?!5)[0-9])))([0-9]{7})$"),
    }
    #正则匹配电话号码
    # mobile = "13692177708"
    (coutry, regex) = code_map.get(region.upper(), ('', '.*'))
    if regex=='.*':
        raise Exception(1, '不支持的区域')
    match = re.match(regex, mobile)
    return True if match else False

def region_mobile(mobile, region):
    """
    区域手机号码验证
    """
    if '-' not in mobile:
        if region.lower() in settings.region_code:
            mobile = "%s-%s" % (settings.region_code[region.lower()]['number'], mobile)
        else:
            return False
    if is_mobile(mobile, region):
        return mobile
    return False

def is_phone(phone, region='CN'):
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

def is_phone_or_mobile(phone, region='CN'):
    return func.is_mobile(phone, region) or func.is_phone(phone, region)

def if_json(str):
    """
    判断传入参数是否为json，如json返回dict对象，否则返回false
    :param str:
    :return:
    """
    try:
        return json.loads(str)
    except Exception:
        return False

def validate_bankcard(bankcard_no):
    """
    阿里接口 验证银行卡
    :param bankcard_no:
    :return:{"cardType":"DC","bank":"CCB","key":"6217002920108203330","messages":[],"validated":true,"stat":"ok"}
    """
    url = 'https://ccdcapi.alipay.com/validateAndCacheCardInfo.json?' \
          '_input_charset=utf-8&cardNo=%s&cardBinCheck=true' % (bankcard_no)
    res = requests.get(url)
    return json.loads(res.text)

def filter_lang(lang):
    """
    客户端语言转换为与数据库中一致
    :param lang:
    :return:
    """
    if lang in ['en', 'us', 'en_US', 'en-US']:
        return 'en'
    elif lang in ['cn', 'zh_CN', 'zh-CN', 'zh-Hans-CN']:
        return 'cn'
    elif lang in ['ph', 'en_PH', 'en-PH']:
        return 'en'
    elif lang in ['id', 'id_ID', 'id-ID']:
        return 'id'
    elif lang in ['vi', 'vi_VN', 'vi-VN']:
        return 'vi'
    elif lang in ['tw', 'zh_TW', 'zh-TW']:
        return 'tw'
    else:
        return 'en'

def increment(key, inc = 1):
    db = mysqldb()
    result = db.execute('select nextval(\'%s\', %s)' % (key, inc)).scalar()
    db.commit()
    return result

def sha256_sign(val):
    """
    SHA256签名
    """
    try:
        m = hashlib.sha256()
        m.update(val.encode('utf-8'))
        return m.hexdigest()
    except Exception as e:
        raise e
    return ''

def sha256_verify_sign(sign, val):
    SysLogger.debug('sha256_sign(val): ' + sha256_sign(val))
    return True if sha256_sign(val)==sign else False


def option_change(options):
    """
    选项字典转数组
    :param options:
    :return:
    """
    list = []
    for key in options:
        item = {}
        item['key'] = key
        item['value'] = key
        item['label'] = options[key]
        list.append(item)
    return list

def as_dict(val_dict):
    """
    连接查询数据转字段
    :param val_dict:
    :return:
    """
    for key in list(val_dict.keys()):
        if key.endswith('_at'):
            val_dict['dt_%s' % key] = utime.ts_to_str(int(val_dict[key]), to_tz=None) if val_dict[key] else ''
        datetime_tuple = (datetime.datetime, datetime.date)
        if isinstance(val_dict[key], datetime_tuple):
            val_dict[key] = str(val_dict[key])
        elif isinstance(val_dict[key], Decimal):
            val_dict[key] = str(val_dict[key])
    return val_dict
