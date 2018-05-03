[TOC]

特别声明：
> 本软件参考 https://github.com/mqingyn/torngas 很多地方“参考”了torngas的，支持Python3.6

基于Tornado的web mvc框架。大量参考和借鉴了Django的设计模式，形成一套基于tornado的Django like应用层开发框架。tornado 建议使用5.0以上版本

# 开发约定
* 数据库密码经过AES加密，没有明文存储，进过AES加密的密码，格式 aes::: + ciphertext；
* 数据库和时间相关的字段统一使用datetime(6)数据类型，通过Python3取UTC时间
* 数据库表的主键统一用uuid(32位)
* 其他约定遵从[Python风格规范](http://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_language_rules/)、[Python 编码规范](http://liyangliang.me/posts/2015/08/simple-python-style-guide/)


# 项目启动
```
git clone https://gitee.com/leeyi/py_admin.git py_admin && cd py_admin
// 你首先执行以下这个脚本
sh ./init.sh
// 激活Python3虚拟环境
source py3/bin/activate
// 启动项目
python admin.py
```

# init db
```
set global validate_password_policy=0;
create database db_py_admin default charset utf8;
GRANT ALL PRIVILEGES ON db_py_admin.* TO 'user_py_admin'@'%' IDENTIFIED BY 'eb26acWq16E1' WITH GRANT OPTION;
flush privileges;
```
# features
* 登录密码经过RSA加密，后台可配置是否开启该功能，后台可设置公钥私钥；
* 用户密码使用“ PBKDF2 + HMAC + SHA256”加密存储；
* 数据库密码经过AES加密，没有明文存储，进过AES加密的密码，格式 aes::: + ciphertext；
* 数据库和时间相关的字段统一使用datetime(6)数据类型，通过Python3取UTC时间
* 数据库表的主键统一用uuid(32位)
* 参考网站 [torngas](https://github.com/mqingyn/torngas)
* UI 使用 [layui-v2.2.6](https://www.layui.com)
* 其他特性继承自 tornado

## todo fetures
* 后台用户登录日志功能
* 多次登录失败账户锁定功能
* 图像验证码验证功能
* 锁屏功能
* 清理缓存功能
*

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


