# -*- coding: utf-8 -*-

import sys
from readability import Document
import urllib.parse
#import urllib.request
import requests
import win32clipboard as wc
import win32con
import HtmlClipboard

def getHtmlToClipboard(dest_url):
    html_headers = {
            "Host": "note.youdao.com",
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
        #print(html_respone.text)
        html_text = html_respone.text

        html_doc = Document(html_text)
        HtmlClipboard.PutHtml(html_doc.summary())
        if HtmlClipboard.HasHtml():
            print('there is HTML!!')
            dirty_HTML = HtmlClipboard.GetHtml()

    except Exception:
        return False
    else:
        return True
    
url = 'https://blog.csdn.net/yl416306434/article/details/80569688'
getHtmlToClipboard(url)
