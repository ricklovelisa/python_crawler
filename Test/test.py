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
from snownlp import SnowNLP
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
        queryTask = "SELECT rateid,uid,buyernick,rank,uid_encrypted,content FROM %s.%s %s" % (database,shop_tbname,query_rule)
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

def main():
    host = 'localhost'
    user = 'root'
    password = 'root'
    database = 'db_leihon'
    tablename = 'crawl_item_comments'
    tbname = 'result'
    rule = ''
    try:
        itemstage = sys.argv[1]
    except:
        itemstage = 102412
        
    projectlist = getSubTask(host,user,password,database,tablename,rule)
    
    data = []
    for project in projectlist:
        s = (project[0],project[1],project[2],project[3],project[4],project[5],SnowNLP(project[5]).sentiments)
        data.append(s)
    db = MySQLdb.connect(host=host,user=user,passwd=password,db=database,charset="utf8")
    dbconn = db.cursor()
    InsertStr = "REPLACE INTO "+str(tbname)+"(rateid,uid,buyernick,rank,uid_encrypted,content,sentiments) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    dbconn.executemany(InsertStr,data)
    db.commit()
    db.close()
        
##    for project in projectlist:
##        do_crawl_item(host,user,password,project[0],project[1],project[2],project[3])
if __name__ == "__main__":
    main()
    
