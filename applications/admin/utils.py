#!/usr/bin/env python
# -*- coding: utf-8  -*-

import urllib
import functools
from typing import Callable
from typing import Optional
from typing import Awaitable
from tornado.util import import_object
from tornado.web import RequestHandler

from trest.exception import HTTPError
from trest.exception import JsonError
from trest.utils.encrypter import RSAEncrypter


def required_permissions(*dargs, **dkargs):
    """权限控制装饰器
    """
    AdminUser = import_object('applications.common.models.admin_user.AdminUser')
    def wrapper(method):
        # @functools.wraps(method)
        def _wrapper(*args, **kargs):
            code = dargs[0] if dargs else method.__name__
            self = args[0]
            # print('required_permissions dargs ', type(dargs), dargs)
            # print('required_permissions code ', type(code), code)
            # print('required_permissions self ', type(self), self)

            if self.super_role():
                return method(*args, **kargs)

            user_id = self.current_user.get('id')
            obj = AdminUser.Q.filter(AdminUser.id==user_id).first()
            if not obj:
                raise HTTPError(401)
                # raise JsonError('未授权', 401)
            if not code:
                raise HTTPError(401)
                # raise JsonError('未授权', 401)
            permission = obj.user_permission + obj.role_permission
            if type(code)==str:
                if code in permission:
                    return method(*args, **kargs)
            elif type(code)==list:
                if any([cd in permission for cd in code]):
                    return method(*args, **kargs)
            raise HTTPError(401)
            # raise JsonError('未授权', 401)
        return _wrapper
    return wrapper


def admin_required_login(
    method: Callable[..., Optional[Awaitable[None]]]
) -> Callable[..., Optional[Awaitable[None]]]:
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in, they will be redirected to the configured
    `login url <RequestHandler.get_login_url>`.

    If you configure a login url with a query parameter, Tornado will
    assume you know what you're doing and use it as-is.  If not, it
    will add a `next` parameter so the login page knows where to send
    you once you're logged in.
    """

    @functools.wraps(method)
    def wrapper(  # type: ignore
        self: RequestHandler, *args, **kwargs
    ) -> Optional[Awaitable[None]]:
        if not self.current_user:
            if self.request.method in ("GET", "HEAD"):
                url = self.get_login_url()
                next_url = ''
                if "?" not in url:
                    if urllib.parse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        assert self.request.uri is not None
                        next_url = self.request.uri
                    url += "?" + urllib.parse.urlencode(dict(redirect=next_url))
                    data = {'login_url':url, 'next_url': next_url,}
                accept = self.request.headers.get('Accept', '')
                if accept.startswith('application/json'):
                    raise JsonError('请重新登录', 706)
                else:
                    return self.redirect(url)
            raise JsonError('请重新登录....', 706)
        return method(self, *args, **kwargs)
    return wrapper
