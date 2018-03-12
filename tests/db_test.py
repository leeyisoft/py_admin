#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

import unittest


# 把当前目录添加到 sys.path 开头
root_path = os.getcwd()
sys.path.insert(0, os.path.dirname(root_path))


from applications.utils.db import Mysql

if __name__ == "__main__":
    print('root_path : ', os.path.dirname(root_path))

    lists = Mysql.table('user').fields('username, password').where('1=1').select()
    print(lists)
    print("\n")
    # lists = Mysql.table('user').fields('username, password').where('1=1').find()
    # print(lists)

    try:
        pass
    except KeyboardInterrupt:
        sys.exit(0)