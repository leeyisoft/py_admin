# 【生产构建】开始
# 由于 ADD . /data/py_admin 必须在项目根目录下面执行
# cd py_admin/
# docker build -f docker/Dockerfile . -t py_admin:v1.0.1
# docker run --name=py_admin -p 5080:5080 -v /Users/leeyi/workspace/py3/py_admin:/data/py_admin py_admin:v1.0.1

FROM python:3.8
MAINTAINER leeyi<leeyisoft@qq.com>
#工作目录
WORKDIR /data/py_admin

# 【生产构建】
ENV LIBDEPS_TOOLS automake autoconf libtool

RUN  echo 'deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster main contrib non-free \n \
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-updates main contrib non-free \n \
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-backports main contrib non-free \n \
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security buster/updates main contrib non-free \n' > /etc/apt/sources.list \
&& apt-get update && \
    apt install vim -y && \
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pyyaml && \
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple mysqlclient && \
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple sqlalchemy && \
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple redis && \
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple rsa && \
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pycryptodome && \
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pytz && \
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple python-dateutil && \
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple requests && \
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple raven && \
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pika && \
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pillow && \
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple sqlacodegen && \
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple qrcode && \
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple PyJWT && \
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple tornado && \
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pyyaml && \
    pip3 install git+https://gitee.com/leeyi/trest.git@master

# 设置默认启动的命令
CMD ["tail", "-f", "/dev/null"]
