#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import rsa
from Crypto.Cipher import AES

from .settings_manager import settings


class RSAEncrypter(object):
    """RSA加密解密
    参考 https://stuvel.eu/python-rsa-doc/index.html
    对应JavaScript版本参考 https://github.com/travist/jsencrypt
    [description]
    """
    @classmethod
    def encrypt(cls, plaintext, file):
        #明文编码格式
        content = plaintext.encode('utf-8')
        with open(file) as publicfile:
            keydata = publicfile.read()

        pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(keydata)
        #公钥加密
        crypto = rsa.encrypt(content, pubkey)
        return base64.b64encode(crypto).decode('utf-8')

    @classmethod
    def decrypt(cls, ciphertext, file):
        ciphertext = base64.b64decode(ciphertext)
        with open(file) as privatefile:
            keydata = privatefile.read()

        privkey = rsa.PrivateKey.load_pkcs1(keydata, format='PEM')
        con = rsa.decrypt(ciphertext, privkey)
        return con.decode('utf-8')

class AESEncrypter(object):
    def __init__(self, key, iv=None):
        self.key = key
        self.iv = iv if iv else bytes(key[0:16], 'utf-8')

    def _pad(self, text):
        text_length = len(text)
        padding_len = AES.block_size - int(text_length % AES.block_size)
        if padding_len == 0:
            padding_len = AES.block_size

        return text + chr(padding_len) * padding_len

    def _unpad(self, text):
        pad = ord(text[-1])
        return text[:-pad]

    def encrypt( self, raw):
        raw = self._pad(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        encrypted = cipher.encrypt(raw)
        return base64.b64encode(encrypted).decode('utf-8')

    def decrypt( self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        decrypted = cipher.decrypt(enc)
        return self._unpad(decrypted.decode('utf-8'))


def aes_decrypt(ciphertext, secret=None):
    secret = settings.default_aes_secret if secret is None else secret
    cipher = AESEncrypter(secret)
    return cipher.decrypt(ciphertext[6:]) if ciphertext[0:6]=='aes:::' else ciphertext

def aes_encrypt(plaintext, secret=None):
    secret = settings.default_aes_secret if secret is None else secret
    cipher = AESEncrypter(secret)
    encrypted = cipher.encrypt(plaintext)
    return 'aes:::%s' % encrypted

if __name__ == "__main__":
    try:
        # for RSA test
        ciphertext = 'Qa2EU2EF4Eq4w75TnA1IUw+ir9l/nSdW3pMV+a6FkzV9bld259DxM1M4RxYkpPaVXhQFol04yFjuxzkRg12e76i6pkDM1itQSOy5hwmrud5PQvfnBf7OmHpOpS6oh6OQo72CA0LEzas+OANmRXKfn5CMN14GsmfWAn/F6j4Azhs='
        public_key = '/Users/leeyi/chanrongdai/eam/py_admin/datas/public.pem'
        private_key = '/Users/leeyi/chanrongdai/eam/py_admin/datas/private.pem'

        ciphertext = RSAEncrypter.encrypt('admin888中国', public_key)
        print("ciphertext: ", ciphertext)
        plaintext = RSAEncrypter.decrypt(ciphertext, private_key)
        print("plaintext: ", type(plaintext))
        print("plaintext: ", plaintext)


        # for AES test
        key = 'abc20304050607081q2w3e4r*1K|j!ta'
        cipher = AESEncrypter(key)

        plaintext = '542#1504'
        encrypted = cipher.encrypt(plaintext)
        print('Encrypted: %s' % encrypted)
        ciphertext = 'EPLtushldq9E1U8vG/sL3g=='
        assert encrypted == ciphertext

        plaintext = '542#1504你好'
        encrypted = '+YGDvnakKi77SBD6GXmThw=='
        decrypted = cipher.decrypt(encrypted)
        print('Decrypted: %s' % decrypted)
        assert decrypted == plaintext

    except KeyboardInterrupt:
        sys.exit(0)
