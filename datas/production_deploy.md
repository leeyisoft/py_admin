[TOC]

supervisor 只支持python2；我的tornado在Python3.6下面开发；
所以需要在服务器上面同时按照多个python版本，默认Python版本为python2.7.15

# 安装 supervisor
```
sudo pip install supervisor
```
# 启动
```
supervisord -c /etc/supervisor/supervisord.conf
```
查看 supervisord 是否在运行：
```
ps aux | grep supervisord
```
# supervisorctl
```
supervisorctl

> status    # 查看程序状态
> stop tornadoes:*   # 关闭 tornadoes组 程序
> start tornadoes:*  # 启动 tornadoes组 程序
> restart tornadoes:*    # 重启 tornadoes组 程序
> update    ＃ 重启配置文件修改过的程序
```

# 配置 supervisor
运行supervisord服务的时候，需要指定supervisor配置文件，如果没有显示指定，默认在以下目录查找：
```
$CWD/supervisord.conf
$CWD/etc/supervisord.conf
/etc/supervisord.conf
/etc/supervisor/supervisord.conf (since Supervisor 3.3.0)
../etc/supervisord.conf (Relative to the executable)
../supervisord.conf (Relative to the executable)
```

可以通过运行echo_supervisord_conf程序生成supervisor的初始化配置文件，如下所示：
```
mkdir /etc/supervisor /etc/supervisor/include
echo_supervisord_conf > /etc/supervisor/supervisord.conf
```
vim 打开编辑supervisord.conf文件，修改
```
[include]
files = relative/directory/*.ini
```
为

```
[include]
files = /etc/include/supervisor/*.conf
```

## supervisor配置文件参数说明
```
[unix_http_server]
file=/tmp/supervisor.sock   ;UNIX socket 文件，supervisorctl 会使用
;chmod=0700                 ;socket文件的mode，默认是0700
;chown=nobody:nogroup       ;socket文件的owner，格式：uid:gid

;[inet_http_server]         ;HTTP服务器，提供web管理界面
;port=127.0.0.1:9001        ;Web管理后台运行的IP和端口，如果开放到公网，需要注意安全性
;username=user              ;登录管理后台的用户名
;password=123               ;登录管理后台的密码

...
;包含其它配置文件
[include]
files = relative/directory/*.ini    ;可以指定一个或多个以.ini结束的配置文件
```

## 在/etc/supervisor/include/中新建tornado管理的配置文件tornado.conf
```
[group:tornadoes]
programs=tornado-8001,tornado-8002,tornado-8003,tornado-8004

[program:tornado-8001]
command=/data/www/py_admin/py3/bin/python3.6 /data/www/py_admin/server.py --port=8001
directory=/data/www/py_admin
user=python
autorestart=true
redirect_stderr=true
stdout_logfile=/data/www/py_admin/logs/supervisor_info_tornado.log
loglevel=info

[program:tornado-8002]
command=/data/www/py_admin/py3/bin/python3.6 /data/www/py_admin/server.py --port=8002
directory=/data/www/py_admin
user=python
autorestart=true
redirect_stderr=true
stdout_logfile=/data/www/py_admin/logs/supervisor_info_tornado.log
loglevel=info

[program:tornado-8003]
command=/data/www/py_admin/py3/bin/python3.6 /data/www/py_admin/server.py --port=8003
directory=/data/www/py_admin
user=python
autorestart=true
redirect_stderr=true
stdout_logfile=/data/www/py_admin/logs/supervisor_info_tornado.log
loglevel=info

[program:tornado-8004]
command=/data/www/py_admin/py3/bin/python3.6 /data/www/py_admin/server.py --port=8004
directory=/data/www/py_admin
user=python
autorestart=true
redirect_stderr=true
stdout_logfile=/data/www/py_admin/logs/supervisor_info_tornado.log
loglevel=info
```

# nginx配置
```
upstream tornadoes {
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
    server 127.0.0.1:8004;
}

server {
    listen 80;
    server_name demo.leeyi.net;

    location ^~ /static {
        alias /data/www/py_admin/applications/statics;
        if ($query_string) {
            expires max;
        }
    }

    location / {
        proxy_pass_header Server;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Scheme $scheme;  # 协议 http https
        proxy_pass http://tornadoes;
    }
}

upstream supervisor9001{
    server 127.0.0.1:9001;
}

server{
    listen 80;
    server_name supervisor.leeyi.net;

    access_log /data/www/py_admin/logs/supervisor_access.log;
    error_log /data/www/py_admin/logs/supervisor_error.log;

    client_max_body_size 60M;
    client_body_buffer_size 512k;
        location / {
        proxy_pass_header Server;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Scheme $scheme;
        proxy_pass http://supervisor9001;
    }

    location ~ /\.ht {
        deny all;
    }
}

```
