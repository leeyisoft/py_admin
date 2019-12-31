"""
公共的函数都放到这里
"""
from applications.common.utils import sys_config


def tpl_params():
    """模板公共变量
    Returns:
        dict -- 网页底部变量
    """
    footer_address = sys_config('footer_address', ['title', 'value'])
    working_time = sys_config('working_time', ['title', 'value'])
    company_hotline = sys_config('company_hotline', ['title', 'value'])
    company_email = sys_config('company_email', ['title', 'value'])
    site_name = sys_config('site_name')

    params = {
        'footer_address': footer_address,
        'working_time': working_time,
        'company_hotline': company_hotline,
        'company_email': company_email,
        'site_name': site_name,
    }
    return params
