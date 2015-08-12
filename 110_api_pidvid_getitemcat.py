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
#import yaml

def getDate():
    date=time.strftime("%Y-%m-%d",time.localtime())
    return date

def getTask(host,port,user,password,database,tablename,itemstage = 1):
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

def getSubTask(host,port,user,password,database,read_table,query_rule):
    # keyword,pagenumber = 1,ratesum = "",location = "",cat = "",brand = "",ppath = "",sort = "sale-desc")
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
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

def getPidvid(parent_cid,appkey,secret,level):
##    url = "http://localhost"
##    port = "80"
##    appkey = "21786895"
##    secret = "934fe5351c6d2c2a506aa97fdbd445b1"
    req=top.api.ItemcatsGetRequest()
    req.set_app_info(top.appinfo(appkey,secret))
    req.parent_cid=parent_cid
    req.fields="cid,parent_cid,name,is_parent"
    try:
            resp= req.getResponse()
            print("Fetched")
            dataset = resp.get('itemcats_get_response').get('item_cats').get('item_cat')
    except Exception,e:
            print('resp error:',e)
            dataset = []
    data = []

    for i in range(0,len(dataset)):
        cid = dataset[i].get('cid')
        name = dataset[i].get('name')
        parent_cid = dataset[i].get('parent_cid')
        is_parent = dataset[i].get('is_parent')
        datatemp = (cid,name,parent_cid,is_parent,level+1)
        data.append(datatemp)

    return data

def api_pidvid_data(info):
    host = info[0]
    port = info[1]
    user = info[2]
    password = info[3]
    database = info[4]
    tbname = info[5]
    appkey = info[6]
    secret = info[7]
    cid = info[8]
    level = info[9]

    try:
        pidviddata = getPidvid(cid,appkey,secret,level)

        if pidviddata == []:
            is_end = 1
        else:
            is_end = 0
        
        db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
        dbconn=db.cursor()
        ItemDataInsert = "REPLACE INTO "+str(tbname)+" (cid,name,parent_cid,is_parent,level) VALUES (%s,%s,%s,%s,%s)"
        dbconn.executemany(ItemDataInsert,pidviddata)
        db.commit()
        db.close()
    except Exception,e:
        print(e)
        print("No Attrib:",str(cid))
    return is_end
    
    
def initialTable(host,port,user,password,database,tbname):
    initial_str = '''CREATE TABLE IF NOT EXISTS '''+str(tbname)+'''(cid bigint,name varchar(50),parent_cid bigint,is_parent varchar(10),level int(1),INDEX `cid` (cid),INDEX `level` (level)) COLLATE='utf8_general_ci' ENGINE=InnoDB;'''
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
    
def do_api_pidvid(host,port,user,password,database,write_table,appkey,secret,level):
    query_rule = '''where is_parent = '1' and level = %s and cid not in (select parent_cid from %s.%s) group by cid''' % (level,database,write_table)
    taskList = getSubTask(host,port,user,password,database,write_table,query_rule)


##    multiTask(taskList,host,user,password,database,write_table,appkey,secret)
    tasktemp = taskList
    z = len(tasktemp)

    print("Total_CID:",str(z))
    if z==0:
        print("yes")
        z = 1
        tasktemp = ((0,),)
    for j in range(0,z):

        ptask = (host,port,user,password,database,write_table,appkey,secret,tasktemp[j][0],level)
        is_end = api_pidvid_data(ptask)

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
    port = 33060
    password = 'root'
    database = 'etc_calc'
    tablename = 'dim_itemcat_r20150401'
##    appkey = "21786895"
##    secret = "934fe5351c6d2c2a506aa97fdbd445b1"
    appkey = "23113820"
    secret = "dd3e0ad2b2cff904bfccfc823aba7ad4"
    try:
        itemstage = sys.argv[1]
    except:
        itemstage = 6
    projectlist = (0,1,2,3,4,5,6)
    for level in projectlist:
        print(level)
        initialTable(host,port,user,password,database,tablename)
        do_api_pidvid(host,port,user,password,database,tablename,appkey,secret,level)
if __name__ == "__main__":
    main()
##    cid = '120878006'
##    appkey = "21786895"
##    secret = "934fe5351c6d2c2a506aa97fdbd445b1"
##    jim = getPidvid(cid,appkey,secret)
##    for x in jim:
##        print(x)
