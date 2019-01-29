"""
公共的函数都放到这里
"""


from applications.core.cache import sys_config
from applications.core.utils import Func


from .models.content import Article

def tpl_params():
    """模板公共变量
    Returns:
        dict -- 网页底部变量
    """
    populars = Article.populars(6)

    footer_address = sys_config('footer_address', ['title', 'value'])
    telephone = sys_config('telephone', ['title', 'value'])
    fax = sys_config('fax', ['title', 'value'])
    email = sys_config('email', ['title', 'value'])
    site_name = sys_config('site_name')

    params = {
        'footer_address': footer_address,
        'telephone': telephone,
        'fax': fax,
        'email': email,
        'populars_left': populars[:3],
        'populars_right': populars[3:],
        'site_name': site_name,
        'ad_thumb_prefix': '',
        'article_thumb_prefix': '',
        'app_name': 'home',
    }
    return params

def get_ad(position, options={}):
    """
    根据广告位置获取广告列表
    """
    try:
        default = {'get_list': True, 'limit': 3}
        default.update(options)

        ads = Advertisement.Q.filter(status='show', position=position)
        if ads:
            ads = ads.order_by('order').all()[:default['limit']]

        if default['get_list']:
            return ads
    except Exception as e:
        raise e
