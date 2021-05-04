#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, re, os, copy, datetime
#from readability import Document
#import richxerox
import urllib.parse
import requests

def getHtml(dest_url):
    html_headers = {
            #"Host": "note.youdao.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            #"Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive"
        }
    try:
        html_host = urllib.parse.urlparse(dest_url)
        html_headers["Host"] = html_host.netloc
        # urllib不会自动解压缩
        #html_request = urllib.request.Request(url, headers=html_headers)
        #html_respone = urllib.request.urlopen(html_request)
        #html_respone = urllib.request.urlopen(dest_url)
        #print(html_respone.read().decode("utf-8"))
        #html_text = html_respone.read().decode("utf-8")

        html_respone = requests.get(dest_url, headers=html_headers)
        print(html_respone)
        #html_text = html_respone.text
    except Exception:
        return False
    else:
        return True

def getMachineInt(strBin):
    '''
    补码的反向计算，返回机器码对应的int值，失败返回None
    '''
    #数字减1
    intNum = int(strBin, base=2) - 1
    # 返回串开头为0b
    strBin = bin(intNum)[2:]
    # 取反
    #reserveStr = reverse(strBin)
    binary_out = list(strBin)
    for epoch,i in enumerate(strBin):
        if i == "0":
            binary_out[epoch] = "1"
        else:
            binary_out[epoch] = "0"
    reserveStr = "".join(binary_out)
    resInt = -int(reserveStr,2)

    return resInt

print(getMachineInt("1111001110110111001100110011011100110011011101111011001100101100"))
#print(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))
#
#a = '01-24~01-30'
#b = '01-19,01-23'
#c = '01-24~01-30, 01-19,01-23'
#
#print(a.split(','))
#print(a.split(',')[0].split('~'))
#
#c = [1,2]
#a = [1,2,3,c]
#b = a[3]
#d = copy.copy(a)
#print(a,b,c,d)
#b[1] = 1
#print(a,b,c,d)
#c[1] = 3
#print(a,b,c,d)
#x = 1
#y = x
#print(x,y)
#y = 3
#print(x,y)

#url = 'https://blog.csdn.net/qq_38410730/article/details/80500920'
#
#html = urllib.request.urlopen(url).read().decode('utf-8')
##print(html)
#doc = Document(html)
#print(doc.title())
#print(doc.summary())
#richxerox.pasteboard.set_contents(html=doc.summary())

#url = 'https://www.hackthebox.eu/api/invite/generate'
#getHtml(url)
