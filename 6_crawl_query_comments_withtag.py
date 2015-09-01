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

def getRankid(rank):
    if rank < 4: rankid = 0
    elif rank < 11: rankid = 2
    elif rank < 41: rankid = 3
    elif rank < 91: rankid = 4
    elif rank < 151: rankid = 5
    elif rank < 251: rankid = 6
    elif rank < 501: rankid = 7
    elif rank < 1001: rankid = 8
    elif rank < 2001: rankid = 9
    elif rank < 5001: rankid = 10
    elif rank < 10001: rankid = 11
    elif rank < 20001: rankid = 12
    elif rank < 50001: rankid = 13
    elif rank < 100001: rankid = 14
    elif rank < 200001: rankid = 15
    elif rank < 500001: rankid = 16
    elif rank < 1000001: rankid = 17
    elif rank < 2000001: rankid = 18
    elif rank < 5000001: rankid = 19
    else : rankid = 20
    return rankid

def getDate():
    date=time.strftime("%Y-%m-%d",time.localtime())
    return date
def unixTime(timestr):
    value = time.gmtime(timestr)
    format = '%Y-%m-%d %H:%M:%S'
    return time.strftime(format,value)

def getTask(host,port,user,password,database,tablename,taskid = 1):
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        queryTask = "SELECT `dbname`,r_table,w_table,rule FROM %s.%s WHERE taskid = '%s'"
        dbconn.execute(queryTask % (database,tablename,taskid))
        result = dbconn.fetchall()
        db.commit()
    except:
        print(rule)
        result = []
    dbconn.close()
    return result

def getSubTask(host,port,user,password,database,shop_tbname,query_rule):
    # keyword,pagenumber = 1,ratesum = "",location = "",cat = "",brand = "",ppath = "",sort = "sale-desc")
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        queryTask = "SELECT uid,itemid,attribute FROM %s.%s %s" % (database,shop_tbname,query_rule)
        dbconn.execute(queryTask)
        result = dbconn.fetchall()
        db.commit()
    except Exception,e:
        try:
            queryTask = "SELECT uid,itemid,'' FROM %s.%s %s" % (database,shop_tbname,query_rule)
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

def openPage(uid,itemid,rule,pageno,ip):
    # 使用代理 IP 打开页面
    ##    keyword = urllib.quote(keyword.encode("utf8"))
    #ipJson =  {'http':'http://'+str(ip[0][0])+':'+str(ip[0][1])}
    ipJson = {}
    proxy_handler = urllib2.ProxyHandler(ipJson)
    opener=urllib2.build_opener(makeCookie(),urllib2.HTTPHandler,proxy_handler)
    urllib2.install_opener(opener)
    # 生成 URL
    time.sleep(2)
    url = 'http://rate.taobao.com/feedRateList.htm?callback=jsonp_reviews_list&userNumId='+str(uid)+'&auctionNumId='+str(itemid)+'&siteID=7&currentPageNum='+str(pageno)+'&attribute='+rule+'&ua='
    url_referer= 'http://item.taobao.com/item.htm?spm=a230r.1.14.82.ReBj7G&id='+str(itemid)+'&ns=1&_u=mua6h780dc1'
    # 加载 URL 头
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
    page = opener.open(req,None,20)
    
    return page

def soupPage(page,encode="utf8"):
    soup = BeautifulSoup(page,fromEncoding=encode)
    return soup

def reSoup(soup):
    pageData = re.sub("<\\/em>","</em>",str(soup))
    pageData =  re.sub("&gt;",">",str(soup))
    pageData =  re.sub("&lt;","<",str(soup))
    pageData =  re.sub("</span>","",str(soup))
    pageData =  re.sub("<span class=\"H\">","",str(pageData))
    return pageData


def PhraseCommentData(comments,seller_id,rule):
    data = []
    spuData = []
    
    for i in range(0,len(comments)):
        auction = comments[i]["auction"] # No Need
        try:
            itemid = auction['aucNumId']
            pic_url = auction['auctionPic']
            sku = re.sub('&nbsp','',auction['sku'])
            title = auction['title']
        except:
            itemid = ''
            pic_url = ''
            sku = ''
            title =''
        award = comments[i]['award']
        buyAmount = comments[i]["buyAmount"]
        
        content = reSoup(comments[i]["content"].encode('utf8')) # AppendList
        try:
            updatetime = re.sub('日','',re.sub('年','-',re.sub('月','-',comments[i]["date"].encode('utf8'))))
            newupdatetime = time.strptime(updatetime,'%Y-%m-%d %H:%M')
            updatetime_date = time.strftime('%Y-%m-%d',newupdatetime)
            updatetime_hour = time.strftime('%H%M',newupdatetime)
        except Exception,e:
            print("Data:",e)
            print(type(comments[i]["date"]))
            print(comments[i]["date"])
        dayAfterConfirm = comments[i]["dayAfterConfirm"] # AppendList
        enableSNS = comments[i]["enableSNS"]
        datafrom = comments[i]["from"]
        lastModifyFrom = comments[i]["lastModifyFrom"]
        try:
            payTime = str(comments[i]["payTime"]['time'])[0:10]
            payTime = unixTime(int(payTime))
        except Exception,e:
            payTime = ''
        photos = comments[i]["photos"] # AppendList
        if photos == []:
            photos = ''
        else:
            try:
                photos = str(photos).encode('utf8')
            except Exception,e:
                print("photo:",e)
##            photos = re.sub(',','\,',str(photos))
        promotionType = comments[i]["promotionType"]
        propertiesAvg = comments[i]["propertiesAvg"]
        rate = comments[i]["rate"]
        rateId = comments[i]["rateId"]
        raterType = comments[i]["raterType"]
        showCuIcon = comments[i]["showCuIcon"]
        showDepositIcon = comments[i]["showDepositIcon"]
        spuRatting = comments[i]["spuRatting"]
        if spuRatting == []:
            spu_string = ''
        else:
            spu_string = ''
            for z in range(0,len(spuRatting)):
                spu_name = spuRatting[z]['name']
                spu_value = spuRatting[z]['value']
                spu_desc = spuRatting[z]['desc']
                spuData.append((spu_value,spu_name,spu_desc))
                spu_string = spu_value+';'+spu_string

        status = comments[i]["status"]
        tag = comments[i]["tag"]
        useful = comments[i]["useful"]
        user = comments[i]["user"] # No Need
        try:
            anony = user["anony"]
            uid = user["userId"]
            buyernick = user["nick"]
            rank = user["rank"]
            try:
                 uid_encrypted = re.findall('http://my.taobao.com/(.*)',user["nickUrl"])[0]
            except:
                 uid_encrypted = ''
        except:
            anony = 'nodata'
            buyernick = ''
            uid_encrypted = ''
            uid = ''
            rank = -1
        if rank <> -1:
            rankid = getRankid(rank)
        else:
            rankid = -1
        appendId = 0
        datatemp = (seller_id,itemid,pic_url,sku,title,award,buyAmount,updatetime,updatetime_date,updatetime_hour,dayAfterConfirm,enableSNS,datafrom,lastModifyFrom,payTime,promotionType,propertiesAvg,rate,rateId,raterType,showCuIcon,showDepositIcon,spu_string,status,tag,useful,anony,uid,buyernick,rankid,rank,uid_encrypted,appendId,content,photos,rule)
        data.append(datatemp)
        appendList = comments[i]["appendList"]
        for x in range(0,len(appendList)):
            NewappendId = appendList[x]['appendId']
            Newcontent = reSoup(appendList[x ]['content'].encode('utf8'))
            NewdayAfterConfirm = appendList[x ]["dayAfterConfirm"]
            Newphotos = appendList[x ]["photos"]
            if Newphotos == []:
                Newphotos = ''
            else:
                try:
                    Newphotos = str(Newphotos)
                except Exception,e:
                    print("NewPhoto",e)
            datatemp = (seller_id,itemid,pic_url,sku,title,award,buyAmount,updatetime,updatetime_date,updatetime_hour,dayAfterConfirm,enableSNS,datafrom,lastModifyFrom,payTime,promotionType,propertiesAvg,rate,rateId,raterType,showCuIcon,showDepositIcon,spu_string,status,tag,useful,anony,uid,buyernick,rankid,rank,uid_encrypted,NewappendId,Newcontent,Newphotos,rule)
            data.append(datatemp)

    return [data,spuData]
            
def PhraseJson(jsonData):
    maxPage = int(jsonData['maxPage'])
    currentPageNum = int(jsonData['currentPageNum'])
##    print(maxPage,currentPageNum)
##    print(">",currentPageNum,end = '')
    print(">",end='')
    commentsData = jsonData['comments']
    if maxPage > currentPageNum:
        pageno = currentPageNum + 1
    else:
        print(":Done")
        pageno = 0
    return [commentsData,pageno]

def FindJson(pageData):
    try:
        pageJsonData = re.findall('jsonp_reviews_list\((.*)\)',pageData)[0]
        is_banned = 0
    except Exception,e:
        print('#Banned!#')
        print(pageData.encode('utf8'))
        pageJsonData = '{"watershed":100,"maxPage":0,"currentPageNum":0,"comments":null}'
        is_banned = 1
    return [json.loads(pageJsonData),is_banned]

def getSingleData(uid,itemid,rule,pageno):
    #Initial
    seller_id = uid
    taskLife = 4
    sleep = 1
    data = []
    spuData = []
    #getData
    updatetime = getDate()
    while taskLife >0:
        ip = getIp('192.168.1.110',33060,'kettle','root','etc_crawl','ip_proxy')
        try:
            page = openPage(uid,itemid,rule,pageno,ip).read()
            try:
                soup = page.decode('gbk','ignore')
            except Exception,e:
                print("GBK decode Failed:",e)
                soup = page.decode('utf8')

            pageJsonData = FindJson(soup)
            try:
                wait = pageJsonData[0]["status"]
                if wait == 1111:
                    print("GottaWait")
                    ipOk = 1
                    pageJsonData = [0,1]
                else:
                    ipOk = 0
            except:
                ipOk = 0
            
                
        except Exception,e:
            print("PageSoure:",e)
            ipOk = 0
            pageJsonData = [0,1]
            print("TheShitIpProxy,replacing Now")
        if pageJsonData[1] == 1:
            taskLife = taskLife - 1
            if ipOk == 0 or sleep > 3:
                print("Banned 1")
                print(ipOk,":",sleep)
                markBannedIp('192.168.1.110',33060,'kettle','root','etc_crawl','ip_proxy',ip)
            else:
                if sleep == 1:
                    print("Sleep",sleep,end = '')
                else:
                    print(sleep,end = '')
                sleep = sleep + 1
                time.sleep(5)

        else:
            try:
                commentsData = PhraseJson(pageJsonData[0])   
                taskLife = 0
                try:
                    fullData = PhraseCommentData(commentsData[0],seller_id,rule)
                    data.extend(fullData[0])
                    spuData.extend(fullData[1])
                    pageno = commentsData[1]
                except Exception,e:
                    print("NoData",e)
                    print('This Item No Comment Data')
                    pageno = 0
                
            except Exception,e:
                print("TaskLife",e)
                taskLife = taskLife - 1
                time.sleep(5)
            
    return [data,spuData,pageno]


def getData(uid,itemid,rule,limit_page):
    data = []
    spuData = []
    pageno = 1
    print('itemid:',itemid,'F',end='')
    print(limit_page)
    while pageno > 0 and pageno <= limit_page:
        newdata = getSingleData(uid,itemid,rule,pageno)
        data.extend(newdata[0])
        spuData.extend(newdata[1])
        pageno = newdata[2]
    return [data,spuData]
def crawl_item_data(info):
    host = info[0]
    port = info[1]
    user = info[2]
    password = info[3]
    database = info[4]
    tbname = info[5]
    uid = info[6]
    itemid = info[7]
    rule = info[8]
    limit_page = info[9]
   
    itemdata = getData(uid,itemid,rule,limit_page)
    
    print("Wringting...",end='')
    try:
        db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
        dbconn=db.cursor()
        ItemDataInsert = "INSERT IGNORE INTO "+str(tbname)+"(seller_id,itemid,pic_url,sku,title,award,buyamount,updatetime,updatetime_date,updatetime_hour,dayafterconfirm,enablesns,datafrom,lastmodifyfrom,paytime,promotiontype,propertiesavg,rate,rateid,ratertype,showcuicon,showdepositicon,spuratting,status,tag,useful,anony,uid,buyernick,rankid,rank,uid_encrypted,appendid,content,photos,attribute) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        spuDataInsert = "INSERT IGNORE INTO dim_item_spu (`value`,`name`,`spu_desc`) VALUES (%s,%s,%s)"
        try:
            dbconn.executemany(ItemDataInsert,itemdata[0])
        except Exception,e:
            print("ItemData:",e)
            print(itemdata[0])
        try:
            dbconn.executemany(spuDataInsert,itemdata[1])
        except Exception,e:
            print("SpuData:",e)
            print(itemdata[1])
        db.commit()
        db.close()
        print("Writen")
    except Exception,e:
        print("Unable to Write:",e)
        print()
    
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
def initialTable(host,port,user,password,database,tbname,initial_str):
    #initial_str = '''CREATE TABLE IF NOT EXISTS '''+str(tbname)+'''( `itemid` BIGINT(20) NULL DEFAULT NULL, `pic_url` VARCHAR(255) NULL DEFAULT NULL, `sku` VARCHAR(255) NULL DEFAULT NULL, `title` VARCHAR(255) NULL DEFAULT NULL, `award` VARCHAR(255) NULL DEFAULT NULL, `buyamount` INT(11) NULL DEFAULT NULL, `updatetime` DATETIME NULL DEFAULT NULL, `updatetime_date` DATE NULL DEFAULT NULL, `updatetime_hour` VARCHAR(4) NULL DEFAULT NULL, `dayafterconfirm` INT(11) NULL DEFAULT NULL, `enablesns` INT(11) NULL DEFAULT NULL, `datafrom` VARCHAR(255) NULL DEFAULT NULL, `lastmodifyfrom` VARCHAR(255) NULL DEFAULT NULL, `paytime` VARCHAR(255) NULL DEFAULT NULL, `promotiontype` VARCHAR(255) NULL DEFAULT NULL, `propertiesavg` VARCHAR(255) NULL DEFAULT NULL, `rate` INT(11) NULL DEFAULT NULL, `rateid` BIGINT(20) NULL DEFAULT NULL, `ratertype` INT(11) NULL DEFAULT NULL, `showcuicon` INT(11) NULL DEFAULT NULL, `showdepositicon` INT(11) NULL DEFAULT NULL, `spuratting` VARCHAR(255) NULL DEFAULT NULL, `status` INT(11) NULL DEFAULT NULL, `tag` VARCHAR(255) NULL DEFAULT NULL, `useful` INT(11) NULL DEFAULT NULL, `anony` INT(11) NULL DEFAULT NULL, `uid` VARCHAR(50) NULL DEFAULT NULL, `buyernick` VARCHAR(50) NULL DEFAULT NULL, `rankid` int(2) NULL DEFAULT NULL, `rank` int(10) NULL DEFAULT NULL, `uid_encrypted` VARCHAR(50) NULL DEFAULT NULL, `appendid` BIGINT(20) NULL DEFAULT NULL, `content` TEXT NULL, `photos` TEXT NULL, `attribute` varchar(50), INDEX `itemid` (`itemid`), UNIQUE INDEX `unique_index` (`itemid`, `rateid`, `appendid`)) COLLATE='utf8_general_ci' ENGINE=InnoDB;'''
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        dbconn.execute(initial_str % str(tbname))
        result = dbconn.fetchall()
        db.commit()
    except Exception,e:
        print(e)
        print(initial_str)
    dbconn.close()
    return


def initialTableSpu(host,port,user,password,database,tbname):
    initial_str = '''CREATE TABLE IF NOT EXISTS '''+str(tbname)+''' (  `value` bigint(20) DEFAULT NULL,  `name` varchar(50) DEFAULT NULL,  `spu_desc` varchar(50) DEFAULT NULL,  UNIQUE KEY `value` (`value`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8;'''
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

def do_crawl_item(host,port,user,password,database,r_tbname,w_tbname,rule,initial_str,limit_page):
    rule_json = json.loads(rule.encode('utf-8'))
    query_rule = rule_json["query_rule"]
    search_rule = rule_json["search_rule"]
    taskList = getSubTask(host,port,user,password,database,r_tbname,query_rule)
## Uncomment here for multi running task
##    multiTask(taskList,host,user,password,database,item_tbname,keyword,search_rule)

    tasktemp = taskList
    initialTableSpu(host,port,user,password,database,'dim_item_spu')
    initialTable(host,port,user,password,database,w_tbname,initial_str)
    for j in range(0,len(tasktemp)):
        ptask = (host,port,user,password,database,w_tbname,tasktemp[j][0],tasktemp[j][1],tasktemp[j][2],limit_page)
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
    #-------- Configuration part --------#
    #        Connection Database
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
    # Print('SQL Print',sql)
    # SQL Section
    initial_str = sql['raw_crawl_item_comments']

    #---------------END-------------------#
    
    try:
        itemstage = sys.argv[1]
        limit_page = sys.argv[2]
    except:
        itemstage = 408
        limit_page = 1000
        
    projectlist = getTask(host,port,user,password,database,tablename,itemstage)
    print(projectlist)
    for project in projectlist:
        do_crawl_item(host,port,user,password,project[0],project[1],project[2],project[3],initial_str,limit_page)
if __name__ == "__main__":
    main()
    
