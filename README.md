[TOC]

基于Tornado的web mvc框架。参考了torngas（torngas大量参考和借鉴了Django的设计模式），形成一套基于tornado的Django like应用层开发框架。tornado 建议使用5.0.2及以上版本

特别声明：
> 本软件很多地方“参考”了[torngas](https://github.com/mqingyn/torngas)，在MacBookPro下采用 Python3.6+MySQL5.7开发；因为torngas没有更新了（最后一次提交在2016年9月份，参考的时候它也不支持Python3），所以就自己开始“造轮子”了。
# wiki
* [生产环境部署](https://gitee.com/leeyi/py_admin/wikis/%E7%94%9F%E4%BA%A7%E7%8E%AF%E5%A2%83%E9%83%A8%E7%BD%B2?sort_id=403630)

# 开发约定
* 在第一个发布版本之前的“数据库结构、数据变动”，不会给出相应update的SQL语句（如有需要、或者其他建议，欢迎留言）
* 数据库密码经过AES加密，没有明文存储，进过AES加密的密码，格式 aes::: + ciphertext；
* 数据库和时间相关的字段统一使用datetime(6)数据类型，通过Python3取UTC时间
* 数据库表的主键统一用 int(11)
* 只定义了一个API 通过不同的请求方式，来执行不同的操作（<span style="color:red;">查询用get 添加用post 更新用put 删除用delete</span>） [参考](https://blog.csdn.net/dxftctcdtc/article/details/9197639)
* 其他约定遵从[Python风格规范](http://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_language_rules/)、[Python 编码规范](http://liyangliang.me/posts/2015/08/simple-python-style-guide/)

# 环境依赖
* 本人在在MacBookPro下采用 Python3.6+MySQL5.7开发，应该可以所以操作系统化下面跑起来 （MySQL5.6.2及以上）
* 不打算支持Python3.6以下的Python环境了，会跟随tornado或Python升级代码
* 操作数据库的ORM框架为 SQLAlchemy1.2.7（SQLAlchemy包括用于SQLite，Postgresql，MySQL，Oracle，MS-SQL，Firebird，Sybase等的语言），如果要用其他数据库，本软件应该要做少许的调整
* 下列Python依赖会保持最新版本

```
» pip list
Package         Version
--------------- -------
mysqlclient     1.3.12
Pillow          5.1.0
pip             10.0.1
pyasn1          0.4.2
pycrypto        2.6.1
python-dateutil 2.7.2
pytz            2018.4
redis           2.10.6
rsa             3.4.2
setuptools      39.1.0
six             1.11.0
SQLAlchemy      1.2.7
tornado         5.0.2
wheel           0.31.0
```

# 项目启动
```
git clone https://gitee.com/leeyi/py_admin.git py_admin && cd py_admin
// 你首先执行以下这个脚本
sh ./init.sh
// 激活Python3虚拟环境
source py3/bin/activate
// 配置本地开发环境变量，然后启动
cp applications/configs/dev.py applications/configs/local.py

// 启动项目
python server.py
```

# init db
## datas/db.sql
只有表结构数据

## datas/db_data.sql
含默认的后台管理用户、默认菜单、默认配置数据

## db other
```
set global validate_password_policy=0;
create database db_py_admin default charset utf8;
GRANT ALL PRIVILEGES ON db_py_admin.* TO 'user_py_admin'@'%' IDENTIFIED BY 'eb26acWq16E1' WITH GRANT OPTION;
flush privileges;

// 只导出表结构
mysqldump --opt -d db_py_admin -u root -p > datas/db.sql

```
# features
* 后台配置添加
* 后台用户角色管理
* 基于角色的权限功能，后台用户管理
* 登录密码经过RSA加密，后台可配置是否开启该功能，后台可设置公钥私钥；
* 用户密码使用“ PBKDF2 + HMAC + SHA256”加密存储；
* 数据库密码经过AES加密，没有明文存储，进过AES加密的密码，格式 aes::: + ciphertext；
* 数据库和时间相关的字段统一使用datetime(6)数据类型，通过Python3取UTC时间
* 数据库表的主键统一用uuid(32位)
* 参考网站 [torngas](https://github.com/mqingyn/torngas)
* UI 使用 [layui-v2.2.6](https://www.layui.com)
* 其他特性继承自 tornado
* 后台用户登录日志功能
* 前端 注册、登录、修改资料、激活Email、修改密码、通过Email找回密码、上传头像

## im fetures
* group [add group, edit group, delete group]
* move friend to other group


## todo fetures
* 多次登录失败账户锁定功能
* 锁屏功能
* 清理缓存功能

## maybe todo fetures
* 绑定手机号码、绑定多个Email、绑定微信、绑定支付宝、
* 人类验证
* 系统消息
* 用户等级

# FAQ
## 为什么要用 datetime(6) ？
因为表的主键uuid没有“顺序”，有时候需要自然排序，所以，就把datetime设计为了datetime(6)了，这样就有了自然顺序了；而且，附带了更精准的时间。


# 目录说明
```
git clone ...
cd py_admin
./init.sh


tree -I '*svn|*node_module*|*git|py3|*.pyc|__pycache__|statics'
```

### 使用 OpenSSL 生成公钥私钥
```
// 生成 RSA 私钥
openssl genrsa -out private.pem 1024
// 从密钥中提取公钥
openssl rsa -pubout -in private.pem -out public.pem
```

查询数据用 GET
添加/修改数据用 POST
删除数据用 DELETE

还有发放奖励功能需要做
用户上传头像的功能

### IM 参考

http://test.guoshanchina.com/index.php
