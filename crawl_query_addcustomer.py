#!/usr/bin/python
# encoding:utf8
# All competitors
# Copyright(c)2012 vsu@opensuse.org

from __future__ import print_function
import sys,os,MySQLdb
import urllib2,urllib,time,re,socket,cookielib,random
from selenium import webdriver
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

def getTask(host,user,password,database,tablename,itemstage = 1):
    db=MySQLdb.connect(host=host,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        queryTask = "SELECT `dbname`,taggettable,storetable,rule FROM %s.%s WHERE stage = '%s'"
        dbconn.execute(queryTask % (database,tablename,itemstage))
        result = dbconn.fetchall()
        db.commit()
    except:
        result = []
    dbconn.close()
    return result

def getSubTask(host,user,password,database,shop_tbname,query_rule):
    # keyword,pagenumber = 1,ratesum = "",location = "",cat = "",brand = "",ppath = "",sort = "sale-desc")
    db=MySQLdb.connect(host=host,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        queryTask = "SELECT uid_encrypted,attribute FROM %s.%s %s" % (database,shop_tbname,query_rule)
        dbconn.execute(queryTask)
        result = dbconn.fetchall()
        db.commit()
    except Exception,e:
        try:
            queryTask = "SELECT uid_encrypted,'' FROM %s.%s %s" % (database,shop_tbname,query_rule)
            dbconn.execute(queryTask)
            result = dbconn.fetchall()
            db.commit()
        except Exception,e:
            print(e)
            result = []
    dbconn.close()
    return result
def getIp(host,user,password,database,tbname):
    db=MySQLdb.connect(host=host,user=user,passwd=password,db=database,charset="utf8")
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

def markBannedIp(host,user,password,database,tbname,ip):
    db=MySQLdb.connect(host=host,user=user,passwd=password,db=database,charset="utf8")
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
def makeCandy():
    chromedriver = '''C:/Users/db/Desktop/crawl/use/chrome/chromedriver.exe'''
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
##    driver.get("https://login.taobao.com/member/login.jhtml")
    driver.get("http://shop.crm.taobao.com")

    # 获得cookie信息
    cookie= driver.get_cookies()

    #将获得cookie的信息打印
    print(cookie)

    driver.quit()
    return cookie

def makeCookie():
    # 生成 Cookie 支持
    cookie=cookielib.LWPCookieJar()
    print(cookie)
    cookie_support = urllib2.HTTPCookieProcessor(cookie)
    return cookie_support

def openPage(uid_encrypted,rule,pageno,ip):
    # 使用代理 IP 打开页面
    ##    keyword = urllib.quote(keyword.encode("utf8"))
    ipJson =  {'http':'http://'+str(ip[0][0])+':'+str(ip[0][1])}
    print(ipJson)
    proxy_handler = urllib2.ProxyHandler(ipJson)
    opener=urllib2.build_opener(makeCookie(),urllib2.HTTPHandler,proxy_handler)
    urllib2.install_opener(opener)
    # 生成 URL
    # rater
    # rater = 1 来自他人的评价
    # rater = 3 给予他人的评价
    rater = 3
    url = 'http://ecrm.taobao.com/wangwang/updateMemberInfo.do?buyerId='+str(uid)+'&_tb_token_=Fz9G5CNESn&_input_charset=UTF-8&name='+str(buyernick)+'&callBack=jsonp43'
    url_referer= url
    # 加载 URL 头
    headers = {
        "GET":url,
        "Accept":"*/*",
        "Connection":"keep-alive",
        "Host":"ecrm.taobao.com",
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

def PhraseCommentData(rateListDetail,rule):
    data = []
    spuData = []
    
    for i in range(0,len(rateListDetail)):
        auction = rateListDetail[i]["auction"] # No Need
        try:
            itemid = auction['aucNumId']
            sku = re.sub('&nbsp','',auction['sku'])
            title = auction['title']
        except:
            itemid = ''
            sku = ''
            title =''
        award = rateListDetail[i]['award']
        buyAmount = rateListDetail[i]["buyAmount"]
        
        content = reSoup(rateListDetail[i]["content"].encode('utf8')) # AppendList
        try:
            date = re.sub('日','',re.sub('年','-',re.sub('月','-',rateListDetail[i]["date"].encode('utf8'))))
        except Exception,e:
            print("Data:",e)
            print(type(rateListDetail[i]["date"]))
            print(rateListDetail[i]["date"])
        dayAfterConfirm = rateListDetail[i]["dayAfterConfirm"] # AppendList
        enableSNS = rateListDetail[i]["enableSNS"]
        datafrom = rateListDetail[i]["from"]
        lastModifyFrom = rateListDetail[i]["lastModifyFrom"]
        try:
            payTime = str(rateListDetail[i]["payTime"]['time'])[0:10]
            payTime = unixTime(int(payTime))
        except Exception,e:
            payTime = ''
        photos = rateListDetail[i]["photos"] # AppendList
        if photos == []:
            photos = ''
        else:
            try:
                photos = str(photos).encode('utf8')
            except Exception,e:
                print("photo:",e)
##            photos = re.sub(',','\,',str(photos))
        promotionType = rateListDetail[i]["promotionType"]
        propertiesAvg = rateListDetail[i]["propertiesAvg"]
        rate = rateListDetail[i]["rate"]
        rateId = rateListDetail[i]["rateId"]
        raterType = rateListDetail[i]["raterType"]
        showCuIcon = rateListDetail[i]["showCuIcon"]
        showDepositIcon = rateListDetail[i]["showDepositIcon"]
        spuRatting = rateListDetail[i]["spuRatting"]
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

        tag = rateListDetail[i]["tag"]
        useful = rateListDetail[i]["useful"]
        user = rateListDetail[i]["user"] # No Need
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
            rank = ''
        appendId = 0
        datatemp = (itemid,sku,title,award,buyAmount,date,dayAfterConfirm,enableSNS,datafrom,lastModifyFrom,payTime,promotionType,propertiesAvg,rate,rateId,raterType,showCuIcon,showDepositIcon,spu_string,tag,useful,anony,uid,buyernick,rank,uid_encrypted,appendId,content,photos,rule)
        data.append(datatemp)
        appendList = rateListDetail[i]["appendList"]
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
            datatemp = (itemid,sku,title,award,buyAmount,date,dayAfterConfirm,enableSNS,datafrom,lastModifyFrom,payTime,promotionType,propertiesAvg,rate,rateId,raterType,showCuIcon,showDepositIcon,spu_string,status,tag,useful,anony,uid,buyernick,rank,uid_encrypted,NewappendId,Newcontent,Newphotos,rule)
            data.append(datatemp)

    return [data,spuData]
            
def PhraseJson(jsonData):
    maxPage = int(jsonData['maxPage'])
    currentPageNum = int(jsonData['currentPageNum'])
##    print(maxPage,currentPageNum)
##    print(">",currentPageNum,end = '')
    print(">",end='')
    commentsData = jsonData['rateListDetail']
    if maxPage > currentPageNum:
        pageno = currentPageNum + 1
    else:
        print(":Done")
        pageno = 0
    return [commentsData,pageno]

def FindJson(pageData):
    try:
        pageJsonData = re.findall('jsonp_reviews_list\((.*)\)',pageData.encode('utf8'))[0]
        is_banned = 0
    except Exception,e:
        print('#Banned!#')
        print(pageData.encode('utf8'))
        pageJsonData = '{"watershed":100,"maxPage":0,"currentPageNum":0,"rateListDetail":null}'
        is_banned = 1
    return [json.loads(pageJsonData),is_banned]

def getSingleData(uid_encrypted,rule,pageno):
    #Initial
    taskLife = 6
    sleep = 1
    data = []
    spuData = []
    #getData
    updatetime = getDate()
    while taskLife >0:
        ip = getIp('192.168.1.110','kettle','root','etc_crawl','ip_proxy')
        try:
            page = openPage(uid_encrypted,rule,pageno,ip)
            try:
                soup = page.read().decode('gbk')
            except:
                soup = page.read().decode('utf8')

            pageJsonData = FindJson(soup)
            try:
                wait = pageJsonData[0]["status"]
                print(wait)
                if wait == 1111:
                    ipOk = 1
                    pageJsonData = [0,1]
                else:
                    if wait == 'checkcode':
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
            print("The Shit Ip Proxy,replacing Now")
        if pageJsonData[1] == 1:
            
            taskLife = taskLife - 1
            if ipOk == 0 or sleep > 3:
                print("Banned 1")
                markBannedIp('192.168.1.110','kettle','root','etc_crawl','ip_proxy',ip)
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
                    fullData = PhraseCommentData(commentsData[0],rule)
                    data.extend(fullData[0])
                    spuData.extend(fullData[1])
                except Exception,e:
                    print("NoData",e)
                    print('This Item No Comment Data')
                pageno = commentsData[1]
            except Exception,e:
                print("TaskLife",e)
                print(pageJsonData[0])
                taskLife = taskLife - 1
                time.sleep(5)
    return [data,spuData,pageno]

def getData(uid_encrypted,rule):
    data = []
    spuData = []
    pageno = 1
    print('uid_encrypted:',uid_encrypted,'F',end='')
    while pageno > 0:
        newdata = getSingleData(uid_encrypted,rule,pageno)
        data.extend(newdata[0])
        spuData.extend(newdata[1])
        pageno = newdata[2]
    return [data,spuData]
def crawl_item_data(info):
    host = info[0]
    user = info[1]
    password = info[2]
    database = info[3]
    tbname = info[4]
    uid_encrypted = info[5]
    rule = info[6]

    itemdata = getData(uid_encrypted,rule)
    
    print("Wringting...",end='')
    db=MySQLdb.connect(host=host,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    ItemDataInsert = "INSERT IGNORE INTO "+str(tbname)+"(itemid,title,sku,award,buyamount,updatetime,dayafterconfirm,enablesns,datafrom,lastmodifyfrom,paytime,promotiontype,propertiesavg,rate,rateid,ratertype,showcuicon,showdepositicon,spuratting,tag,useful,anony,uid,buyernick,rank,uid_encrypted,appendid,content,photos,attribute) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    spuDataInsert = "INSERT IGNORE INTO dim_item_spu (`value`,`name`,`spu_desc`) VALUES (%s,%s,%s)"
    dbconn.executemany(ItemDataInsert,itemdata[0])
    dbconn.executemany(spuDataInsert,itemdata[1])
    db.commit()
    db.close()
    print("Writen")
    
def multiTask(tasklist,host,user,password,database,item_tbname,keyword,search_rule):
    for i in range(0,len(tasklist),20):
        tasktemp = tasklist[i:i+20]
        job=[]
        if i <20:
            print(getDate()+":"+"Begin_Project:"+str(len(tasklist)))
        print(getDate()+":"+"Process:"+str(round((i+10)*100/len(tasklist),0))+"%")
        for j in range(0,len(tasktemp)):
            ptask = (host,user,password,database,w_tbname,tasktemp[j][0],tasktemp[j][1])
            # info
            p = multiprocessing.Process(target = crawl_item_data,args=(ptask,))
            p.start()
            job.append(p)
        for p in job:
            p.join()
def initialTable(host,user,password,database,tbname):
    initial_str = '''CREATE TABLE IF NOT EXISTS '''+str(tbname)+'''( `itemid` BIGINT(20) NULL DEFAULT NULL, `pic_url` VARCHAR(255) NULL DEFAULT NULL, `sku` VARCHAR(255) NULL DEFAULT NULL, `title` VARCHAR(255) NULL DEFAULT NULL, `award` VARCHAR(255) NULL DEFAULT NULL, `buyamount` INT(11) NULL DEFAULT NULL, `updatetime` DATETIME NULL DEFAULT NULL, `dayafterconfirm` INT(11) NULL DEFAULT NULL, `enablesns` INT(11) NULL DEFAULT NULL, `datafrom` VARCHAR(255) NULL DEFAULT NULL, `lastmodifyfrom` VARCHAR(255) NULL DEFAULT NULL, `paytime` VARCHAR(255) NULL DEFAULT NULL, `promotiontype` VARCHAR(255) NULL DEFAULT NULL, `propertiesavg` VARCHAR(255) NULL DEFAULT NULL, `rate` INT(11) NULL DEFAULT NULL, `rateid` BIGINT(20) NULL DEFAULT NULL, `ratertype` INT(11) NULL DEFAULT NULL, `showcuicon` INT(11) NULL DEFAULT NULL, `showdepositicon` INT(11) NULL DEFAULT NULL, `spuratting` VARCHAR(255) NULL DEFAULT NULL, `status` INT(11) NULL DEFAULT NULL, `tag` VARCHAR(255) NULL DEFAULT NULL, `useful` INT(11) NULL DEFAULT NULL, `anony` INT(11) NULL DEFAULT NULL, `uid` VARCHAR(50) NULL DEFAULT NULL, `buyernick` VARCHAR(50) NULL DEFAULT NULL, `rank` VARCHAR(50) NULL DEFAULT NULL, `uid_encrypted` VARCHAR(50) NULL DEFAULT NULL, `appendid` BIGINT(20) NULL DEFAULT NULL, `content` TEXT NULL, `photos` TEXT NULL, `attribute` varchar(50), INDEX `itemid` (`itemid`)) COLLATE='utf8_general_ci' ENGINE=InnoDB;'''
    db=MySQLdb.connect(host=host,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        dbconn.execute(initial_str)
        result = dbconn.fetchall()
        db.commit()
    except Exception,e:
        print(e)
    dbconn.close()
    return

def initialTableSpu(host,user,password,database,tbname):
    initial_str = '''CREATE TABLE IF NOT EXISTS '''+str(tbname)+'''( `value` BIGINT(20) NULL DEFAULT NULL, `name` VARCHAR(50) NULL DEFAULT NULL, `spu_desc` VARCHAR(50) NULL DEFAULT NULL, UNIQUE INDEX `value` (`value`) ) COLLATE='utf8_general_ci'  ENGINE=InnoDB;'''
    db=MySQLdb.connect(host=host,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        dbconn.execute(initial_str)
        result = dbconn.fetchall()
        db.commit()
    except Exception,e:
        print(e)
    dbconn.close()
    return

def do_crawl_item(host,user,password,database,r_tbname,w_tbname,rule):
    rule_json = json.loads(rule.encode('utf-8'))
    query_rule = rule_json["query_rule"]
    search_rule = rule_json["search_rule"]
    taskList = getSubTask(host,user,password,database,r_tbname,query_rule)
## Uncomment here for multi running task
##    multiTask(taskList,host,user,password,database,item_tbname,keyword,search_rule)

    tasktemp = taskList
    initialTableSpu(host,user,password,database,'dim_comment_spu')
    initialTable(host,user,password,database,w_tbname)
    for j in range(0,len(tasktemp)):
        ptask = (host,user,password,database,w_tbname,tasktemp[j][0],search_rule)
        crawl_item_data(ptask)

def writeStatus(host,user,password,database,shopid,pageinfo):
    '''
    Log and current job status sent
    '''
    # keyword,pagenumber = 1,ratesum = "",location = "",cat = "",brand = "",ppath = "",sort = "sale-desc")
    db=MySQLdb.connect(host=host,user=user,passwd=password,db=database,charset="utf8")
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
##    conf_file = open('/etc/crawl/item_conf')
##    conf = yaml.load(conf_file)
##    host = conf['host']
##    user = conf['user']
##    password = conf['password']
##    database = conf['database']
##    tablename = conf['tablename']
    host = '192.168.1.110'
    user = 'kettle'
    password = 'root'
    database = 'etc_crawl'
    tablename = 'crawl_config'
    try:
        itemstage = sys.argv[1]
    except:
        itemstage = 102412
        
    projectlist = getTask(host,user,password,database,tablename,itemstage)
    print(projectlist)
    for project in projectlist:
        do_crawl_item(host,user,password,project[0],project[1],project[2],project[3])
if __name__ == "__main__":
    makeCandy()
##    print(makeCookie())
    
