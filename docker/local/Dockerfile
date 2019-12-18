# 【生产构建】开始
# 由于 ADD . /data/wwwroot/py_admin 必须在项目根目录下面执行
# docker build -f Dockerfile . -t py_admin_local:v1.0.1
# docker run --name=py_admin -p 5080:5080 -v /Users/leeyi/workspace/py3/py_admin:/data/wwwroot/py_admin py_admin_local:v1.0.1

FROM python:3.7.5
MAINTAINER leeyi<leeyisoft@qq.com>
WORKDIR /data/wwwroot/py_admin    #工作目录

# 【生产构建】
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple tornado && \
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
    pip3 install git+https://gitee.com/leeyi/trest.git@master

#【生产构建】暴露端口
EXPOSE 22 80 5080 9528

#设置默认启动的命令
CMD ["python", "/data/wwwroot/py_admin/server.py"]
