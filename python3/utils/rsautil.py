# -*- coding: utf-8 -*-

import rsa

class Encrypt(object):
    def __init__(self,e,m):
        self.e = e
        self.m = m
 
    def encrypt(self,message):
        mm = int(self.m, 16)
        ee = int(self.e, 16)
        rsa_pubkey = rsa.PublicKey(mm, ee)
        crypto = self._encrypt(message.encode(), rsa_pubkey)
        return crypto.hex()
 
    def _pad_for_encryption(self, message, target_length):
        message = message[::-1]
        max_msglength = target_length - 11
        msglength = len(message)
 
        padding = b''
        padding_length = target_length - msglength - 3
 
        for i in range(padding_length):
            padding += b'\x00'
 
        return b''.join([b'\x00\x00',padding,b'\x00',message])
 
    def _encrypt(self, message, pub_key):
        keylength = rsa.common.byte_size(pub_key.n)
        padded = self._pad_for_encryption(message, keylength)
 
        payload = rsa.transform.bytes2int(padded)
        encrypted = rsa.core.encrypt_int(payload, pub_key.e, pub_key.n)
        block = rsa.transform.int2bytes(encrypted, keylength)
 
        return block

def get_rsa_result(e,n,content):
    """
    根据 模量与指数 生成公钥，并利用公钥对内容 rsa 加密返回结果
    padding模式，结果每次会不一样
    :param e:指数
    :param n: 模量
    :param content:待加密字符串
    :return: 加密后结果
    """
    e = int(e, 16)
    n = int(n, 16)

    #pub_key = rsa.PublicKey(e=e, n=n)
    pub_key = rsa.PublicKey(n=n, e=e)
    m = rsa.encrypt(content.encode(),pub_key)
    return m.hex()

if __name__ == '__main__':
    e = "010001"
    m = "00858c46adbaacea74f8b62e9ff34a3d27fc1e10e8342be1b90e4522e5a8fedf261a1810b60616ffdd888652421bf4a70dbff19e81ab635847a6d301854cecace5"

    name = "admin"
    
    res = get_rsa_result(n=m, e=e, content=name)
    print("res : " + res)

    en = Encrypt(e,m)
    print(en.encrypt(name))



