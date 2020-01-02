[TOC]

基于Tornado的restful API 系统；tornado 建议使用6.0.1

# wiki
* [生产环境部署](https://gitee.com/leeyi/py_admin/wikis/%E7%94%9F%E4%BA%A7%E7%8E%AF%E5%A2%83%E9%83%A8%E7%BD%B2?sort_id=403630)

# [开发约定](https://gitee.com/leeyi/trest/blob/master/promise.md)

* 开发约定 [https://gitee.com/leeyi/trest/blob/master/promise.md](https://gitee.com/leeyi/trest/blob/master/promise.md)
* 其他约定遵从[Python风格规范](http://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_language_rules/) 、 [Python 编码规范](http://liyangliang.me/posts/2015/08/simple-python-style-guide/)

# demo
API响应，在任意需要的地方 raise JsonError
```
from trest.exception import JsonError

raise JsonError('msg')
raise JsonError('msg', 0)
raise JsonError('msg', 1, [])
raise JsonError('msg', 1, [1,2,3])
```

# 环境依赖
* 本人在在MacBookPro下采用 Python3.7.2+MySQL5.7开发，应该可以所以操作系统化下面跑起来 （MySQL5.6.2及以上）
* 不打算支持Python3.6以下的Python环境了，会跟随tornado或Python升级代码
* 操作数据库的ORM框架为 SQLAlchemy（SQLAlchemy包括用于SQLite，Postgresql，MySQL，Oracle，MS-SQL，Firebird，Sybase等的语言），如果要用其他数据库，本软件应该要做少许的调整
* 引入 pipenv https://github.com/pypa/pipenv/blob/master/docs/advanced.rst

## 设置全局变量


```
echo -e '\nexport PIPENV_VENV_IN_PROJECT=1' >> /etc/profile
source /etc/profile
```


# 项目启动

## 原生开发启动
```
git clone https://gitee.com/leeyi/py_admin.git py_admin && cd py_admin

pipenv install --skip-lock --pypi-mirror=http://mirrors.cloud.aliyuncs.com/pypi/simple
// or
pipenv install --dev --skip-lock

// 配置本地开发环境变量，然后启动
cp configs/dev.yaml configs/product.yaml
echo '# TREST_ENV is not one of the local, dev, test, or product
TREST_ENV : local' > .env

// 开启虚拟环境
pipenv shell
// 启动项目
python server.py --port=5080

// 退出pipenv
exit
```
pipenv install -e git+https://gitee.com/leeyi/trest.git@master#egg=trest

# DB
参见 datas/mysql 目录

## db other
```
show processlist;

set global validate_password_policy=0;
create database db_py_admin default charset utf8 COLLATE utf8_general_ci;
CREATE USER user_py_admin IDENTIFIED BY 'eb27acWq#16E1';
GRANT ALL ON db_py_admin.* TO 'user_py_admin'@'%';
flush privileges;


// 只导出表结构
mysqldump --opt -d db_py_admin -u root -p > datas/db.sql
// alter database db_py_admin collate utf8_general_ci
```
# features
* 后台配置添加
* 后台用户角色管理
* 基于角色的权限功能，后台用户管理
* 登录密码经过RSA加密，后台可配置是否开启该功能，后台可设置公钥私钥；
* 用户密码使用“ PBKDF2 + HMAC + SHA256”加密存储；
* 数据库密码经过AES加密，没有明文存储，进过AES加密的密码，格式 aes::: + ciphertext；
* 后台菜单管理参考文件（applications/admin/menu.py）docstring
* 参考网站 [torngas](https://github.com/mqingyn/torngas)
* 其他特性继承自 tornado

# 目录说明
```
git clone ...
cd py_admin

tree -I '*svn|*node_module*|*git|py3|*.pyc|__pycache__|statics'
```

### 使用 OpenSSL 生成公钥私钥
```
// 生成 RSA 私钥
openssl genrsa -out dev_privkey.pem 1024
// 从密钥中提取公钥
openssl rsa -pubout -in dev_privkey.pem -out dev_pubkey.pem
```

查询数据用 GET
添加/修改数据用 POST
删除数据用 DELETE

还有发放奖励功能需要做
用户上传头像的功能


### Other
```
        from applications.core.utils.encrypter import RSAEncrypter
        from applications.vsn1.services import ApiVsnService
        (code_, msg_, pubkeyser) = ApiVsnService.pubkeyser('1.0.0')
        plaintext = 'Ly123456'
        ciphertext = RSAEncrypter.encrypt(plaintext, pubkeyser)
        print('ciphertext ', ciphertext)
```
