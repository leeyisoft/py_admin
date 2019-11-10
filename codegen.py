#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
import argparse

from sqlalchemy.schema import MetaData
from sqlalchemy.engine import create_engine

from sqlacodegen.codegen import CodeGenerator

from tornado.options import define

abs_file = os.path.abspath(sys.argv[0])
ROOT_PATH = abs_file[:abs_file.rfind('/')]
define('ROOT_PATH', ROOT_PATH)

sys.path.insert(0, '/Users/leeyi/workspace/py3/trest')

from trest.utils import func
from trest.db.dbalchemy import DBConfigParser


class ModelGenerator(CodeGenerator):
    template = '''\
#!/usr/bin/env python
# -*- coding: utf-8 -*-
{imports}
from trest.db import Model as Base


{models}
'''
    def render(self, outfile):
        rendered_models = []
        for model in self.models:
            if isinstance(model, self.class_model):
                rendered_models.append(self.render_class(model))
            elif isinstance(model, self.table_model):
                rendered_models.append(self.render_table(model))

        imports = self.render_imports()
        imports = imports.replace('from sqlalchemy.ext.declarative import declarative_base', '')
        output = self.template.format(
            imports=imports,
            metadata_declarations=self.render_metadata_declarations(),
            models=self.model_separator.join(rendered_models).rstrip('\n'))
        # print(output, file=outfile)
        fout = open(outfile, 'w', encoding='utf8')
        # 写入文件内容
        fout.write(output)
        # 关闭文件
        fout.close()

class ServiceGenerator:
    template = '''\
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from trest.utils import utime
from trest.logger import SysLogger
from trest.config import settings
from trest.exception import JsonError
from applications.common.models.{classname_underline} import {classname}


class {classname}Service:
    @staticmethod
    def data_list(where, page, per_page):
        """列表记录
        Arguments:
            where dict -- 查询条件
            page int -- 当前页
            per_page int -- 每页记录数

        return:
            Paginate 对象 | None
        """
        query = {classname}.Q

        if 'status' in where.keys():
            query = query.filter({classname}.status == where['status'])
        else:
            query = query.filter({classname}.status != -1)

        pagelist_obj = query.paginate(page=page, per_page=per_page)

        if pagelist_obj is None:
            raise JsonError('暂无数据')
        return pagelist_obj

    @staticmethod
    def get(id):
        """获取单条记录

        [description]

        Arguments:
            id int -- 主键

        return:
            {classname} Model 实例 | None
        """
        if not id:
            raise JsonError('ID不能为空')
        obj = {classname}.Q.filter({classname}.id == id).first()
        return obj

    @staticmethod
    def update(id, param):
        """更新记录

        [description]

        Arguments:
            id int -- 主键
            param dict -- [description]

        return:
            True | JsonError
        """
        param.pop('_xsrf', None)
        param.pop('file', None)
        param.pop('id', None)
        param['updated_at'] = utime.timestamp(3)

        if not id:
            raise JsonError('ID 不能为空')

        try:
            {classname}.Q.filter({classname}.id == id).update(param)
            {classname}.session.commit()
            return True
        except Exception as e:
            {classname}.session.rollback()
            SysLogger.error(e)
            raise JsonError('update error')

    @staticmethod
    def insert(param):
        """插入

        [description]

        Arguments:
            id int -- 主键
            param dict -- [description]

        return:
            True | JsonError
        """
        param.pop('_xsrf', None)
        param['created_at'] = utime.timestamp(3)
        try:
            data = {classname}(**param)
            {classname}.session.add(data)
            {classname}.session.commit()
            return True
        except Exception as e:
            {classname}.session.rollback()
            SysLogger.error(e)
            raise JsonError('insert error')
'''

    def render(self, classname):
        fname = func.hump2underline(classname)
        output = self.template.format(
            classname_underline=fname,
            classname=classname
        )
        # print(output, file=outfile)
        fname = func.hump2underline(classname)
        outfile = f'{ROOT_PATH}/applications/admin/services/{fname}.py'
        fout = open(outfile, 'w', encoding='utf8')
        # 写入文件内容
        fout.write(output)
        # 关闭文件
        fout.close()


class HandlerGenerator:
    template = '''\
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""{classname}控制器
"""
from trest.router import get
from trest.router import put
from trest.router import post
from trest.router import delete
from trest.exception import JsonError

from applications.admin.utils import required_permissions
from applications.admin.utils import admin_required_login

from applications.admin.services.{classname_underline} import {classname}Service

from .common import CommonHandler


class {classname}Handler(CommonHandler):

    @post('{classname_underline}')
    @admin_required_login
    @required_permissions()
    def {classname_underline}_post(self, *args, **kwargs):
        param = self.params()
        {classname}Service.insert(param)
        return self.success()

    @get('{classname_underline}/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def {classname_underline}_get(self, id):
        """获取单个记录
        """
        obj = {classname}Service.get(id)
        data = obj.as_dict() if obj else {{}}
        return self.success(data = data)

    @get(['{classname_underline}','{classname_underline}/(?P<category>[a-zA-Z0-9_]*)'])
    @admin_required_login
    @required_permissions()
    def {classname_underline}_list_get(self, category = '', *args, **kwargs):
        """列表、搜索记录
        """
        page = int(self.get_argument('page', 1))
        per_page = int(self.get_argument('limit', 10))
        title = self.get_argument('title', None)
        status = self.get_argument('status', None)

        param = {{}}
        if category:
            param['category'] = category
        if title:
            param['title'] = title
        if status:
            param['status'] = status

        pagelist_obj = {classname}Service.data_list(param, page, per_page)
        items = []
        for val in pagelist_obj.items:
            data = val.as_dict()
            items.append(data)
        resp = {{
            'page':page,
            'per_page':per_page,
            'total':pagelist_obj.total,
            'items':items,
        }}
        return self.success(data = resp)

    @put('{classname_underline}/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def {classname_underline}_put(self, id, *args, **kwargs):
        param = self.params()
        {classname}Service.update(id, param)
        return self.success(data = param)

    @delete('{classname_underline}/(?P<id>[0-9]+)')
    @admin_required_login
    @required_permissions()
    def {classname_underline}_delete(self, id, *args, **kwargs):
        param = {{
            'status':-1
        }}
        {classname}Service.update(id, param)
        return self.success()
'''

    def render(self, classname):
        fname = func.hump2underline(classname)
        output = self.template.format(
            classname_underline=fname,
            classname=classname
        )
        # print(output, file=outfile)
        outfile = f'{ROOT_PATH}/applications/admin/handlers/{fname}.py'
        fout = open(outfile, 'w', encoding='utf8')
        # 写入文件内容
        fout.write(output)
        # 关闭文件
        fout.close()

def get_metadata(tables):
    # Use reflection to fill in the metadata
    engines = DBConfigParser.parser_engines()
    engine = create_engine(engines['default']['master'][0])
    metadata = MetaData(engine)
    schema = None
    noviews = True
    # tables = None

    metadata.reflect(engine, schema, noviews, tables)
    return metadata

def create_models(tables = None):
    try:
        metadata = get_metadata(tables)

        noindexes = True
        noconstraints = True
        nojoined = True
        noinflect = True
        noclasses = False
        nocomments = False
        # Write the generated model code to the specified file or standard output
        outfile = f'{ROOT_PATH}/applications/common/models/{tables[0]}.py'
        generator = ModelGenerator(metadata, noindexes, noconstraints, nojoined, noinflect, noclasses, nocomments=nocomments)
        # print('generator ', type(generator), generator)
        generator.render(outfile)
    except Exception as e:
        raise

def create_services(tables):
    try:
        generator = ServiceGenerator()
        for t in tables:
            generator.render(func.underline2hump(t, True))
    except Exception as e:
        raise

def create_handlers(tables):
    try:
        generator = HandlerGenerator()
        for t in tables:
            generator.render(func.underline2hump(t, True))
    except Exception as e:
        raise


if __name__ == "__main__":

    metadata = get_metadata(None)
    # print(dir(metadata))
    for table in metadata.sorted_tables:
        print(table.name)
        create_models([table.name])
        # create_services([table.name])
        # create_handlers([table.name])
