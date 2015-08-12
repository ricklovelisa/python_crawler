#!/usr/bin/python
# encoding:utf8
# All competitors
# Copyright(c)2012 vsu@opensuse.org

from __future__ import print_function
import sys,os,MySQLdb
import urllib2,urllib,time,re,socket,cookielib,random
import json
from BeautifulSoup import BeautifulSoup
import multiprocessing
#import yaml

def getDate():
    date=time.strftime("%Y-%m-%d",time.localtime())
    return date

def GenerateURL(pageno):
    url = 'http://ip.zdaye.com/?ip=&port=&dengji=&adr=&checktime=1%D0%A1%CA%B1%C4%DA&sleep=5%C3%EB%C4%DA&cunhuo=&px=%B0%B4%CF%EC%D3%A6%CA%B1%BC%E4%C9%FD%D0%F2&pageid='+str(pageno)
##    url = 'http://ip.zdaye.com/?ip=&port=&dengji=&adr=%CA%A1&checktime=&sleep=&cunhuo=&px=&pageid='+str(pageno)
    # 匿名URL
##    url = 'http://ip.zdaye.com/?ip=&port=&dengji=%C6%D5%C4%E4&adr=&checktime=30%B7%D6%D6%D3%C4%DA&sleep=3%C3%EB%C4%DA&cunhuo=&px=%B0%B4%B4%E6%BB%EE%CA%B1%BC%E4%C9%FD%D0%F2&pageid='+str(pageno)
##    url = 'http://ip.zdaye.com/?ip=&port=&dengji=&adr=&checktime=10%B7%D6%D6%D3%C4%DA&sleep=&cunhuo=&px=%B0%B4%CF%EC%D3%A6%CA%B1%BC%E4%C9%FD%D0%F2&pageid='+str(pageno)
    return url

def openPage(url):
    cookie=cookielib.CookieJar()
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    req=urllib2.Request(url)
    opener.add_handlers=['User-Agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)']
    urllib2.install_opener(opener)
    page=opener.open(req)
    return page

def soupPage(page,encode="utf8"):
    soup = BeautifulSoup(page,fromEncoding=encode)
    return soup

def reSoup(soup):
    pageData =  re.sub("&gt;",">",str(soup))
    pageData =  re.sub("&lt;","<",str(soup))
    pageData =  re.sub("</span>","",str(soup))
    pageData =  re.sub("<span class=\"H\">","",str(pageData))
    pageData =  re.sub("\r","",str(pageData))
    pageData =  re.sub("\n","",str(pageData))
    return pageData

def getData(pageno):
    data = []
    
    url = GenerateURL(pageno)
    page = openPage(url)
    updatetime = getDate()
    soup = soupPage(page)
    pageDataTemp = reSoup(soup)
    pageData = soupPage(pageDataTemp).findAll("table")[0]
    rows = pageData.findAll('tr')
    for tr in range(0,len(rows)):
        cols = rows[tr].findAll('td')
        print(cols)
        try:
            ip = re.findall('>(\d+.\d+.\d+.\d+)<',str(cols[0]))[0]
        except:
            ip = 'notthis'
        try:
            port = re.findall('>(\d+)<',str(cols[1]))[0]
        except:
            port = '-1'
        try:
            try:
                fen = int(re.findall('(\d+)分',str(cols[5]))[0])*60000
            except:
                fen = 0
            try:
                miao = int(re.findall('(\d+)秒',str(cols[5]))[0])*1000
            except:
                miao = 0
            try:
                haomiao = int(re.findall('(\d+)毫秒',str(cols[5]))[0])
            except:
                haomiao = 0
            weight = fen+miao+haomiao
        except:
            weight = 1000
        if ip == 'notthis':
            print("OK;",end='')
        else:
            datatemp = (getDate(),ip,port,weight)
            data.append(datatemp)

    return data

def crawl_item_data(info):
    host = info[0]
    port = info[1]
    user = info[2]
    password = info[3]
    database = info[4]
    tbname = info[5]

    itemdata = []
    for i in range(1,15):
        print(i,'.',end='')
        try:
            datatemp = getData(i)
            itemdata.extend(datatemp)
        except Exception,e:
            print(e)
            print("no data anymore")
    
    if itemdata == []:
        print("BigError")
    else:
        db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
        dbconn=db.cursor()
        
        ItemDataInsert = "INSERT INTO "+str(tbname)+" (updatetime,ipaddress,ipport,privige,is_valid) VALUES (%s,%s,%s,%s,'1') ON DUPLICATE KEY UPDATE updatetime =VALUES(updatetime),privige = VALUES(privige),is_valid = VALUES(is_valid)"
        
        try:
            dbconn.executemany(ItemDataInsert,itemdata)
            db.commit()
        except Exception,e:
            print(e)
        db.close()
def initialTable(host,port,user,password,database,tbname):
    initial_str = '''CREATE TABLE IF NOT EXISTS '''+str(tbname)+''' (	`updatetime` DATE NULL,	`ipaddress` VARCHAR(50) NOT NULL DEFAULT '0',	`ipport` INT(10) NOT NULL DEFAULT '0',	`privige` INT(11) NOT NULL DEFAULT '0',	`is_valid` INT(11) NOT NULL DEFAULT '1', UNIQUE INDEX `ipaddress_ipport` (`ipaddress`, `ipport`),	INDEX `updatetime` (`updatetime`),	INDEX `privige` (`privige`), INDEX `is_valid` (`is_valid`) ) COLLATE='utf8_general_ci' ENGINE=InnoDB'''
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        dbconn.execute(initial_str)
        result = dbconn.fetchall()
        db.commit()
    except Exception,e:
        print(e)
    dbconn.close()
    return 
def main():
##    conf_file = open('/etc/crawl/item_conf')
##    conf = yaml.load(conf_file)
##    host = conf['host']
##    user = conf['user']
##    password = conf['password']
##    database = conf['database']
##    tablename = conf['tablename']
    host = '192.168.1.110'
    port = 33060
    user = 'kettle'
    password = 'root'
    database = 'etc_crawl'
    tablename = 'ip_proxy'
    task = (host,port,user,password,database,tablename)
    initialTable(host,port,user,password,database,tablename)
    crawl_item_data(task)
    
if __name__ == "__main__":
    main()
    
