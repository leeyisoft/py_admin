#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
公共常量定义，命名风格大写下划线
"""

# 公共类型
COMMON_STATUS = (
    (1, '激活'),
    (0, '待激活'),
    (-1, '删除'),
)
COMMON_STATUS2 = (
    (1, '激活'),
    (0, '待激活'),
)

# 隐私授权数据
PRIVACY_DATA = (
    ('PORTION', '部分授权'),
    ('GRANTED', '已授权'),
    ('NOT_GRANTED', '未授权'),
)

# 是否复借
IS_REPEATED = (
    (1, '复借'),
    (0, '首借'),
)

# 贷款类型
LOAN_TYPE = (
    (1, '发薪日贷款'),
    (2, '展期'),
)

# 语言

LANG_TYPE = (
    ('cn', '简体中文'),
    ('en', '英文'),
    ('id', '印尼语'),
    ('ph', '菲律宾语'),
)
# 案件分配状态
LOAN_ORDER_STATUS = (
    (2, '初审案件'),
    (3, '复审案件'),
    (4, '终审案件'),
)

# 贷款状态
LOAN_STATUS = (
    (0, '已提交'),
    (1, '预审'),
    (2, '初审'),
    (3, '复审'),
    (4, '终审'),
    (5, '准备放款'),
    (6, '放款中'),
    (-6, '放款失败'),
    (7, '还款期'),
    (8, '部分还款'),
    (9, '已还清'),
    (10, '逾期'),
    (13, '预审转人工'),
    (14, '已拒绝'),
    (15, '用户主动取消'),
    (16, '系统关闭'),
    (18, '催收'),
)

LOAN_STATUS2 = (
    (0, '已提交'),
    (1, '预审'),
    (2, '初审'),
    (3, '复审'),
    (4, '终审'),
    (5, '准备放款'),
    (6, '放款中'),
    (7, '还款期')
)

# 放款状态
ISSUE_STATUS = (
    (1, '新建'),
    (2, '放款中'),
    (3, '放款成功'),
    (4, '放款失败'),
    (5, '取消中'),
    (6, '已取消')
)

# 催收案件状态
CASE_STATUS = (
    (0, '创建'),
    (1, '催收中'),
    (2, '催收完成'),
    (3, '催收失败'),
    (4, '已再分配'),
)

# 催收案件流转类型
FLOW_TYPE = (
    ('inside', '内部流转'),
    ('weight', '权重流转'),
)

# 页面类型
PAGE_TYPE = (
    ('all_application', '全部申请详情页面'),
    ('first_review', '初审详情页面'),
    ('second_review', '复审详情页面'),
    ('final_review', '终审详情页面'),
    ('collector_collection_detail', '催收员催收详情页面'),
    ('admin_collection_detail', '管理员催收详情页面'),
)

# 子页面
PAGE_TAB = (
    ('customer_info', '客户信息'),
    ('additional_info', '其他信息'),
    ('evidence', '凭证'),
    ('charge_data', '收费数据'),
    ('third_party_info', '第三方数据'),
    ('common_bottom_info', '子页面公用部分'),
)

# 页面模块
PAGE_MODULE = (
    ('pre_review_conclusion_card', '待人工审核'),
    ('basic_info_card', '基本信息'),
    ('all_payment_code_card', '还款码信息'),
    ('personal_info_card', '个人信息'),
    ('employment_info_card', '雇佣信息'),
    ('identity_report_card', '身份证验证结果'),
    ('face_verify_card', '活体校验'),
    ('star_risk_report_card', '风险报告'),
    ('inner_review_card', '内部审批'),
    ('contact_card', '紧急联系人息'),
    ('phone_sms_log_card', '短信信息'),
    ('all_harvest_button', '同步最新授权数据'),
    ('phone_call_log_card', '通话记录'),
    ('phone_contact_card', '联系人通讯录'),
    ('phone_gps_card', '手机定位记录'),
    ('review_tasks_card', '审批案件任务'),
    ('loan_info_card', '贷款信息'),
    ('review_log_card', '审批记录'),
    ('conclusions_card', '机审结论'),
    ('collection_log_card', '催收日志'),
    ('history_application_card', '历史申请记录'),
    ('bankcard_info_card', '银行卡信息'),
    ('sky_pay_card', 'skypay信息'),
    ('deposit_history_card', '还款记录'),
    ('loan_issued_history_card', '放款记录'),
    ('review_evidence_card', '审批凭证'),
    ('repayment_evidence_card', '还款凭证'),
    ('third_party_info_card', '第三方数据'),
    ('more_device_card', '设备列表'),
    ('face_info_card', ' 风险人脸'),
    ('phone_verify_card', '手机检验'),
    ('collection_call_record_card', '外呼记录'),
    ('charge_data_info_data', '星探人脸'),
    ('third_party_services_card', '第三方服务'),
    ('spider_data', '爬虫数据'),
)

# 短信类型
SMS_TYPE = (
    ('loan', '待款'),
    ('collection', '催收'),
    ('other', '其他'),
)

# 短信模板类型
SMS_APPLICATION = (
    ('loan_submit', '申请提交'),
    ('loan_rejected', '订单被拒'),
    ('customer_hold', '用户冻结'),
    ('loan_closed', '订单关闭'),
    ('loan_approved', '订单审核通过'),
    ('realtime_loan', '实时放款'),
    ('loan', '放款'),
    ('loan_success', '放款成功'),
    ('overdue_day_reminder', '逾期当天短信'),
    ('overdue_reminder', '逾期短信'),
    ('overdue_reminder_m1', '逾期一月短信'),
    ('repayment_reminder', '还款短信'),
    ('loan_payoff', '成功还款'),
    ('collection', '催收短信'),
    ('welcome', '欢迎短信'),
    ('test', '测试'),
    ('orther_channel', '其他渠道'),
    ('login', '登录'),
)

# 短信触发类型
SMS_TRIGGER = (
    ('repayment', '还款短信'),
    ('overdue', '逾期短信'),
)

# 短信状态
SMS_STATUS = (
    (0, '等待发送'),
    (1, '正在发送'),
    (2, '发送成功'),
    (3, '发送失败'),
)

# 短信渠道
SMS_CHANNEL = (
    ('unknown_key', 'UNKNOWN_YET'),
)

# 公司类型
COMPANY_TYPE = (
    ('outer', '外部委派'),
    ('inner', '内部'),
)
COMPANY_MODULE = (
    ('review', '审批'),
    ('collection', '催收'),
    ('manage', '管理'),
    ('service', '客服'),
)

# 标签类型
TAG_TYPE = (
    ('loan', 'loan'),
)

# 黑名单类型
BLACK_TYPE = (
    ('ktp', '身份证'),
    ('mobile', '手机号'),
    ('fullname', '姓名'),
    ('company_name', '公司名'),
    ('company_phone', '公司电话'),
)

BANK_TYPE = (
    ('payment', '放款银行渠道 '),
    ('repayment', '还款银行渠道'),
)

# 性别类型
SEX_TYPE = (
    ('', '不填'),
    ('hide', '隐藏'),
    ('male', '男'),
    ('female', '女'),
    ('other', '其他'),
)

# 联系人认证和前端约定的数据格式
AUTH_CONTACT = [
    {
        'group': 'c1',
        'title': 'Mother/Father',
        'relation': {
            'Mother': 'Mother',
            'Father': 'Father'
        },
        'required': True,
    },
    {
        'group': 'c2',
        'title': 'Friend',
        'relation': 'Friend',
        'required': False,
    },
    {
        'group': 'c3',
        'title': 'Brother/Sister',
        'relation': {
            'Brother': 'Brother',
            'Sister': 'Sister'
        },
        'required': True,
    }
]

# 职业选项
CAREER_OPTIONS = (
    ('会计', 'ACCOUNTING'),
    ('飞行员', 'AIR_TRANSPORTATION'),
    ('建筑师', 'ARCHITECT'),
    ('畜牧人员', 'BREEDER'),
    ('经纪人', 'BROKER'),
    ('厨师', 'CHEF'),
    ('咨询师', 'CONSULTANT'),
    ('工匠', 'CRAFTSMAN'),
    ('设计师', 'DESIGNER'),
    ('批发商', 'DISTRIBUTOR'),
    ('医生', 'DOCTOR'),
    ('工程师', 'ENGINEER'),
    ('企业主', 'ENTREPRENEUR'),
    ('执行官', 'EXECUTIVE'),
    ('农民', 'FARMER'),
    ('渔民', 'FISHERMAN'),
    ('行政管理', 'GENERAL_ADMINISTRATION'),
    ('政府雇员', 'GOVERNMENT_EMPLOYEE'),
    ('家庭主妇', 'HOUSEWIFE'),
    ('非正式工人', 'INFORMAL_WORKERS'),
    ('IT', 'INFORMATION_TECHNOLOGY'),
    ('力工', 'LABOR'),
    ('司机', 'LAND_TRANSPORTATION'),
    ('律师', 'LAWYER'),
    ('市场人员', 'MARKETING'),
    ('医务人员', 'MEDICAL_PERSONNEL'),
    ('军官', 'MILITARY'),
    ('其他', 'OTHER'),
    ('警察', 'POLICE'),
    ('研究院', 'RESEARCHER'),
    ('退休人员', 'RETIRED'),
    ('海海员', 'SEA_TRANSPORTATION'),
    ('安全员', 'SECURITY'),
    ('政府官员', 'STATE_OFFICIALS'),
    ('学生', 'STUDENT'),
    ('教师', 'TEACHER'),
    ('服务员', 'WAITER'),
    ('艺术家', 'WORKERS_ART'),
)

#
SALARY_OPTIONS = (
    ('低于6K', 'BELOW_6K'),
    ('6K到10K', 'BETWEEN_6K_10K'),
    ('10K到15K', 'BETWEEN_10K_15K'),
    ('15K到20K', 'BETWEEN_15K_20K'),
    ('20K到30K', 'BETWEEN_20K_30K'),
    ('超过30K', 'OVER_30K'),
)

#
EDUCATION_OPTIONS = (
    ('初中', '初中'),
    ('高中/专科', '高中/专科'),
    ('本科', '本科'),
    ('本科以上', '本科以上'),
)

#
MARITAL_OPTIONS = (
    ('已婚', '已婚'),
    ('未婚', '未婚'),
    ('离异', '离异'),
    ('其他', '其他'),
)

#
CHILDREN_OPTIONS = (
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '3个以上'),
)

# 子页面名称
SUBPAGE_NAME = (
    ('customer_info', '客户信息'),
    ('first_review', '初审详情页面',),
    ('evidence', '凭证'),
    ('charge_data', '收费数据'),
    ('third_party_info', '第三方数据'),
    ('common_bottom_info', '子页面公用部分'),
)

region_code = {
    # region_code 字典的key必须小写
    # https://countrycode.org/
    'cn': {
        'region': 'China',
        'number': '86',
        'code': 'CN',
        'iso_code': 'CN / CHN'
    },
    'ph': {
        'region': 'Philippines',
        'number': '63',
        'code': 'PH',
        'iso_code': 'PH / PHL'
    },
    'id': {
        'region': 'Indonesia',
        'number': '62',
        'code': 'ID',
        'iso_code': 'ID / IDN'
    }
}

# 订单审核：拒绝原因
refuse_reason = [
    '内部黑名单',
    '第三方黑名单',
    '联系人信息虚假',
    '内含高危字段且击中三次以上',
    '公司信息虚假',
    '信息虚假',
    '身份证过期',
    '身份证姓名与填写姓名不符',
    '第三方贷款申请',
    '通话记录不足',
    '联系人信息不足',
    '收入不足',
    '短信记录不足',
    '贷款逾期超过7天',
    '行业限制',
    '居住地限制',
    '职业限制',
    '自动拒绝贷款',
    '其他',
]

# 拒绝原因
LOAN_REFUSE_REASON = (
    ('内部黑名单', '内部黑名单'),
    ('第三方黑名单', '第三方黑名单'),
    ('联系人信息虚假', '联系人信息虚假'),
    ('内含高危字段且击中三次以上', '内含高危字段且击中三次以上'),
    ('公司信息虚假', '公司信息虚假'),
    ('信息虚假', '信息虚假'),
    ('身份证过期', '身份证过期'),
    ('身份证姓名与填写姓名不符', '身份证姓名与填写姓名不符'),
    ('第三方贷款申请', '第三方贷款申请'),
    ('通话记录不足', '通话记录不足'),
    ('联系人信息不足', '联系人信息不足'),
    ('收入不足', '收入不足'),
    ('短信记录不足', '短信记录不足'),
    ('贷款逾期超过7天', '贷款逾期超过7天'),
    ('行业限制', '行业限制'),
    ('居住地限制', '居住地限制'),
    ('职业限制', '职业限制'),
    ('自动拒绝贷款', '自动拒绝贷款'),
    ('其他', '其他')
)


# 机审拒绝原因
MACHINE_AUDIT_REFUSE_REASON = (
    ('customer.education.limit', 'CUSTOMER_EDUCATION_LIMIT'),
    ('customer.province.limit', 'CUSTOMER_PROVINCE_LIMIT'),
    ('customer.profession.limit', 'CUSTOMER_PROFESSION_LIMIT'),
    ('name.share.birthday', 'NAME_SHARE_BIRTHDAY'),
    ('imei.share.mobile', 'IMEI_SHARE_MOBILE'),
    ('ktp.share.imei', 'KTP_SHARE_IMEI'),
    ('loan.apply.packagename', 'LOAN_APPLY_PACKAGENAME'),
    ('loan.apply.version', 'LOAN_APPLY_VERSION'),
    ('name.share.bankcard', 'NAME_SHARE_BANKCARD'),
    ('name.share.ktp', 'NAME_SHARE_KTP'),
    ('name.share.mobile', 'NAME_SHARE_MOBILE'),
    ('phone.valid.contact.match', 'PHONE_VALID_CONTACT_MATCH'),
    ('phone.valid.total ', 'PHONE_VALID_TOTAL'),
    ('phone.valid.count', 'PHONE_VALID_COUNT'),
    ('phone.valid.percent', 'PHONE_VALID_PERCENT'),
    ('first.apply.min.used', 'FIRST_APPLY_MIN_USED'),
    ('apply.time.validate', 'APPLY_TIME_VALIDATE'),
    ('imei.current.count', 'IMEI_CURRENT_COUNT'),
    ('imei.apply.day.limit', 'IMEI_APPLY_DAY_LIMIT'),
    ('loan.apply.overdue', 'LOAN_APPLY_OVERDUE'),
    ('bankcard.share.mobile', 'BANKCARD_SHARE_MOBILE'),
    ('risk.report.hit.multi.level', 'RISK_REPORT_HIT_MULTI_LEVEL'),
    ('sms.sensitive.words.limit', 'SMS_SENSITIVE_WORDS_LIMIT'),
    ('sms.sensitive.words', 'SMS_SENSITIVE_WORDS'),
    ('check.contact.mobile', 'CHECK_CONTACT_MOBILE'),
    ('atest.loan.overdue.days', 'ATEST_LOAN_OVERDUE_DAYS'),
    ('phone.sms.count', 'PHONE_SMS_COUNT'),
    ('imei.apply.count', 'IMEI_APPLY_COUNT'),
    ('contact.overdue.count', 'CONTACT_OVERDUE_COUNT'),
    ('contact.apply.count', 'CONTACT_APPLY_COUNT'),
    ('imei.overdue.count', 'IMEI_OVERDUE_COUNT'),
    ('sms.no.day', 'SMS_NO_DAY'),
    ('phone.no.day', 'PHONE_NO_DAY'),
    ('ignore.identity_verify', 'IGNORE_IDENTITY_VERIFY'),
    ('loan.overdue.days', 'LOAN_OVERDUE_DAYS'),
    ('loan.apply.success', 'LOAN_APPLY_SUCCESS'),
    ('phone.apply.contact', 'PHONE_APPLY_CONTACT'),
    ('phone.contact.count', 'PHONE_CONTACT_COUNT'),
    ('phone.sms.no', 'PHONE_SMS_NO'),
    ('his.reject', 'HIS_REJECT'),
    ('his.approved', 'HIS_APPROVED'),
    ('his.overdue', 'HIS_OVERDUE'),
    ('contact.limit', 'CONTACT_LIMIT'),
    ('imei.share.name', 'IMEI_SHARE_NAME'),
    ('imei.share', 'IMEI_SHARE'),
    ('ktp.share', 'KTP_SHARE'),
    ('bankcard.share', 'BANKCARD_SHARE'),
    ('age.range', 'AGE_RANGE'),
    ('ktp.validate', 'KTP_VALIDATE'),
    ('backlist', 'BACKLIST'),
    ('risk.report.hit.rules', 'RISK_REPORT_HIT_RULES'),
    ('ignore.face.contrast', 'IGNORE_FACE_CONTRAST'),
    ('thirdparty.data', 'THIRDPARTY_DATA')
)

# 关闭原因
close_reason = [
    '身份证照片不清晰',
    '身份证照片未包含工作号码',
    '图片非原始身份证照片',
    '图片未包含身份证照片',
    '工作照不清晰',
    '工作照无工装',
    '联系人重复',
    '银行卡号无效',
    '非本人银行卡',
    '请上传身份证',
    '请上传工资单',
    '其他',
]

# 用户状态
USER_STATUS = (
    (1, '激活'),
    (2, '锁定'),
    (0, '禁用'),
)

# 审核任务可选状态
REVIEW_TASK_INTEGRANT = (
    (0, '可选'),
    (1, '必选')
)

# 审核任务分类
REVIEW_CATEGORY = (
    (2, '初审'),
    (3, '复审'),
    (4, '终审'),
)

# 证件类型
ID_TYPE = (
    (1, 'Company ID'),
    (2, 'Driver’s License'),
    (3, 'Government Service Insurance System (GSIS) e-Card'),
    (4, 'GSIS ID'),
    (5, 'IBP ID'),  # Integrated Bar of the Philippines
    (6, 'OWWA ID'),  # Overseas Workers Welfare Administration
    (7, 'Passport'),
    (8, 'Postal ID'),
    (9, 'PRC ID'),  # Professional Regulation Commission
    (11, 'School ID'),
    (12, 'Senior Citizen ID'),
    (13, 'SSS ID'),  # Social Security System
    (14, 'TIN ID'),  # Taxpayer Identification Number
    (15, 'UMID'),  # Unified Multi-Purpose ID
    (16, "Voter's ID")
)

# 订单申请来源
APPLY_SOURCE = (
    ('web', 'web'),
    ('wechat', 'wechat'),
    ('android', 'android'),
    ('ios', 'ios'),
    ('mobile', 'mobile'),
)

# 订单放款状态
LOAN_ISSUE_STATUS = (
    (1, '新建'),
    (2, '放款中'),
    (3, '放款成功'),
    (4, '放款失败'),
    (5, '取消中'),
    (6, '已取消'),
)

# 第三方支付平台
PAY_PLATFORM = (
    ('DRAGONPAY', 'DRAGONPAY'),
    ('SKYPAY_OFFLINE', 'SKYPAY_OFFLINE'),
)

# 第三方支付平台 还款
REPAYMENT_PLATFORM = (
    ('DRAGONPAY', 'DRAGONPAY'),
    ('SKYPAY_OFFLINE', 'SKYPAY_OFFLINE'),
)

# 还款状态
REPAYMENT_STATUS = (
    (1, '新建'),
    (2, '成功'),
    (3, '失败'),
    (4, '已过期'),
    (5, '清算完成')
)
