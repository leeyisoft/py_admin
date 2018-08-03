#!/bin/bash
#安装依赖
pip install virtualenv -U
#安装环境
virtualenv --no-site-packages --python=python3.6 py3
#激活环境
source py3/bin/activate

echo "
tornado>=5.0.2
mysqlclient
sqlalchemy
rsa
pycrypto
pytz
pillow
python-dateutil
qrcode
websocket-client
" > requirements.txt
pip install -r requirements.txt
