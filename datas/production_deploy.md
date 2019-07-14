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

supervisorctl -c /etc/supervisor/supervisord.conf status

ln -s /data/wwwroot/py_admin/datas/supervisor_tornado.conf /etc/supervisor/include/spv_cashloan.conf

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
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;py_admin
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; 日志级别，有critical, error, warn, info, debug, trace, or blather等  默认为info

[program:py_admin]
directory=/data/wwwroot/py_admin
command=/data/wwwroot/py_admin/.venv/bin/python3 /data/wwwroot/py_admin/server.py --port=81%(process_num)02d
process_name=%(process_num)02d
numprocs=4
numprocs_start=1 ; 上面的process_num从1开始 默认从0 开始
autostart=true ; 在 supervisord 启动的时候也自动启动
startsecs=5 ; 启动 5 秒后没有异常退出，就当作已经正常启动了
autorestart=true ; 程序异常退出后自动重启
startretries=3 ; 启动失败自动重试次数，默认是 3
user=www ; 用哪个用户启动
redirect_stderr=true ; 把 stderr 重定向到 stdout，默认 false
stdout_logfile_maxbytes=20MB ; stdout 日志文件大小，默认 50MB
stdout_logfile_backups=20 ; stdout 日志文件备份数
; stdout 日志文件，需要注意当指定目录不存在时无法正常启动，所以需要手动创建目录（supervisord 会自动创建日志文件）
stdout_logfile=/data/wwwroot/py_admin/logs/cashloan_stdout.log

; 可以通过 environment 来添加需要的环境变量，一种常见的用法是修改 PYTHONPATH
; environment=PYTHONPATH=$PYTHONPATH:/path/to/somewhere

; 默认为 false，如果设置为 true，当进程收到 stop 信号时，会自动将该信号发给该进程的子进程。
; 如果这个配置项为 true，那么也隐含 killasgroup 为 true。
; 例如在 Debug 模式使用 Flask 时，Flask 不会将接收到的 stop 信号也传递给它的子进程，因此就需要设置这个配置项。
stopasgroup=true ; send stop signal to the UNIX process
; 默认为 false，如果设置为 true，当进程收到 kill 信号时，会自动将该信号发给该进程的子进程。
; 如果这个程序使用了 python 的 multiprocessing 时，就能自动停止它的子线程。
killasgroup=true ; SIGKILL the UNIX process group (def false)


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
