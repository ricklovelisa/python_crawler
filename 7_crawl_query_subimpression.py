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
        queryTask = "SELECT uid,itemid FROM %s.%s %s" % (database,shop_tbname,query_rule)
        dbconn.execute(queryTask)
        result = dbconn.fetchall()
        print(result)
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
        print(queryTask)
        dbconn.execute(queryTask)
        result = dbconn.fetchall()
        
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
        dbconn.execute(queryTask)
        result = dbconn.fetchall()
        db.commit()
    except Exception,e:
        print(e)
    dbconn.close()
    return

##def GenerateURL(uid,keyword,search_rule,inshops=0):
##    keyword = urllib.quote(keyword.encode("utf-8"))
##    url = 'http://s.taobao.com/search?inshopn=128&inshops=0&userids='+str(uid)+'&q='+keyword+search_rule+'&app=api&m=get_shop_auctions'
##
##    return url
def makeCookie():
    # 代理 IP 使用
    # post cookie
    cookie=cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cookie)
    return cookie_support

def openPage(uid,itemid,ip):
    #
    try:
        ipJson = {'http':'http://'+str(ip[0][0])+':'+str(ip[0][1])}
    except:
        ipJson = {}
    proxy_handler = urllib2.ProxyHandler(ipJson)
    opener=urllib2.build_opener(makeCookie(),urllib2.HTTPHandler,proxy_handler)
##    keyword = urllib.quote(keyword.encode("utf8"))
    urllib2.install_opener(opener)

    url = 'http://orate.alicdn.com/detailCommon.htm?callback=jsonp_reviews_list&userNumId='+str(uid)+'&auctionNumId='+str(itemid)+'&siteID=4'
    print(url)
    url_referer= 'http://item.taobao.com/item.htm?spm=a230r.1.14.82.ReBj7G&id='+str(itemid)+'&ns=1&_u=mua6h780dc1'
    headers = {
        "GET":url,
        "Accept":"*/*",
        "Connection":"keep-alive",
        "Host":"rate.taobao.com",
        "Referer":url_referer,
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.69 Safari/537.36"
        }
    
    req = urllib2.Request(url)
    for header in headers:
        req.add_header(header,headers[header])
    page = opener.open(req,None,10)
    
    return page

def soupPage(page,encode="utf8"):
    soup = BeautifulSoup(page,fromEncoding=encode)
    return soup

def reSoup(soup):
    pageData =  re.sub("&gt;",">",str(soup))
    pageData =  re.sub("&lt;","<",str(soup))
    pageData =  re.sub("</span>","",str(soup))
    pageData =  re.sub("<span class=\"H\">","",str(pageData))
    return pageData
def FindJson(pageData):
    try:
        pageJsonData = re.findall('jsonp_reviews_list\((.*)\)',str(pageData))[0]
        is_banned = 0
        jsonData = json.loads(pageJsonData)
    except Exception,e:
        print('#Banned!#')
        jsonData = ''
        is_banned = 1
    return [jsonData,is_banned]

def PhraseImpressData(impressData,uid,itemid):
    data = []

    try:
        impress = impressData["data"]["impress"] # No Need
        #print(impressData)
        if impress == []:
            print("itemid:",itemid)
    except Exception,e:
        print('Json Impression Data:',e)
        impress = []
    
    if impress == []:
        print("impress empty")
    else:
        for z in range(0,len(impress)):
            attribute = impress[z]['attribute']
            count = impress[z]['count']
            title = impress[z]['title']
            value = impress[z]['value']
            data.append((getDate(),uid,itemid,attribute,count,title,value))

    return data

def getSingleData(uid,itemid):
    #Initial
    taskLife = 4
    data = []

    #getData
    updatetime = getDate()
    while taskLife >0:
        ip = getIp('192.168.1.110',33060,'kettle','root','etc_crawl','ip_proxy')
        try:
            page = openPage(uid,itemid,ip)
            soup = soupPage(page,'gbk')
            pageData = reSoup(soup)
            pageJsonData = FindJson(pageData)
            print(pageJsonData)
        except Exception,e:
            print('#2306:',e)
            pageJsonData = [0,1]
            print("TheShitIpProxy,replacing Now")
        if pageJsonData[1] == 1:
            taskLife = taskLife - 1
            markBannedIp('192.168.1.110',33060,'kettle','root','etc_crawl','ip_proxy',ip)
        else:
            try:
                try:
                    fullData = PhraseImpressData(pageJsonData[0],uid,itemid)
                    data.extend(fullData)
                except Exception,e:
                    print(e)
                    print('This Item No Impression Data')
                taskLife = 0
            except:
                taskLife = taskLife - 1
                time.sleep(5)
    return data

def crawl_item_data(info):
    host = info[0]
    port = info[1]
    user = info[2]
    password = info[3]
    database = info[4]
    tbname = info[5]
    uid = info[6]
    itemid = info[7]
   
    itemdata = getSingleData(uid,itemid)
    
    print("Wringting...",end='')
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    ItemDataInsert = "INSERT IGNORE INTO "+str(tbname)+"(updatetime,uid,itemid,attribute,num,title,value) VALUES (%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE updatetime = VALUES(updatetime),`num`=VALUES(`num`)"
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
    initial_str = '''CREATE TABLE IF NOT EXISTS '''+str(tbname)+'''(`updatetime` date, `uid` BIGINT(20) NULL DEFAULT NULL, `itemid` BIGINT(20) NULL DEFAULT NULL, `attribute` VARCHAR(50) NULL DEFAULT NULL, `num` INT(11) NULL DEFAULT NULL, `title` VARCHAR(255) NULL DEFAULT NULL, `value` VARCHAR(10) NULL DEFAULT NULL, UNIQUE INDEX `uid_itemid_attribute` (`uid`, `itemid`, `attribute`), INDEX `num` (`num`), INDEX `title` (`title`), INDEX `value` (`value`)) COLLATE='utf8_general_ci' ENGINE=InnoDB;'''
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
##    multiTask(taskList,host,user,password,database,item_tbname,keyword,search_rule)
    tasktemp = taskList
    initialTable(host,port,user,password,database,w_tbname)
    for j in range(0,len(tasktemp)):
##    for j in range(0,1):
        print('task:',j,':')
        ptask = (host,port,user,password,database,w_tbname,tasktemp[j][0],tasktemp[j][1])
        crawl_item_data(ptask)

def writeStatus(host,port,user,password,database,shopid,pageinfo):
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
        itemstage = 7
        
    projectlist = getTask(host,port,user,password,database,tablename,itemstage)
    print(projectlist)
    for project in projectlist:
        
        do_crawl_item(host,port,user,password,project[0],project[1],project[2],project[3])
if __name__ == "__main__":
    main()
    
