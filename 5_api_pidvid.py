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

def getTask(host,user,password,database,tablename,itemstage = 1):
    db=MySQLdb.connect(host=host,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        queryTask = "SELECT `dbname`,r_table,w_table,keyword,rule FROM %s.%s WHERE taskid = '%s'"
        print(queryTask % (database,tablename,itemstage))
        dbconn.execute(queryTask % (database,tablename,itemstage))
        result = dbconn.fetchall()
        db.commit()
    except:
        result = []
    dbconn.close()
    return result

def getSubTask(host,user,password,database,read_table,query_rule):
    # keyword,pagenumber = 1,ratesum = "",location = "",cat = "",brand = "",ppath = "",sort = "sale-desc")
    db=MySQLdb.connect(host=host,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    
    try:
        queryTask = "SELECT cid FROM %s.%s %s" % (database,read_table,query_rule)
        print(queryTask)
        dbconn.execute(queryTask)
        result = dbconn.fetchall()
        db.commit()
        
    except:
        result = []
        print("Error!SubTask")
    dbconn.close()
    return result

def getPidvid(cid,appkey,secret):
##    url = "http://localhost"
##    port = "80"
##    appkey = "21786895"
##    secret = "934fe5351c6d2c2a506aa97fdbd445b1"
    req=top.api.ItempropsGetRequest()
    req.set_app_info(top.appinfo(appkey,secret))

    req.fields="pid,name,must,multi,prop_values"
    req.cid=cid
    data = []
    try:
        resp= req.getResponse()
    except Exception,e:
        print(e)
        resp =[]

    dataset = resp.get('itemprops_get_response').get('item_props').get('item_prop')
    for i in range(0,len(dataset)):
        pid = dataset[i].get('pid')
        props = dataset[i].get('name')
        try:
            values = dataset[i].get('prop_values').get('prop_value')    

            for j in values:
                value = j.get('name')
                vid = j.get('vid')
                datatemp = (cid,pid,props,vid,value)
                data.append(datatemp)


        except Exception,e:
            vid = 0
            value = 0
            datatemp = (cid,pid,props,vid,value)
            data.append(datatemp)

    return data

def api_pidvid_data(info):
    host = info[0]
    user = info[1]
    password = info[2]
    database = info[3]
    tbname = info[4]
    appkey = info[5]
    secret = info[6]
    cid = info[7]

    try:
        pidviddata = getPidvid(cid,appkey,secret)
        print(pidviddata)
        #db=MySQLdb.connect(host=host,user=user,passwd=password,db=database,charset="utf8")
        #dbconn=db.cursor()
        ItemDataInsert = "REPLACE INTO "+str(tbname)+" (cid,pid,props,vid,value) VALUES (%s,%s,%s,%s,%s)"
        print(ItemDataInsert)
        #dbconn.executemany(ItemDataInsert,pidviddata)
        #db.commit()
        #db.close()
    except Exception,e:
        print(e)
        print("No Attrib:",str(cid))
    
    
    
def multiTask(tasklist,host,user,password,database,write_table,appkey,secret):
    for i in range(0,len(tasklist),20):
        tasktemp = tasklist[i:i+20]
        job=[]
        if i <20:
            print(getDate()+":"+"Begin_Project:"+str(len(tasklist)))
        print(getDate()+":"+"Process:"+str(round((i+10)*100/len(tasklist),0))+"%")
        for j in range(0,len(tasktemp)):
            ptask = (host,user,password,database,write_table,appkey,secret,tasktemp[j][0])
            # info
            p = multiprocessing.Process(target = api_pidvid_data,args=(ptask,))
            p.start()
            job.append(p)
        for p in job:
            p.join()

def do_crawl_item(host,user,password,database,shop_tbname,item_tbname,keyword,rule):
    rule_json = json.loads(rule.encode('utf-8'))
    query_rule = rule_json["query_rule"]
    search_rule = rule_json["search_rule"]
    taskList = getSubTask(host,user,password,database,shop_tbname,query_rule)
    multiTask(taskList,host,user,password,database,item_tbname,keyword,search_rule)
##    tasktemp = taskList
##    for j in range(0,len(tasktemp)):
##        ptask = (host,user,password,database,item_tbname,keyword,search_rule,tasktemp[j][0])
##        crawl_item_data(ptask)

    

def initialTable(host,user,password,database,tbname):
    initial_str = '''CREATE TABLE IF NOT EXISTS '''+str(tbname)+'''(	`cid` BIGINT(20) NOT NULL,	`props` VARCHAR(50) NOT NULL DEFAULT '-1' COMMENT '标签归属',	`pid` BIGINT(20) NOT NULL DEFAULT '-1' COMMENT '归属ID',	`value` VARCHAR(255) NOT NULL DEFAULT '-1' COMMENT '标签内容',	`vid` BIGINT(20) NOT NULL DEFAULT '-1' COMMENT '标签ID',		UNIQUE INDEX `pid_vid` (`pid`, `vid`),	INDEX `props` (`props`),	INDEX `value` (`value`) ) COLLATE='utf8_general_ci' ENGINE=InnoDB;'''
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
    
def do_api_pidvid(host,user,password,database,read_table,write_table,rule,appkey,secret):
    rule_json = json.loads(rule.encode('utf-8'))
    query_rule = rule_json["query_rule"]
    taskList = getSubTask(host,user,password,database,read_table,query_rule)
##    multiTask(taskList,host,user,password,database,write_table,appkey,secret)
    tasktemp = taskList
    print("Total_CID:",str(len(tasktemp)))
    initialTable(host,user,password,database,write_table)
    for j in range(0,len(tasktemp)):
        ptask = (host,user,password,database,write_table,appkey,secret,tasktemp[j][0])
        api_pidvid_data(ptask)

def main():
    # Connection Database
    conf_file_path = sys.path[0]+"/conf/crawl.conf"
    conf_file = open(conf_file_path)
    conf = yaml.load(conf_file)
    
    host = conf['host']
    port = conf['port']
    user = conf['user']
    password = conf['password']
    conf_database = conf['database']
    conf_table = conf['tablename']
    

##    appkey = "21786895"
##    secret = "934fe5351c6d2c2a506aa97fdbd445b1"
##    appkey = "21786894"
##    secret = "6b2b2d023dd3fc3945a565ba6e92c414"
##    appkey = "21786893"
##    secret = "e237dcf5e0c0f4bf168688fc955c6dd7"
    appkey = "21822600"
    secret = "9b97a2886dbbb57b4307271d354e1f7d"
    try:
        itemstage = sys.argv[1]
    except:
        itemstage = 289
    projectlist = getTask(host,user,password,database,tablename,itemstage)
    for project in projectlist:
        do_api_pidvid(host,user,password,project[0],project[1],project[2],project[4],appkey,secret)


if __name__ == "__main__":


    main()  ##    cid = '120878006'


