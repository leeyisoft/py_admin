[TOC]

基于Tornado的web mvc框架。参考了torngas（torngas大量参考和借鉴了Django的设计模式），形成一套基于tornado的Django like应用层开发框架。tornado 建议使用6.0.1及以上版本

特别声明：
> 本软件很多地方“参考”了[torngas](https://github.com/mqingyn/torngas)，在MacBookPro下采用 Python3.7+MySQL5.7开发；因为torngas没有更新了（最后一次提交在2016年9月份，参考的时候它也不支持Python3），所以就自己开始“造轮子”了。
# wiki
* [生产环境部署](https://gitee.com/leeyi/py_admin/wikis/%E7%94%9F%E4%BA%A7%E7%8E%AF%E5%A2%83%E9%83%A8%E7%BD%B2?sort_id=403630)


# 开发约定
* 各个INSTALLED_APP之间不要夸应用调用，不同App需要使用的模型放到common/models/[app_name].py文件里，避免跨越App引用模型
* 每个App应该有自己的CommonHandler，如无必要，请直接使用 ` from applications.core.handler import BaseHandler `
* handlers 层 接受请求参数、校验参数，请求services，响应结果，后续处理调用；
* models 层 单纯的和数据表做映射关系，可以在这里添加虚拟熟悉，格式化数据等功能；
* services 层 供handlers层或者其他脚本调用需要事务性的的功能，由它来引入models，操作数据库，比如用户注册功能；数据列表功能，都可以定义到services里面；
* 在第一个发布版本之前的“数据库结构、数据变动”，不会给出相应update的SQL语句（如有需要、或者其他建议，欢迎留言）
* 数据库密码经过AES加密，没有明文存储，进过AES加密的密码，格式 aes::: + ciphertext；
* 数据库和时间相关的字段统一使用Unix时间戳格式 int(11)
* 数据库表的主键统一用 int(11)
* 数据库和利息相关字段数据类型统一用 decimal(4,4)
* 数据库和金额相关字段数据类型统一用 decimal(16,2)
* 异常信息务必记录到`SysLogger.error(e, exc_info=True)`记录到日志里面，便于排查错误
* 只定义了一个API 通过不同的请求方式，来执行不同的操作（<span style="color:red;">查询用get 添加用post 更新用put 删除用delete</span>） [参考](https://blog.csdn.net/dxftctcdtc/article/details/9197639)
* 其他约定遵从[Python风格规范](http://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_language_rules/)、[Python 编码规范](http://liyangliang.me/posts/2015/08/simple-python-style-guide/)

# demo
API响应，在任意需要的地方 raise JsonError
```
from pyrestful.rest import JsonError

raise JsonError(0,'msg')
raise JsonError(0,'msg', [])
raise JsonError(1,'msg', [1,2,3])
```

# 环境依赖
* 本人在在MacBookPro下采用 Python3.7.2+MySQL5.7开发，应该可以所以操作系统化下面跑起来 （MySQL5.6.2及以上）
* 不打算支持Python3.6以下的Python环境了，会跟随tornado或Python升级代码
* 操作数据库的ORM框架为 SQLAlchemy1.2.7（SQLAlchemy包括用于SQLite，Postgresql，MySQL，Oracle，MS-SQL，Firebird，Sybase等的语言），如果要用其他数据库，本软件应该要做少许的调整
* 引入 pyrestful，[用法参考](https://github.com/rancavil/tornado-rest/tree/master/demos)

## 初始化特定版本的环境
> pipenv --python 3.7
## 进入环境
> pipenv shell
## 退出环境
> exit
## 其他命令
```

pipenv install -e git+https://github.com/leeyisoft/tornado-rest.git@master#egg=pyrestful

pipenv graph
```

# 项目启动
```
git clone https://gitee.com/leeyi/py_admin.git py_admin && cd py_admin
// 你首先执行以下这个脚本
sh ./init.sh
// 激活Python3虚拟环境
source vent/bin/activate
// 配置本地开发环境变量，然后启动
cp applications/configs/dev.py applications/configs/local.py

// 启动项目
python server.py

// 退出虚拟环境
deactivate
```

# init db
## datas/db.sql
只有表结构数据

## datas/db_data.sql
含默认的后台管理用户、默认菜单、默认配置数据

## db other
```
set global validate_password_policy=0;
create database db_cashloan default charset utf8 COLLATE utf8_general_ci;

CREATE USER user_cashloan IDENTIFIED BY 'eb27acWq#16E1';
GRANT ALL ON db_cashloan.* TO 'user_cashloan'@'%';
flush privileges;

// 只导出表结构
mysqldump --opt -d db_cashloan -u root -p > datas/db.sql
// alter database db_cashloan collate utf8_general_ci

set global log_bin_trust_function_creators = 1;
DELIMITER $$
--
-- 函数
--
CREATE DEFINER=`root`@`%` FUNCTION `currval` (`seq_name` VARCHAR(40)) RETURNS INT(11) SQL SECURITY INVOKER
BEGIN
DECLARE ret_value INTEGER;
SET ret_value=0;
SELECT `value` INTO ret_value
FROM sys_sequence
WHERE `key`=seq_name;
RETURN ret_value;
END$$

CREATE DEFINER=`root`@`%` FUNCTION `nextval` (`seq_name` VARCHAR(40), `incr` INT(11)) RETURNS INT(11) SQL SECURITY INVOKER
BEGIN
    UPDATE `sys_sequence` SET `value` = `value` + incr where `key`=seq_name;

    set @val = currval(seq_name);
    if @val = 0 then
        insert into sys_sequence (`key`, `value`) value (seq_name, incr);
        set @val = incr;
    end if;
    return @val;
END$$

DELIMITER ;

```
# features
* 后台配置添加
* 后台用户角色管理
* 基于角色的权限功能，后台用户管理
* 登录密码经过RSA加密，后台可配置是否开启该功能，后台可设置公钥私钥；
* 用户密码使用“ PBKDF2 + HMAC + SHA256”加密存储；
* 数据库密码经过AES加密，没有明文存储，进过AES加密的密码，格式 aes::: + ciphertext；
* 参考网站 [torngas](https://github.com/mqingyn/torngas)
* 其他特性继承自 tornado

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
openssl genrsa -out dev_privkey.pem 1024
// 从密钥中提取公钥
openssl rsa -pubout -in dev_privkey.pem -out dev_pubkey.pem
```

查询数据用 GET
添加/修改数据用 POST
删除数据用 DELETE

还有发放奖励功能需要做
用户上传头像的功能
### 依赖
```
(py3) ➜  paydayapi pip
```

### demo
```
        from applications.core.utils.encrypter import RSAEncrypter
        from applications.vsn1.services import ApiVsnService
        (code_, msg_, pubkeyser) = ApiVsnService.pubkeyser('1.0.0')
        plaintext = 'Ly123456'
        ciphertext = RSAEncrypter.encrypt(plaintext, pubkeyser)
        print('ciphertext ', ciphertext)
```

### IM 参考
http://test.guoshanchina.com/index.php
