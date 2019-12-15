# 【生产构建】开始
FROM docker.io/centos
MAINTAINER leeyi<leeyisoft@qq.com>
WORKDIR /data/wwwroot/py_admin    #工作目录

# 【生产构建】构建sshd服务 openssh-server*
# RUN yum -y update
RUN yum -y install zlib zlib-devel bzip2 bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc* make wget kernel-devel libffi-devel git && yum clean all

# 【生产构建】下载Python3.7.5
RUN wget https://www.python.org/ftp/python/3.7.5/Python-3.7.5.tar.xz
#ADD Python-3.7.5.tar.xz /Python-3.7.5.tar.xz
RUN tar Jvxf Python-3.7.5.tar.xz && cd  ./Python-3.7.5 && ./configure --prefix=/usr/local/python3  && make && make install && ln -s /usr/local/python3/bin/python3 /usr/bin/python && ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3 && pip3 install pipenv && cd ../ && rm -rf Python-3.7.5 && rm -rf Python-3.7.5.tar.xz && ln -s /usr/local/python3/bin/pipenv /usr/bin/pipenv

# 【生产构建】
RUN mkdir -p /data /data/logs /data/wwwroot && cd /data/wwwroot/ && git clone https://gitee.com/leeyi/py_admin.git py_admin && cd py_admin && mkdir -p .venv && pipenv install --skip-lock && echo 'TREST_ENV : local' > .env

VOLUME ['/data/wwwroot/py_admin', '/data/wwwroot/vue_py_admin']
# 【生产构建】删除多余包

#【生产构建】暴露端口
EXPOSE 22
EXPOSE 80
EXPOSE 5080
EXPOSE 9528

#设置默认启动的命令
CMD ["docker_init", "cd /data/wwwroot/py_admin && pipenv shell && python server.py"]
