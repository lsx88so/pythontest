#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar
from requests_toolbelt.multipart.encoder import MultipartEncoder
import random

if __name__ == "__main__":
    ##创建一个cookiejar对象，用来存储获取的cookie
    ##new_cookie = http.cookiejar.CookieJar()
    #new_cookie = http.cookiejar.MozillaCookieJar("cookie.txt")
    ##通过cookiejar对象来自定义一个handler
    #new_handler = urllib.request.HTTPCookieProcessor(new_cookie)
    ##设定一个opener
    #new_opener = urllib.request.build_opener(new_handler)
    ##设定URL
    #url1 = "https://note.youdao.com/yws/mapi/wcp?method=login&from=chrome&keyfrom=wcp&vn=2&vendor=ChromeStore"
    ##设定请求头字典
    #new_headers = {
    #    "Host": "note.youdao.com",
    #    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
    #    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    #    "Accept-Encoding": "gzip, deflate, br",
    #    "Accept-Language": "zh-CN,zh;q=0.9",
    #    "Content-Type": "application/x-www-form-urlencoded",
    #    "Origin": "https://note.youdao.com",
    #    "Connection": "keep-alive",
    #    "Referer": "https://note.youdao.com/yws/mapi/wcp?method=putfile&keyfrom=wcp&from=chrome&vendor=ChromeStore&vn=2",
    #}
    ##设定Post传参值
    #new_post = {
    #    "user":"11",
    #    "pass":"11"
    #}
    ##URL编码Post传参值
    #new_post_url = urllib.parse.urlencode(new_post).encode()
    ##生成请求request
    #new_request = urllib.request.Request(url=url1,headers=new_headers)
    ##发送请求
    #new_respone = new_opener.open(new_request,data=new_post_url)
    #print(new_respone.getcode())
    #for item in new_cookie:
    #    print('Name = %s' % item.name)
    #    print('Value = %s' % item.value)
    #
    #new_cookie.save(ignore_discard=True, ignore_expires=True)
    
    new_cookie = http.cookiejar.MozillaCookieJar()
    new_cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
    #通过cookiejar对象来自定义一个handler
    new_handler = urllib.request.HTTPCookieProcessor(new_cookie)
    #设定一个opener
    new_opener = urllib.request.build_opener(new_handler)
    #设定URL
    url1 = "https://note.youdao.com/yws/mapi/user?method=get"
    #设定请求头字典
    new_headers = {
        "Host": "note.youdao.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://note.youdao.com",
        "Connection": "keep-alive",
        "Referer": "https://note.youdao.com",
    }
    
    try:
        #生成请求request
        new_request = urllib.request.Request(url=url1,headers=new_headers)
        #发送请求
        new_respone = new_opener.open(new_request)
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.reason)
        #print(new_respone)
    else:
        print(new_respone.getcode())
    
    url2 = "https://note.youdao.com/yws/mapi/wcp?method=update&from=chrome&keyfrom=wcp&vn=2&vendor=ChromeStore"
    
    data = {
        "tl": "mpstat",
        "nb": "",
        "ourl": "false",
        "p": "/wcp1608971780340803",
        "bs": "ceshi",
        "len": "15",
        "src": "https://www.cnblogs.com/skyzy/p/9433487.html",
        "e": "false",
        "type": "MainBody",
        "from": "chrome",
        "ml": "true",
        "confirm": "true"
    }
    
    mdata = MultipartEncoder(fields=data,boundary='------' + str(random.randint(1e28, 1e29 - 1)))
    
    new_headers['Content-Type'] = mdata.content_type
    
    try:
        #生成请求request
        new_request = urllib.request.Request(url=url2,headers=new_headers)
        #发送请求
        new_respone = new_opener.open(new_request, data=mdata)
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.reason)
        #print(new_respone)
    else:
        print(new_respone.read().decode("utf-8"))
        