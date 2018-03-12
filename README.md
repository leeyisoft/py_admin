[TOC]

特别声明：
> 本软件参考 https://github.com/mqingyn/torngas 很多代码直接copy了torngas的，部分代码多了小调整以兼容Python3

# init db
```
set global validate_password_policy=0;
create database db_py_admin default charset utf8;
GRANT ALL PRIVILEGES ON db_py_admin.* TO 'user_py_admin'@'%' IDENTIFIED BY 'eb26acWq16E1' WITH GRANT OPTION;
flush privileges;
```

# features
* 登录密码经过RSA加密，后台可配置是否开启该功能，后台可设置公钥私钥；
* 数据库密码经过AES加密，没有明文存储，进过AES加密的密码，格式 aes::: + ciphertext；
* 数据库和时间相关的字段统一使用datetime(6)数据类型，通过Python3取UTC时间
* 基于REDIS的Session管理
* 数据库、缓存、日志、中间件等模块copy自 [torngas](https://github.com/mqingyn/torngas)
* UI 使用 [layui-v2.2.5](https://www.layui.com)
* 其他特性继承自 tornado

# 目录说明
```
git clone ...
cd py_admin
./init.sh


tree -I '*svn|*node_module*|*git|py3|*.pyc|__pycache__|statics'
```

# UI
安装步骤参考 https://pro.ant.design/docs/getting-started-cn
```
cd ui
pro new
    admin

npm install
npm start
npm run build // 生成 dist
```

### 使用 OpenSSL 生成公钥私钥
```
// 生成 RSA 私钥
openssl genrsa -out private.pem 1024
// 从密钥中提取公钥
openssl rsa -pubout -in private.pem -out public.pem
```

        conf = Config(key='front_end_title',
            value='前端标题',
            remark='前端标题',
            # status=1,
            # created_at=datetimezone(),
            )
        Config.session().merge(conf)
        Config.session.commit()

查询数据用 GET
添加/修改数据用 POST
删除数据用 DELETE


