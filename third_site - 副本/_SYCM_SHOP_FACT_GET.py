#!/usr/bin/python
# encoding:utf8
# All competitors
# Copyright(c)2012 vsu@opensuse.org


import sys,os,MySQLdb,time,datetime
import webbrowser
#os.system('''"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"''')
def getDate(delta_days=0):
    date = (datetime.datetime.now()-datetime.timedelta(delta_days)).strftime("%Y-%m-%d")
    return date

def openRecruit(url):
        webbrowser.open_new_tab(url)
        return webbrowser.get()

def shop_fact(host,port,user,password,database,tablename,rule):
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        queryTask = "SELECT `url` FROM %s.%s %s"
        
        dbconn.execute(queryTask % (database,tablename,rule))
        result = dbconn.fetchall()
        db.commit()
    except Exception,e:
        print(e)
        result = []
    dbconn.close()
    return result

def get_sycm_shop_fact(uid,host,port,user,password,database,initial=0):
    tablename = 'etc_download_sycm'
    rule = ""
    projectlist = shop_fact(host,port,user,password,database,tablename,rule)
##    print(projectlist)
    for project in projectlist:
        time.sleep(3)
        openRecruit(project[0])
        
