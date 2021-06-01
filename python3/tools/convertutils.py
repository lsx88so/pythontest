#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, re, os, copy, time
import string, base64, hashlib, uuid
from urllib import parse

#ALPHA = string.digits + string.ascii_uppercase + string.ascii_lowercase + '+' + '/'
#def self_base64_encode(num, base, alphabet=ALPHA):
#    """Encode a number in Base X
#
#    `num`: The number to encode
#    `base`: Base of number
#    `alphabet`: The alphabet to use for encoding
#    """
#    if (num == 0):
#        return alphabet[0]
#    arr = []
#    while num:
#        rem = num % base
#        num = num // base
#        arr.append(alphabet[rem])
#    arr.reverse()
#    return ''.join(arr)
#
#def self_base64_decode(string, base, alphabet=ALPHA):
#	"""Decode a Base X encoded string into the number
#
#	Arguments:
#	- `string`: The encoded string
#	- `base`: base of number
#	- `alphabet`: The alphabet to use for encoding
#	"""
#	strlen = len(string)
#	num = 0
#
#	idx = 0
#	for char in string:
#	    power = (strlen - (idx + 1))
#	    num += alphabet.index(char) * (base ** power)
#	    idx += 1
#
#	return num

#########instr binary
def convertBinary(instr):
    # calculate decimal number
    decimal = int(instr, 2)

    # calculate octal number
    octal = oct(decimal)[2:]

    # calculate hex number
    hexadec = hex(decimal)[2:].upper()

    return decimal, octal, hexadec

#########instr decimal
def convertDecimal(instr):
    # calculate binary number
    binary = bin(int(instr))[2:].zfill(8)

    # calculate octal number
    octal = oct(int(instr))[2:]

    # calculate hex number
    hexadec = hex(int(instr))[2:].upper()

    return binary, octal, hexadec

#########instr hex
def convertHex(instr):
    # calculate decimal number
    decimal = int(instr, 16)

    # calculate binary number
    binary = bin(decimal)[2:].zfill(8)

    # calculate octal number
    octal = oct(decimal)[2:]

    return decimal, binary, octal

#########instr octal
def convertOctal(instr):
    # calculate decimal number
    decimal = int(instr, 8)

    # calculate binary number
    binary = bin(decimal)[2:].zfill(8)

    # calculate hex number
    hexadec = hex(decimal)[2:].upper()

    return decimal, binary, hexadec

def base64_encode(instr):
    return base64.b64encode(instr.encode("utf-8")).decode("utf-8")

def base64_decode(instr):
    return base64.b64decode(instr).decode("utf-8")

def toTimestamp(instr):
    # 13位
    # int(round(time.time() * 1000))
    timestamp = int(time.time())
    flag = True

    if len(instr) > 0:
        regstr1 = r'^[0-9]{4}-[0-9]{1,2}-[0-9]{1,2} [0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}'
        regstr2 = r'^[0-9]{4}[0-9]{2}[0-9]{2}[0-9]{2}[0-9]{2}[0-9]{2}'
        if re.search(regstr1, instr):
            dt = time.strptime(instr, "%Y-%m-%d %H:%M:%S")
            timestamp = int(time.mktime(dt))
        elif re.search(regstr2, instr):
            dt = time.strptime(instr, "%Y%m%d%H%M%S")
            timestamp = int(time.mktime(dt))
        else:
            flag = False
    
    return flag, timestamp

def toTimeStr(instr):
    # 13位 or 10位
    dt = time.localtime()
    flag = True

    if len(instr) == 10:
        dt = time.localtime(int(instr))
    elif len(instr) == 13:
        dt = time.localtime(int(instr[0:10]))
    elif len(instr) > 0:
        flag = False
    
    timestr1 = time.strftime("%Y-%m-%d %H:%M:%S", dt)
    timestr2 = time.strftime("%Y%m%d%H%M%S", dt)
    return flag, timestr1, timestr2

def url_encode(instr):
    return parse.quote(instr, encoding="utf-8")

def url_decode(instr):
    return parse.unquote(instr, encoding="utf-8")

def calcSha1(instr):
    sha1 = hashlib.sha1()
    sha1.update(instr.encode("utf-8"))
    return sha1.hexdigest()
 
def calcMD5(instr):
    md5 = hashlib.md5()
    md5.update(instr.encode("utf-8"))
    return md5.hexdigest()

def hexToAsc(instr):
    return bytes.fromhex(instr).decode("utf-8")

def ascToHex(instr):
    return str(instr.encode("utf-8").hex())

def getuuid():
    return uuid.uuid4()

if __name__ == "__main__":
    #print(hexToAsc("616263"))
    #print(ascToHex("abc"))
    #print(calcSha1("admin"))
    #print(calcMD5("admin"))
    #instr = "http://hzsvn.asiainfo.com/svn/svnfiles/doc/project/JXmcc/04.其他项目/2018.计费网关"
    #instr1 = "http://hzsvn.asiainfo.com/svn/doc/VerisBilling_CMC_6.x/05%E4%BA%A7%E5%93%81%E6%89%8B%E5%86%8C/01%E8%9E%8D%E5%90%88%E8%AE%A1%E8%B4%B9/02%E7%BC%96%E8%AF%91%E6%89%8B%E5%86%8C/VerisBilling6.0%E6%93%8D%E4%BD%9C%E6%89%8B%E5%86%8C-%E7%BC%96%E8%AF%91-%E8%AE%A1%E8%B4%B9%E7%B3%BB%E7%BB%9F%E7%BC%96%E8%AF%91%E8%AF%B4%E6%98%8E(%E8%BE%BD%E5%AE%81)v1.0.doc"
    #print(url_encode(instr))
    #print(url_decode(instr1))
    #print(toTimeStr("1606927203"))
    #print(toTimestamp("2020-12-03 17:25:25"))
    #print(time.time())
    #print(convertDecimal(12))
    #print(base64_encode("Nsmdb*1"))
    #print(base64_decode("TnNtZGIqMQ=="))
    print(getuuid())
