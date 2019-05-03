#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.types import DECIMAL
from sqlalchemy.types import VARCHAR
from sqlalchemy.types import CHAR
from sqlalchemy.types import DATE
from sqlalchemy.types import DATETIME
from sqlalchemy import ForeignKey
from sqlalchemy import Column
from applications.core.utils import utime

from applications.common.models.base import BaseModel


class User(BaseModel):
    """
    user model
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, nullable=False, default=None)
    password = Column(String(128), nullable=False, default='')
    username = Column(String(40), nullable=False)
    mobile = Column(String(16), nullable=True)
    email = Column(String(80), nullable=True)
    level_id = Column(Integer, nullable=False, default=0)
    # 经验值
    experience = Column(Integer, nullable=False, default=0)
    # 性别(男 male ，女 female 隐藏 hide)
    sex = Column(String(10), nullable=False, default='hide')
    # 头像
    avatar = Column(String(255), nullable=True, default='')
    # 签名
    sign = Column(String(255), nullable=True, default='')
    login_count = Column(Integer, nullable=False, default=0)
    lastlogin_ip = Column(String(40), nullable=False, default='')
    lastlogin_at = Column(Integer, nullable=True, default=0)
    ref_user_id = Column(Integer, default='')
    # 状态:( 0 禁用；1 启用, 默认1 删除 -1)
    status = Column(Integer, nullable=False, default=1)
    created_at  = Column(Integer, default=utime.timestamp)
    reg_ip = Column(String(40), nullable=False, default='')
    # 客户端：web wechat android ios mobile
    reg_client = Column(String(40), nullable=False, default='')
    reg_bundle_id = Column(String(20), nullable=False, default='')
    reg_channel = Column(String(20), nullable=False, default='')
    lang = Column(String(10), nullable=False, default='')
    region = Column(String(2), nullable=False, default='')

    sex_options = {
        '': '不填',
        'hide': '隐藏',
        'male': '男',
        'female': '女',
        'other': '其他',
    }

    @property
    def sex_option(self):
        return self.sex_options.get(self.sex, '隐藏')


class UserLoginLog(BaseModel):
    """
    用户登录日志表
    """
    __tablename__ = 'user_login_log'

    id          = Column(Integer, primary_key=True, nullable=False, default=None)
    user_id     = Column(Integer, ForeignKey('user.id'))
    ip          = Column(String(40), nullable=False)
    client      = Column(String(20), nullable=True)
    created_at  = Column(Integer, default=utime.timestamp)

class UserOperationLog(BaseModel):
    """
    用户操作日志
    """
    __tablename__ = 'user_operation_log'

    id          = Column(Integer, primary_key=True, nullable=False, default=None)
    user_id     = Column(Integer)
    ip          = Column(String(40), nullable=False)
    client      = Column(String(20), nullable=True)
    #用户账号： email or mobile or username
    account     = Column(String(40), default='')
    #会员操作类型： email_reset_pwd mobile_reset_pwd activate_email
    action      = Column(String(20), nullable=True)
    admin_id      = Column(Integer, nullable=True)
    created_at  = Column(Integer, default=utime.timestamp)

class UserSmsCode(BaseModel):
    """
    用户短信验证码
    """
    __tablename__ = 'user_sms_code'

    id          = Column(Integer, primary_key=True, nullable=False, default=None)
    platform    = Column(String(20), default='')  # 短信平台标识
    message     = Column(String(150))             # 验证码信息
    code        = Column(String(10))              # 短信验证码
    ip          = Column(String(15))
    created_at  = Column(Integer)                 # 创建记录Unix时间戳
    expire_time = Column(Integer)                 # 过期时间 单位秒
    client      = Column(String(20))              # 客户端：web wechat android ios mobile
    user_id     = Column(Integer)                 # 会员ID
    mobile      = Column(String(20))              # 手机号码


class UserLevel(BaseModel):
    """
    用户级别表
    """
    __tablename__ = 'user_level'
    id= Column(Integer, primary_key=True, nullable=False, default=None)
    name=Column(String(80),nullable=False)
    min_exper=Column(Integer,nullable=False,default=0)
    max_exper=Column(Integer,nullable=False,default=0)
    intro=Column(String(255),nullable=False)
    default=Column(Integer,default=0)
    expire=Column(Integer,default=0)
    status=Column(Integer,default=1)
    created_at=Column(Integer,default=utime.timestamp())

class UserBankCard(BaseModel):
    """
    用户银行卡
    """
    __tablename__ = 'user_bank_card'
    id = Column(Integer, primary_key=True, nullable=False, default=None)
    user_id = Column(Integer, nullable=False)
    realname = Column(String(40), nullable=False, default='')  # 持卡人姓名
    mobile = Column(String(20), nullable=False, default='')  # 银行预留手机号
    bank = Column(String(25), nullable=False, default='')  # 银行标识符
    bank_branch = Column(String(100), nullable=False, default='')  # 银行支行
    bankcard_no = Column(String(40), nullable=False, default='')  # 银行卡号
    authorized = Column(Integer, default=0)  # 认证状态:( 0 待审核；1 审核通过, 2 审核失败)
    created_at = Column(Integer, default=utime.timestamp())  # 创建时间
    status = Column(Integer, default=0)  # 状态:( 0；1 默认； 删除 -1)

class UserFeedback(BaseModel):
    """
    意见反馈
    """
    __tablename__ = 'user_feedback'
    id = Column(Integer, primary_key=True, nullable=False, default=None)
    user_id = Column(Integer, nullable=False)
    admin_id = Column(Integer, nullable=False)
    type = Column(String(8), nullable=False, default='other')  # 类型 (咨询 advisory;建议 suggest; 其他 other；)
    content = Column(String(200), nullable=False, default='')  # 反馈内容
    reply = Column(String(255), nullable=False, default='')  # 回复内容
    email = Column(String(25), nullable=False, default='')  # 邮箱
    other = Column(String(40), nullable=False, default='')  # 其他联系方式 微信或手机号
    version = Column(String(10))  # 版本号
    client = Column(String(20))  # 客户端
    ip = Column(String(40))  # 客户端ip
    created_at = Column(Integer, default=utime.timestamp())  # 创建时间
    handle_at = Column(Integer)  # 处理时间
    status = Column(Integer, default=0)  # 状态:( 0 未处理；1 已处理, 默认0)

class UserDevice(BaseModel):
    """
    意见反馈
    """
    __tablename__ = 'user_device'
    id = Column(Integer, primary_key=True, nullable=False, default=None)
    user_id     = Column(Integer, ForeignKey('user.id'))
    did = Column(String(40), nullable=True)
    ip = Column(String(40), nullable=False)
    created_at  = Column(Integer, default=utime.timestamp)
