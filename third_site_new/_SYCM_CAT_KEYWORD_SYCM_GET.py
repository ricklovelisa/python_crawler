#!/usr/bin/python
# encoding:utf8
# All competitors
# Copyright(c)2012 vsu@opensuse.org


import sys,os,MySQLdb,time
import webbrowser

def openRecruit(url):
        webbrowser.open_new_tab(url)
        return webbrowser.get()

def cat_keyword(host,port,user,password,database,tablename,rule):
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        queryTask = "SELECT `cat_id` FROM %s.%s %s"
        
        dbconn.execute(queryTask % (database,tablename,rule))
        result = dbconn.fetchall()
        db.commit()
    except Exception,e:
        print(e)
        result = []
    dbconn.close()
    return result

def cat_url(cid,devid):
        url = 'http://sycm.taobao.com/excel/IndustryKeywordExcel.do?device='+str(devid)+'&cateId='+str(cid)+'&pageSize=100&orderBy=hotIndex&desc=&date=1&page=1&sycmToken=27e9f846c&isHot=true'
        return url


def get_sycm_cat_keyword(uid,host,port,user,password,database,initial=0):
    tablename = 'etc_cat_keyword'

    rule = "order by id asc"
        
    projectlist = cat_keyword(host,port,user,password,database,tablename,rule)
##    print(projectlist)
    for project in projectlist:
        time.sleep(2)
##        print((project[0]))
        for devid in (1,2):        
                openRecruit(cat_url(project[0],devid))
                time.sleep(3) 
        
