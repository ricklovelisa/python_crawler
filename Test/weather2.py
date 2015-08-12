#!/usr/bin/python
# encoding:utf8
# Copyright(c)2012 vsu@opensuse.org

from __future__ import print_function
import sys,os,MySQLdb
import urllib2,urllib,time,datetime,re,socket,cookielib,random
import json
from BeautifulSoup import BeautifulSoup
import multiprocessing
#import yaml

def makeCookie():
    # 代理 IP 使用
    # post cookie
    cookie=cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cookie)
    return cookie_support

def openPage(cityid,ip):
    #
    try:
        ipJson = {'http':'http://'+str(ip[0][0])+':'+str(ip[0][1])}
    except:
        ipJson = {}
    proxy_handler = urllib2.ProxyHandler(ipJson)
    opener=urllib2.build_opener(makeCookie(),urllib2.HTTPHandler,proxy_handler)
    urllib2.install_opener(opener)

    url = 'http://3g.tianqi.cn/getCfData.do?type=more'
    print(url)
    time.sleep(6)
    #url_referer= 'http://item.taobao.com/item.htm?spm=a230r.1.14.82.ReBj7G&id='+str(itemid)+'&ns=1&_u=mua6h780dc1'
    headers = {
        "GET":url,
        "Accept":"*/*",
        "Connection":"keep-alive",
        "DNT":"1",
        "Host":"3g.tianqi.cn",
        #"Referer":url_referer,
        "Cookie":"cityCode=01011410; cityName=%E6%AD%A6%E6%B1%89;",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.69 Safari/537.36"
        }
    
    req = urllib2.Request(url)
    for header in headers:
        req.add_header(header,headers[header])
    page = opener.open(req,None,10)
    return page
cityid = '01011410'
ip={}
print(openPage(cityid,ip).read())
