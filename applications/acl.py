#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""系统权限控制模块

>>> 注意：
* 节点id一定要保证唯一性
* 节点level从0开始，目前情况只用到 0 1 2 这3级
* 节点之间的父子关系要明确，level要和父子关系对应好
* 在获取URL的时候会自动排除重复URL
"""

acl_nodes = [
    {
        'id': 'dashboard',
        'url': ['/admin/dashboard', '/admin', '/admin/index'],
        'handler': 'admin.handlers.dashboard.DashboardHandler',
        'name': '控制面板',
        'class': '',
        'pid': '',
        'level':0,
        'show_top': True,
        'show_left': True,
    },
    {
        'id': 'dashboard_index',
        'url': '/admin/dashboard',
        'handler': 'admin.handlers.dashboard.DashboardHandler',
        'name': '控制面板访问',
        'class': '',
        'pid': 'dashboard',
        'level':1,
        'show_top': False,
        'show_left': True,
    },
    {
        'id': 'admin_user',
        'url': '/admin/user',
        'handler': 'admin.handlers.user.UserHandler',
        'name': '用户',
        'remark': '用户管理模块（用户增删查改、用户组增删查改、用户权限配置等）',
        'class': '',
        'pid': '',
        'level':0,
        'show_top': True,
        'show_left': False,
    },
    {
        'id': 'admin_user_index',
        'url': '#',
        'handler': '',
        'name': '用户管理',
        'class': '',
        'pid': 'admin_user',
        'level':1,
        'show_top': False,
        'show_left': True,
    },
    {
        'id': 'admin_user_index2',
        'url': ['/admin/user', '/admin/user/?(.html)?'],
        'handler': 'admin.handlers.user.UserHandler',
        'name': '用户列表',
        'class': '',
        'pid': 'admin_user_index',
        'level':2,
        'show_top': False,
        'show_left': True,
    },
    {
        'id': 'admin_user_list',
        'url': ['/admin/user/list', '/admin/user/list/?(.html)?'],
        'handler': 'admin.handlers.user.UserListHandler',
        'name': 'Ajax查询用户',
        'class': '',
        'pid': 'admin_user_index',
        'level':2,
        'show_top': False,
        'show_left': False,
    },
    {
        'id': 'admin_user_save',
        'url': ['/admin/user/save', '/admin/user/save/?(.html)?'],
        'handler': 'admin.handlers.user.UserSaveHandler',
        'name': '添加/编辑用户',
        'class': '',
        'pid': 'admin_user_index',
        'level':2,
        'show_top': False,
        'show_left': False,
    },
    {
        'id': 'user_group',
        'url': '/admin/user/group',
        'handler': 'admin.handlers.user.GroupHandler',
        'name': '用户组管理',
        'class': '',
        'pid': 'admin_user',
        'level':1,
        'show_top': False,
        'show_left': True,
    },
    {
        'id': 'user_group_list',
        'url': '/admin/user/group/list/?(.html)?',
        'handler': 'admin.handlers.user.GroupListHandler',
        'name': 'Ajax查询用户组',
        'class': '',
        'pid': 'user_group',
        'level':2,
        'show_top': False,
        'show_left': False,
    },
    {
        'id': 'user_group_save',
        'url': '/admin/user/group/save/?(.html)?',
        'handler': 'admin.handlers.user.GroupSaveHandler',
        'name': '添加/编辑用户组',
        'class': '',
        'pid': 'user_group',
        'level':2,
        'show_top': False,
        'show_left': False,
    },
    {
        'id': 'user_group_delete',
        'url': '/admin/user/group/delete/?(.html)?',
        'handler': 'admin.handlers.user.GroupSaveHandler',
        'name': '删除用户组',
        'class': '',
        'pid': 'user_group',
        'level':2,
        'show_top': False,
        'show_left': False,
    },
    {
        'id': 'user_group_accredit',
        'url': '/admin/user/group/accredit/?(.html)?',
        'handler': 'admin.handlers.user.GroupAccreditHandler',
        'name': '用户组授权',
        'class': '',
        'pid': 'user_group',
        'level':2,
        'show_top': False,
        'show_left': False,
    },

    {
        'id': 'other',
        'url': '#',
        'handler': '',
        'name': '其他系统',
        'class': '',
        'pid': '',
        'level':0,
        'show_top': True,
        'show_left': False,
    },

    {
        'id': 'admin_msg_list',
        'url': '/admin/message',
        'handler': 'admin.handlers.sys.MessageHandler',
        'name': '消息管理',
        'class': '',
        'pid': 'other',
        'level':1,
        'show_top': True,
        'show_left': False,
    },
    {
        'id': 'admin_email_list',
        'url': '/admin/email',
        'handler': 'admin.handlers.sys.EmailHandler',
        'name': '邮件管理',
        'class': '',
        'pid': 'other',
        'level':1,
        'show_top': True,
        'show_left': False,
    },

    # passport
    {
        'id': 'admin_login',
        'url': '/admin/login',
        'handler': 'admin.handlers.passport.LoginHandler',
        'name': '',
        'class': '',
        'pid': '',
        'level':0,
        'show_top': False,
        'show_left': False,
    },
    {
        'id': 'adin_logout',
        'url': '/admin/logout',
        'handler': 'admin.handlers.passport.LogoutHandler',
        'name': '',
        'class': '',
        'pid': '',
        'level':0,
        'show_top': False,
        'show_left': False,
    },
]

def _filter_item(item, **args):
    # print("item", type(item), item)
    show_top = args.get('show_top', '')
    children = _make_menus(level=item['level']+1, pid=item['id'], **args)

    item['url'] = item['url'] if type(item['url'])==str else item['url'][0]
    item['children'] = children
    return item

def _make_menus(level=0, pid='', **args):
    """获取菜单按钮

    该方法为私有方法，共 admin_top_menus/0 和 admin_left_menus/1 调用

    Arguments:
        **args {[type]} -- [description]

    Keyword Arguments:
        level {number} -- [description] (default: {0})
        pid {str} -- [description] (default: {''})

    Returns:
        [type] -- [description]
    """
    nodes = args.get('nodes', [])
    nodes = nodes if len(nodes) else acl_nodes
    items = []
    for item in nodes:
        if item['level']==level and item['pid']==pid:
            items.insert(0, _filter_item(item, **args))

    show_top = args.get('show_top', '')
    # print('show_top: ', type(show_top), show_top, type(show_top)==bool, len(items))
    if len(items) and type(show_top)==bool:
        items2 = []
        for item in items:
            if item['show_top']==show_top:
                items2.insert(0, item)
        items = items2

    show_left = args.get('show_left', '')
    # print('show_left: ', type(show_left), show_left, type(show_left)==bool, len(items))
    if len(items) and type(show_left)==bool:
        items2 = []
        for item in items:
            if item['show_left']==show_left:
                items2.insert(0, item)
        items = items2
    return items

def admin_top_menus():
    """获取顶部菜单按钮

    [description]

    Returns:
        [type] -- [description]
    """
    return _make_menus(level=0, pid='', show_top=True, nodes=acl_nodes)
    # return items

def admin_left_menus(pid):
    """获取左侧菜单按钮

    [description]

    Arguments:
        pid {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    # print('admin_left_menus >> ')
    items = _make_menus(level=1, pid=pid, show_left=True, nodes=acl_nodes)
    return items

def _urls():
    urls_items = [(item['url'], item['handler']) for item in acl_nodes if item['url']!='#']
    items_list = []
    for item in urls_items:
        (url, handler) = item
        handler = 'applications.%s' % handler
        if isinstance(url, (str)):
            item2 = (url, handler)
            items_list.insert(0, item2)
        elif isinstance(url, (list)) and len(url):
            for url2 in url:
                item3 = (url2, handler)
                items_list.insert(0, item3)
    # 过滤重复元素
    return list(set(items_list))

urls = _urls()

# children_urls('admin_user', acl_nodes)
def children_urls(pid, nodes=acl_nodes):
    c1_items = [item for item in nodes if item['pid']==pid and item['show_left']==True]
    if len(c1_items)==0:
        return []
    for item2 in c1_items:
        [c1_items.insert(1, item3) for item3 in nodes if item3['pid']==item2['id'] and item3['show_left']==True]
    return [item['url'] if isinstance(item['url'], (str)) else item['url'][0] for item in c1_items]

def get_acl_id(uri, nodes=acl_nodes):
    c1_items = [item for item in nodes if item['url']==uri]
    if len(c1_items)==0:
        return ''
    elif len(c1_items)==1 and c1_items[0]['pid']!='':
        return c1_items[0]['pid']
    return get_acl_id(c1_items[0]['url']) if c1_items[0]['pid'] else c1_items[0]['id']


def accredit(nodes):
    items0 = _make_menus(level=0, pid='', nodes=nodes)
    ret_items = []
    for item0 in items0:
        pid = item0['id']
        items1 =  _make_menus(level=1, pid=pid)
        temp_items = []
        for item1 in items1:
            pid = item1['id']
            items2 = _make_menus(level=2, pid=pid)
            item1['children'] = items2
            temp_items.insert(1, item1)

        item0['children'] = temp_items
        ret_items.insert(1, item0)
    return ret_items
