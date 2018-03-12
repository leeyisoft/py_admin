#!/bin/bash
#安装依赖
pip install virtualenv -U
#安装环境
virtualenv --no-site-packages --python=python3.6 py3
#激活环境
source py3/bin/activate

# mysqlclient
echo "
tornado>=4.5.3
sqlalchemy
mysqlclient
rsa
pycrypto
pytz
redis
" > requirements.txt
pip install -r requirements.txt
