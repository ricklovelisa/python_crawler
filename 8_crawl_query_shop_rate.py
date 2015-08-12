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
import yaml

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
        queryTask = "SELECT uid_encrypted,shopid FROM %s.%s %s" % (database,shop_tbname,query_rule)
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

def openPage(uid_encrypted,shopid,ip):
    #
    try:
        ipJson = {'http':'http://'+str(ip[0][0])+':'+str(ip[0][1])}
    except:
        ipJson = {}
    proxy_handler = urllib2.ProxyHandler(ipJson)
    opener=urllib2.build_opener(makeCookie(),urllib2.HTTPHandler,proxy_handler)
##    keyword = urllib.quote(keyword.encode("utf8"))
    urllib2.install_opener(opener)
    time.sleep(2)
    url = 'http://rate.taobao.com/ShopService4C.htm?userNumId='+str(uid_encrypted)+'&ua&shopID='+str(shopid)+'&isB2C=true'
    print(url)
    url_referer= 'http://rate.taobao.com/user-rate-'+str(uid_encrypted)+'.htm'
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
        pageJsonData = re.findall('(\{.*\})',str(pageData))[0]
        is_banned = 0
        #
        # Load Json Data
        #
        jsonData = eval(pageJsonData)
    except Exception,e:
        print('#Banned!#')
        jsonData = ''
        is_banned = 1
    return [jsonData,is_banned]

def PhraseData(JsonData,uid_encrypted,shopid):
    data = []
    try:
        avgrefund_indval = JsonData['avgRefund']['indVal']
        avgrefund_localval = JsonData['avgRefund']['localVal']
        
        isbshop = JsonData['isBShop']

        punish_cpunishtimes = JsonData['punish']['cPunishTimes']
        punish_eyitimes = JsonData['punish']['eyiTimes']
        punish_indval = JsonData['punish']['indVal']
        punish_localval = JsonData['punish']['localVal']
        punish_miaoshutimes = JsonData['punish']['miaoshuTimes']
        punish_punishcount = JsonData['punish']['punishCount']
        punish_weibeitimes = JsonData['punish']['weibeiTimes']
        punish_xujiatimes = JsonData['punish']['xujiaTimes']

        ratrefund_indval = JsonData['ratRefund']['indVal']
        ratrefund_localval = JsonData['ratRefund']['localVal']
        ratrefund_merchqualitytimes = JsonData['ratRefund']['merchQualityTimes']
        ratrefund_merchreceivetimes = JsonData['ratRefund']['merchReceiveTimes']
        ratrefund_noreasontimes = JsonData['ratRefund']['noReasonTimes']
        ratrefund_refundcount = JsonData['ratRefund']['refundCount']

        complaints_aftersaletimes = JsonData['complaints']['afterSaleTimes']
        if complaints_aftersaletimes == '':
            complaints_aftersaletimes = 0
        complaints_complaintscount = JsonData['complaints']['complaintsCount']
        if complaints_complaintscount == '':
            complaints_complaintscount = 0
        complaints_disputrefundnum = JsonData['complaints']['disputRefundNum']
        if complaints_disputrefundnum == '':
            complaints_disputrefundnum = 0
        complaints_indval = JsonData['complaints']['indVal']
        if complaints_indval == '':
            complaints_indval = 0
        complaints_localval = JsonData['complaints']['localVal']
        if complaints_localval == '':
            complaints_localval = 0
        complaints_refundsumnum = JsonData['complaints']['refundSumNum']
        if complaints_refundsumnum == '':
            complaints_refundsumnum = 0
        complaints_refundsupportsellernum = JsonData['complaints']['refundSupportSellerNum']
        if complaints_refundsupportsellernum == '':
            complaints_refundsupportsellernum = 0
        complaints_taobaosolvenum = JsonData['complaints']['taobaoSolveNum']
        if complaints_taobaosolvenum == '':
            complaints_taobaosolvenum = 0
        complaints_taobaosolvepercent = JsonData['complaints']['taobaoSolvePercent']
        if complaints_taobaosolvepercent == '':
            complaints_taobaosolvepercent = 0
        complaints_violationtimes = JsonData['complaints']['violationTimes']
        if complaints_violationtimes == '':
            complaints_violationtimes = 0
        data = (getDate(),uid_encrypted,shopid,isbshop,avgrefund_indval,avgrefund_localval,punish_cpunishtimes,punish_eyitimes,punish_indval,punish_localval,punish_miaoshutimes,punish_punishcount,punish_weibeitimes,punish_xujiatimes,ratrefund_indval,ratrefund_localval,ratrefund_merchqualitytimes,ratrefund_merchreceivetimes,ratrefund_noreasontimes,ratrefund_refundcount,complaints_aftersaletimes,complaints_complaintscount,complaints_disputrefundnum,complaints_indval,complaints_localval,complaints_refundsumnum,complaints_refundsupportsellernum,complaints_taobaosolvenum,complaints_taobaosolvepercent,complaints_violationtimes)
        
    except Exception,e:
        print('Phrase Json Error:',e)
        data = (getDate(),uid_encrypted,shopid,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1)
    return data

def getSingleData(uid_encrypted,shopid):
    #Initial
    taskLife = 4
    data = []

    #getData
    updatetime = getDate()
    while taskLife >0:
        #ip = getIp('192.168.1.110',33060,'kettle','root','etc_crawl','ip_proxy')
        ip = {}
        try:
            page = openPage(uid_encrypted,shopid,ip)
            soup = soupPage(page,'gbk')
            pageData = reSoup(soup)
            pageJsonData = FindJson(pageData)

        except Exception,e:
            print('#2306:',e)
            pageJsonData = [0,1]
            print("TheShitIpProxy,replacing Now")
        if pageJsonData[1] == 1:
            taskLife = taskLife - 1
            #markBannedIp('192.168.1.110',33060,'kettle','root','etc_crawl','ip_proxy',ip)
        else:
            try:
                try:
                    fullData = PhraseData(pageJsonData[0],uid_encrypted,shopid)
                    data.append(fullData)
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
    uid_encrypted = info[6]
    shopid = info[7]
   
    itemdata = getSingleData(uid_encrypted,shopid)
    
    print("Wringting...",end='')
    print(itemdata)
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    ItemDataInsert = "INSERT INTO "+str(tbname)+" (updatetime,uid_encrypted,shopid,isbshop,avgrefund_indval,avgrefund_localval,punish_cpunishtimes,punish_eyitimes,punish_indval,punish_localval,punish_miaoshutimes,punish_punishcount,punish_weibeitimes,punish_xujiatimes,ratrefund_indval,ratrefund_localval,ratrefund_merchqualitytimes,ratrefund_merchreceivetimes,ratrefund_noreasontimes,ratrefund_refundcount,complaints_aftersaletimes,complaints_complaintscount,complaints_disputrefundnum,complaints_indval,complaints_localval,complaints_refundsumnum,complaints_refundsupportsellernum,complaints_taobaosolvenum,complaints_taobaosolvepercent,complaints_violationtimes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)  ON DUPLICATE KEY UPDATE updatetime = VALUES(updatetime),avgrefund_indval = VALUES(avgrefund_indval),avgrefund_localval = VALUES(avgrefund_localval),punish_cpunishtimes = VALUES(punish_cpunishtimes),punish_eyitimes = VALUES(punish_eyitimes),punish_indval = VALUES(punish_indval),punish_localval = VALUES(punish_localval),punish_miaoshutimes = VALUES(punish_miaoshutimes),punish_punishcount = VALUES(punish_punishcount),punish_weibeitimes = VALUES(punish_weibeitimes),punish_xujiatimes = VALUES(punish_xujiatimes),ratrefund_indval = VALUES(ratrefund_indval),ratrefund_localval = VALUES(ratrefund_localval),ratrefund_merchqualitytimes = VALUES(ratrefund_merchqualitytimes),ratrefund_merchreceivetimes = VALUES(ratrefund_merchreceivetimes),ratrefund_noreasontimes = VALUES(ratrefund_noreasontimes),ratrefund_refundcount = VALUES(ratrefund_refundcount),complaints_aftersaletimes = VALUES(complaints_aftersaletimes),complaints_complaintscount = VALUES(complaints_complaintscount),complaints_disputrefundnum = VALUES(complaints_disputrefundnum),complaints_indval = VALUES(complaints_indval),complaints_refundsumnum = VALUES(complaints_refundsumnum),complaints_refundsupportsellernum = VALUES(complaints_refundsupportsellernum),complaints_taobaosolvenum = VALUES(complaints_taobaosolvenum),complaints_taobaosolvepercent = VALUES(complaints_taobaosolvepercent),complaints_violationtimes = VALUES(complaints_violationtimes),isbshop = VALUES(isbshop),complaints_localval = VALUES(complaints_localval)"
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
def initialTable(host,port,user,password,database,tbname,sql_string):
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        dbconn.execute(sql_string % str(tbname))
        result = dbconn.fetchall()
        db.commit()
    except Exception,e:
        print(e)
    dbconn.close()
    return

def do_crawl_item(host,port,user,password,database,r_tbname,w_tbname,rule,sql_string):
    rule_json = json.loads(rule.encode('utf-8'))
    query_rule = rule_json["query_rule"]
    search_rule = rule_json["search_rule"]
    taskList = getSubTask(host,port,user,password,database,r_tbname,query_rule)
##    multiTask(taskList,host,user,password,database,item_tbname,keyword,search_rule)
    tasktemp = taskList
    initialTable(host,port,user,password,database,w_tbname,sql_string)
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
    ################################################################
    # Connection Database
    conf_file_path = sys.path[0]+"/conf/crawl.conf"
    conf_file = open(conf_file_path)
    conf = yaml.load(conf_file)
    
    host = conf['host']
    port = conf['port']
    user = conf['user']
    password = conf['password']
    database = conf['conf_database']
    tablename = conf['conf_table']

    # Read initial_sql_table
    sql_file_path = sys.path[0]+"/conf/sql.ini"
    sql_file = open(sql_file_path)
    sql = yaml.load(sql_file)

    # SQL Section
    shoplist_table = sql['raw_crawl_shop_list']

    ###############################################################
    
    try:
        itemstage = sys.argv[1]
    except:
        itemstage = 8
        
    projectlist = getTask(host,port,user,password,database,tablename,itemstage)
    for project in projectlist:
        do_crawl_item(host,port,user,password,project[0],project[1],project[2],project[3],shoplist_table)
if __name__ == "__main__":
    main()
    
