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
def unixTime(timestr):
    value = time.gmtime(timestr)
    format = '%Y-%m-%d %H:%M:%S'
    return time.strftime(format,value)

def getTask(host,port,user,password,database,tablename,itemstage = 1):
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        queryTask = "SELECT `dbname`,r_table,w_table,rule FROM %s.%s WHERE taskid = '%s'"
        print(queryTask % (database,tablename,itemstage))
        dbconn.execute(queryTask % (database,tablename,itemstage))
        
        result = dbconn.fetchall()
        db.commit()
    except:
        result = []
    dbconn.close()
    return result

def getSubTask(host,port,user,password,database,shop_tbname,query_rule):
    # keyword,pagenumber = 1,ratesum = "",location = "",cat = "",brand = "",ppath = "",sort = "sale-desc")
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        queryTask = "SELECT itemid FROM %s.%s %s" % (database,shop_tbname,query_rule)
        dbconn.execute(queryTask)
        result = dbconn.fetchall()
        db.commit()
    except Exception,e:
        try:
            queryTask = "SELECT itemid FROM %s.%s %s" % (database,shop_tbname,query_rule)
            dbconn.execute(queryTask)
            result = dbconn.fetchall()
            db.commit()
        except Exception,e:
            print(e)
            result = []
    dbconn.close()
    return result
def getIp(host,port,user,password,database,tbname):
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        queryTask = "SELECT ipaddress,ipport FROM %s.%s where is_valid = '1' ORDER BY privige ASC limit 1" % (database,tbname)
        dbconn.execute(queryTask)
        result = dbconn.fetchall()
        db.commit()
        
    except Exception,e:
        print(e)
        result = []
    dbconn.close()
    return result

def markBannedIp(host,port,user,password,database,tbname,ip):
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        queryTask = "UPDATE %s.%s SET is_valid = '0' WHERE ipaddress = '%s' and ipport = '%s'" % (database,tbname,ip[0][0],ip[0][1])
        print(queryTask)
        dbconn.execute(queryTask)
        result = dbconn.fetchall()
        db.commit()
    except Exception,e:
        print(e)
    dbconn.close()
    return

def makeCookie():
    # 生成 Cookie 支持
    cookie=cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cookie)
    return cookie_support

def openPage(itemid,ip):
    # 使用代理 IP 打开页面
    ##    keyword = urllib.quote(keyword.encode("utf8"))
    ipJson =  {'http':'http://'+str(ip[0][0])+':'+str(ip[0][1])}
    ##ipJson={}
    proxy_handler = urllib2.ProxyHandler(ipJson)
    opener=urllib2.build_opener(makeCookie(),urllib2.HTTPHandler,proxy_handler)
    urllib2.install_opener(opener)
    # 生成 URL
    url = 'http://item.taobao.com/item.htm?id='+str(itemid)
    url_referer= 'http://item.taobao.com/item.htm?id='+str(itemid)
    # 加载 URL 头
    headers = {
        "GET":url,
        "Accept":"*/*",
        "Connection":"keep-alive",
        "Host":"item.taobao.com",
        "Referer":url_referer,
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.69 Safari/537.36"
        }
    
    req = urllib2.Request(url)
    for header in headers:
        req.add_header(header,headers[header])
    page = opener.open(req,None,20)
    ##print(page.read())
    
    return page

def soupPage(page,encode="utf8"):
    soup = BeautifulSoup(page,fromEncoding=encode)
    return soup

def reSoup(soup):
    pageData = re.sub("<\\/em>","</em>",str(soup))
    pageData = re.sub("\s\s+","\s",str(pageData))
    pageData = re.sub(r'\r|\n|\t',"",str(pageData))
    pageData =  re.sub("&gt;",">",str(pageData))
    pageData =  re.sub("&lt;","<",str(pageData))
    pageData =  re.sub("</span>","",str(pageData))
    pageData =  re.sub("<span class=\"H\">","",str(pageData))
    return pageData

def FindJson(pageData):
    try:
        is_banned = 0
        
        try:
            pageJsonData = soupPage(pageData).findAll(attrs={"class":"attributes"})[0]
        except:
            pageJsonDat = ''
        try:
            sign = re.findall('sign=([a-z0-9]+).',str(pageData))[0]
        except Exception,e:
            print("FindSign:",e)
            is_banned = 1
        
    except Exception,e:
        print('#Banned!#')
        print(pageData.encode('utf8'))
        pageJsonData = ''
        sign = ''
        is_banned = 1
    return [pageJsonData,sign,is_banned]

def getSingleData(itemid):
    #Initial
    taskLife = 4
    sleep = 1
    data = []
    spuData = []
    #getData
    updatetime = getDate()
    while taskLife >0:
        ip = getIp('192.168.1.110','kettle','root','etc_crawl','ip_proxy')
        try:
            page = openPage(itemid,ip)
            soup = soupPage(page,'gbk')
            pageDataTemp = reSoup(soup)
            pageJsonData = FindJson(pageDataTemp)

            sku = ''
            try:
                rows = pageJsonData[0].findAll('li')
            except:
                rows = []
            for x in rows:
                d = re.findall('>(.*)<',str(x))[0]
                sku = sku+ d +';'
            sign = pageJsonData[1]
        except Exception,e:
            print("PageSoure:",e)
            ipOk = 0
            pageJsonData = [0,0,1]
            print("TheShitIpProxy,replacing Now")
        if pageJsonData[2] == 1:
            
            taskLife = taskLife - 1

            print("Banned 1")
            print(ipOk,":",sleep)
            markBannedIp('192.168.1.110','kettle','root','etc_crawl','ip_proxy',ip)

        else:
            data = (updatetime,itemid,sku,sign)
            taskLife = 0
            
    return data


def getData(itemid):
    data = []
    print('itemid:',itemid,'F:',end='')
    newdata = getSingleData(itemid)
    data.append(newdata)
    return data

def crawl_item_data(info):
    host = info[0]
    port = info[1]
    user = info[2]
    password = info[3]
    database = info[4]
    tbname = info[5]
    itemid = info[6]

   
    itemdata = getData(itemid)
    
    print("Wringting...",end='')
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    ItemDataInsert = "INSERT INTO "+str(tbname)+"(updatetime,itemid,sku,`sign`) VALUES (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE sku = VALUES(sku), `sign` = VALUES(`sign`)"
    dbconn.executemany(ItemDataInsert,itemdata)
    db.commit()
    db.close()
    print("Writen")
    
def multiTask(tasklist,host,port,user,password,database,item_tbname,keyword,search_rule):
    for i in range(0,len(tasklist),20):
        tasktemp = tasklist[i:i+20]
        job=[]
        if i <20:
            print(getDate()+":"+"Begin_Project:"+str(len(tasklist)))
        print(getDate()+":"+"Process:"+str(round((i+10)*100/len(tasklist),0))+"%")
        for j in range(0,len(tasktemp)):
            ptask = (host,port,user,password,database,w_tbname,tasktemp[j][0],tasktemp[j][1])
            # info
            p = multiprocessing.Process(target = crawl_item_data,args=(ptask,))
            p.start()
            job.append(p)
        for p in job:
            p.join()
def initialTable(host,port,user,password,database,tbname):
    initial_str = '''CREATE TABLE IF NOT EXISTS '''+str(tbname)+''' ( updatetime date, itemid bigint, sku text, `sign` varchar(255),UNIQUE INDEX `itemid` (`itemid`)) COLLATE='utf8_general_ci' ENGINE=InnoDB;'''
    print(initial_str)
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


def do_crawl_item(host,port,user,password,database,r_tbname,w_tbname,rule):
    rule_json = json.loads(rule.encode('utf-8'))
    query_rule = rule_json["query_rule"]
    search_rule = rule_json["search_rule"]
    taskList = getSubTask(host,port,user,password,database,r_tbname,query_rule)
#### Uncomment here for multi running task
##    multiTask(taskList,host,user,password,database,item_tbname,keyword,search_rule)
    tasktemp = taskList
    initialTable(host,port,user,password,database,w_tbname)
    for j in range(0,len(taskList)):
        time.sleep(4)
        ptask = (host,port,user,password,database,w_tbname,tasktemp[j][0])
        crawl_item_data(ptask)

def writeStatus(host,user,password,database,shopid,pageinfo):
    '''
    Log and current job status sent
    '''
    # keyword,pagenumber = 1,ratesum = "",location = "",cat = "",brand = "",ppath = "",sort = "sale-desc")
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        writeStatus = "REPLACE INTO pool_error_crawl_shop_item (updatetime,shopid,msg) VALUES (%s,%s,%s) "
        dbconn.execute(writeStatus)
        db.commit()
    except:
        result = []
    dbconn.close()
    return


def main():
    # Connection Database
    conf_file_path = sys.path[0]+"/crawl.conf"
    conf_file = open(conf_file_path)
    conf = yaml.load(conf_file)
    
    host = conf['host']
    port = conf['port']
    user = conf['user']
    password = conf['password']
    conf_database = conf['database']
    conf_table = conf['tablename']
    
    try:
        itemstage = sys.argv[1]
    except:
        itemstage = 3
        
    projectlist = getTask(host,port,user,password,database,tablename,itemstage)
    print(projectlist)
    for project in projectlist:
        do_crawl_item(host,port,user,password,project[0],project[1],project[2],project[3])
if __name__ == "__main__":
    main()
##    itemid = '38904275326'
##    uid = ''
##    rule = ''
##    x = getData(itemid)
##    print(x)
    
    
