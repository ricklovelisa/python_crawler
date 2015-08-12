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
import top.api
import yaml

def getDate():
    date=time.strftime("%Y-%m-%d",time.localtime())
    return date

def getTask(host,port,user,password,database,tablename,itemstage = 1):
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        queryTask = "SELECT `dbname`,w_table,keyword,rule FROM %s.%s WHERE taskid = '%s'"
        print(queryTask % (database,tablename,itemstage))
        dbconn.execute(queryTask % (database,tablename,itemstage))
        result = dbconn.fetchall()
        db.commit()
    except:
        result = []
    dbconn.close()
    return result

def getSubTask(host,port,user,password,database,read_table,query_rule):
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    
    try:
        queryTask = "SELECT keyword,rule,pageno FROM %s.%s %s" % (database,read_table,query_rule)
        print(queryTask)
        dbconn.execute(queryTask)
        result = dbconn.fetchall()
        db.commit()
        
    except:
        result = []
        print("No!SubTask")
    dbconn.close()
    return result
def makeOpener():
    # 代理 IP 使用
    # post cookie
    cookie=cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cookie)
    opener=urllib2.build_opener(cookie_support,urllib2.HTTPHandler)
    return opener

def openPage(pageno):
    #
    # keyword : 关键词
    # pagenumber : 页数
    # ratesum : 等级选择
    # location : 地址选择
    # cat ：类目选择
    # brand ：品牌选择
    # ppath ：客户喜欢选择
    # sort ： 排序方式可选 sale-desc/credit-desc
    #
##    rule_json = json.loads(rule.encode('utf-8'))
##    query_rule = rule_json["query_rule"]
##    search_rule = rule_json["search_rule"]
##    keyword = urllib.quote(keyword.encode("utf8"))
    time.sleep(1)
    opener = makeOpener()
    
    urllib2.install_opener(opener)
    url= 'http://fuwu.taobao.com/ser/list.htm?key=&service_type=&free_order=&is_in_activity=&is_mix_sale=&is_tpartner=&isMultiList=0&listType=1&cat_map_id=52266019&primary_sort=default_sort_tag&primary_sort_desc=true&se_wangwang_status=&location_id=&current=0&current_page='+str(pageno)
    url_referer = 'http://fuwu.taobao.com/ser/list.htm?key=&service_type=&free_order=&is_in_activity=&is_mix_sale=&is_tpartner=&isMultiList=0&listType=1&cat_map_id=52266019&primary_sort=default_sort_tag&primary_sort_desc=true&se_wangwang_status=&location_id=&current=0&current_page=2'
    headers = {
        "GET":url,
        "Accept":"*/*",
        "Connection":"keep-alive",
        "Host":"fuwu.taobao.com",
        "Referer":url_referer,
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.69 Safari/537.36"
        }
    if pageno ==1:
        print(pageno,':',url)
    else:
        print('>',pageno,end = '')
    req=urllib2.Request(url)
    for header in headers:
        req.add_header(header,headers[header])
    page=opener.open(req)
    return page
def soupPage(page,encode = "utf8"):
    # Soup the Page
    soup=BeautifulSoup(page,fromEncoding=encode)
    return soup

def getPageSize(soup):
    pagesize = soup.findAll(attrs={"class":"shop-count"})
    print(pagesize)
    print("$$$$$$$$$$$$$$$$$$$")
    print(str(pagesize[0]))
    print("###################")
    full_pagenum = int(re.findall('<b>(\d+)</b>',str(pagesize))[0])/20
    print(full_pagenum)
    return full_pagenum

def reSoup(temp):
    data = re.sub(r'\r|\n|\t','',str(temp))
    data = re.sub("&lt;","<",data)
    data = re.sub("&gt;",">",data)
    data = re.sub("\s+<","<",data)
    data = re.sub(">\s+",">",data)
    data = re.sub("\s\s+","",data)
    return data

def jsonLoads(temp,keyword,pageno):
    dsrData = json.dumps(eval(temp[0].decode("utf8")))
    dsr = json.loads(dsrData)
    dsr_ship = float(dsr['delivery'][0])/100
    
    if dsr['delivery'][1]==1:
        cg = float(dsr['delivery'][2])/10000
    else:
        if dsr['delivery'][1]==0:
            cg = 0
        else:
            cg = float(dsr['delivery'][2])/-10000
  
    dsr_desc = float(dsr['description'][0])/100
    if dsr['description'][1]==1:
        mg = float(dsr['description'][2])/10000
    else:
        if dsr['description'][1]==0:
            mg = 0
        else:
            mg = float(dsr['description'][2])/-10000
        
    dsr_srv = float(dsr['service'][0])/100
    if dsr['service'][1]==1:
        sg = float(dsr['service'][2])/10000
    else:
        if dsr['service'][1]==0:
            sg = 0
        else:
            sg = float(dsr['service'][2])/-10000
        
    uid_encrypted = dsr['safeUid']
    shoptype = dsr['isTmall']
    uid = temp[1]
    try:
        ratesum = dsr['sellerCredit']
    except:
        ratesum = '-1'

    data = (uid,uid_encrypted,shoptype,ratesum,dsr_desc,dsr_srv,dsr_ship,mg,sg,cg,keyword,pageno)
    return data

    
def getData(keyword,rule,pageno):
    soup = soupPage(openPage(keyword,rule,pageno))
    itemData = reSoup(soup)
##    f = open('D://xxxx.txt','w')
##    f.write(itemData)
##    f.close()
    data = []
    try:
        iteminfo_tmall = re.findall('data-param="({\'isTmall\':\d,\'description\':\[\d+,[-]?\d+,\d+\],\'service\':\[\d+,[-]?\d+,\d+\],\'delivery\':\[\d+,[-]?\d+,\d+\],\'safeUid\':\'\w+\'})"><a target="_blank" href="http:\/\/store.taobao.com\/shop\/view_shop.htm\?user_number_id=(\d+)"',str(itemData))
        for i in range(0,len(iteminfo_tmall)):
            data.append(jsonLoads(iteminfo_tmall[i],keyword,pageno))
    except Exception,e:
        print(e)
        iteminfo_tmall = []
    try:
        iteminfo = re.findall('data-param="({\'isTmall\':\d,\'description\':\[\d+,[-]?\d+,\d+\],\'service\':\[\d+,[-]?\d+,\d+\],\'delivery\':\[\d+,[-]?\d+,\d+\],\'safeUid\':\'\w+\',\'sellerCredit\':\d+,\'totalRate\':\d+})"><a target="_blank" href="http:\/\/store.taobao.com\/shop\/view_shop.htm\?user_number_id=(\d+)"',str(itemData))
        for j in range(0,len(iteminfo)):
            data.append(jsonLoads(iteminfo[j],keyword,pageno))
    except:
        iteminfo = []
    return data

def getDataNewOld(keyword,rule,pageno):
    soup = soupPage(openPage(keyword,rule,pageno))
    itemData = reSoup(soup)
##    f = open('D://xxxx.txt','w')
##    f.write(itemData)
##    f.close()
    data = []
    try:
        iteminfo_tmall = re.findall('m=get_shop_card\&amp;sid=(\d+)\&amp;bid=(\d+)',str(itemData))
        for i in range(0,len(iteminfo_tmall)):
            data.append((iteminfo_tmall[i][1],iteminfo_tmall[i][0],keyword,pageno))
    except Exception,e:
        print('iteminf_tmall_error:',e)
        iteminfo_tmall = []
##    try:
##        iteminfo = re.findall('data-param="({\'isTmall\':\d,\'description\':\[\d+,[-]?\d+,\d+\],\'service\':\[\d+,[-]?\d+,\d+\],\'delivery\':\[\d+,[-]?\d+,\d+\],\'safeUid\':\'\w+\',\'sellerCredit\':\d+,\'totalRate\':\d+})"><a target="_blank" href="http:\/\/store.taobao.com\/shop\/view_shop.htm\?user_number_id=(\d+)"',str(itemData))
##        for j in range(0,len(iteminfo)):
##            data.append(jsonLoads(iteminfo[j],keyword,pageno))
##    except:
##        iteminfo = []
    return data

def getDataNew(keyword,rule,pageno):
    soup = soupPage(openPage(keyword,rule,pageno))
    itemData = reSoup(soup)

    data = []
    try:
        iteminfo_tmall = re.findall('comment_count":"(\d+)","nick":"(.*?)","nid":"(\d+)".*?"user_id":"(\d+)","raw_title":"(.*?)".*?"isTmall":(\d).*?item_loc":"(.*?)","detail_url.*?"view_sales":"(\d+).*?","view_price":"(\d+.\d+)","view_fee":"(\d+.\d+)"',itemData)
        for i in range(0,len(iteminfo_tmall)):
            #print(iteminfo_tmall[i][3].encode("utf8"))
            data.append((iteminfo_tmall[i][0],iteminfo_tmall[i][1].decode('raw_unicode_escape'),iteminfo_tmall[i][2],iteminfo_tmall[i][3],iteminfo_tmall[i][4].decode('raw_unicode_escape'),iteminfo_tmall[i][5],iteminfo_tmall[i][6].decode('raw_unicode_escape'),iteminfo_tmall[i][7],iteminfo_tmall[i][8],iteminfo_tmall[i][9],keyword,pageno))
    except Exception,e:
        print('iteminfo_error:',e)
        iteminfo_tmall = []
##    try:
##        iteminfo = re.findall('data-param="({\'isTmall\':\d,\'description\':\[\d+,[-]?\d+,\d+\],\'service\':\[\d+,[-]?\d+,\d+\],\'delivery\':\[\d+,[-]?\d+,\d+\],\'safeUid\':\'\w+\',\'sellerCredit\':\d+,\'totalRate\':\d+})"><a target="_blank" href="http:\/\/store.taobao.com\/shop\/view_shop.htm\?user_number_id=(\d+)"',str(itemData))
##        for j in range(0,len(iteminfo)):
##            data.append(jsonLoads(iteminfo[j],keyword,pageno))
##    except:
##        iteminfo = []
    return data

def runCrawl(info):
    host = info[0]
    port = info[1]
    user = info[2]
    password = info[3]
    database = info[4]
    tbname = info[5]
    keywords = info[6]
    rule = info[7]
    pageno = info[8]

    for keyword in keywords.split(","):
        try:
            resultdata = getDataNew(keyword,rule,pageno)
            if resultdata == []:
                resultdata = [(-1,-1,keyword,pageno)]
                print("No Data",keyword)
            db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
            dbconn=db.cursor()
            ItemDataInsert = "INSERT INTO "+str(tbname)+" (comment_count,sellernick,itemid,uid,title,shoptype,address,volume30day,zk_final_price,shipping_fee,keyword,pageno) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE uid = VALUES(uid)"
            dbconn.executemany(ItemDataInsert,resultdata)
            db.commit()
            db.close()
        except Exception,e:
            print(e)
            print("Banned:",keyword)
    
    
    
    
def multiTask(tasklist,host,port,user,password,database,write_table,appkey,secret):
    for i in range(0,len(tasklist),20):
        tasktemp = tasklist[i:i+20]
        job=[]
        if i <20:
            print(getDate()+":"+"Begin_Project:"+str(len(tasklist)))
        print(getDate()+":"+"Process:"+str(round((i+10)*100/len(tasklist),0))+"%")
        for j in range(0,len(tasktemp)):
            ptask = (host,port,user,password,database,write_table,appkey,secret,tasktemp[j][0])
            # info
            p = multiprocessing.Process(target = api_pidvid_data,args=(ptask,))
            p.start()
            job.append(p)
        for p in job:
            p.join()
def initialTable(host,port,user,password,database,tbname,initial_str):
    #initial_str = '''CREATE TABLE IF NOT EXISTS '''+str(tbname)+'''(sellernick varchar(50),itemid BIGINT(20),title varchar(255),address varchar(50), `uid` BIGINT(20) NULL DEFAULT NULL, `uid_encrypted` VARCHAR(50) NULL DEFAULT NULL, `shoptype` INT(11) NULL DEFAULT NULL, `ratesum` INT(11) NULL DEFAULT NULL, `dsr_desc` FLOAT(5,2) NULL DEFAULT NULL, `dsr_srv` FLOAT(5,2) NULL DEFAULT NULL, `dsr_ship` FLOAT(5,2) NULL DEFAULT NULL, `mg` FLOAT(6,5) NULL DEFAULT NULL, `sg` FLOAT(6,5) NULL DEFAULT NULL, `cg` FLOAT(6,5) NULL DEFAULT NULL, `volume30day` INT,zk_final_price float(15,2), `shipping_fee` float(15,2), comment_count BIGINT(20),`keyword` VARCHAR(50) NULL DEFAULT NULL, `pageno` INT(11) NULL DEFAULT NULL,UNIQUE INDEX `itemid` (`itemid`), INDEX `uid` (`uid`), INDEX `uid_encrypted` (`uid_encrypted`) ) COLLATE='utf8_general_ci' ENGINE=InnoDB;'''
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        dbconn.execute(initial_str % str(tbname))
        result = dbconn.fetchall()
        db.commit()
    except Exception,e:
        print(e)
    dbconn.close()
    return

def runJob(host,port,user,password,database,write_table,keyword,rule,initial_str):
    rule_json = json.loads(rule.encode('utf-8'))
    query_rule = rule_json["query_rule"]
    search_rule = rule_json["search_rule"]
##    taskList = getSubTask(host,user,password,database,read_table,query_rule)
##    multiTask(taskList,host,user,password,database,write_table,appkey,secret)
##    tasktemp = taskList
##    print("Total_UID:",str(len(tasktemp)))
    initialTable(host,port,user,password,database,write_table,initial_str)
    for pageno in range(1,101):
        ptask = (host,port,user,password,database,write_table,keyword,rule,pageno)
        runCrawl(ptask)

def main():
    #########################################################
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
    initial_str = sql['raw_crawl_search_item']
    
    #########################################################
    
    try:
        itemstage = sys.argv[1]
    except:
        itemstage = 21
    print(itemstage)
    projectlist = getTask(host,port,user,password,database,tablename,itemstage)
    print(len(projectlist))
    for project in projectlist:
        runJob(host,port,user,password,project[0],project[1],project[2],project[3],initial_str)
if __name__ == "__main__":
    main()
##    for itemstage in range(101,198):
##        print(itemstage)

    
