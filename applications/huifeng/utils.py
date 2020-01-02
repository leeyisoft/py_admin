"""
公共的函数都放到这里
"""
from trest.utils import utime
from applications.common.utils import sys_config


def tpl_params():
    """模板公共变量
    Returns:
        dict -- 网页底部变量
    """
    working_time = sys_config('working_time', ['title', 'value'])
    company_hotline = sys_config('company_hotline', ['title', 'value'])
    company_email = sys_config('company_email', ['title', 'value'])
    copyright = sys_config('copyright', ['title', 'value'])
    site_name = sys_config('site_name')
    site_logo = sys_config('site_logo')

    params = {
        'working_time': working_time,
        'company_hotline': company_hotline,
        'company_email': company_email,
        'site_name': site_name,
        'site_logo': site_logo,
        'copyright': copyright,
        'utime': utime,
    }
    return params
