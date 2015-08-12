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
    
def getAria2c(filename,url,cookie):
    command = 'D:\\bin\\aria2c.exe -o "'+filename+'" --load-cookie="'+str(cookie)+'" "'+str(url)+ '"'
    print(command)
    os.system(command)
    return

def shop_fact(host,port,user,password,database,tablename,rule):
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        queryTask = "SELECT `url`,tag FROM %s.%s %s"
        
        dbconn.execute(queryTask % (database,tablename,rule))
        result = dbconn.fetchall()
        db.commit()
    except Exception,e:
        print(e)
        result = []
    dbconn.close()
    return result

def get_sycm_shop_fact(cookies,prefix,uid,host,port,user,password,database,initial=0):
    tablename = 'etc_download_sycm'
    rule = ""
    home_dir = '/data/download/'+str(uid)+'/'
    projectlist = shop_fact(host,port,user,password,database,tablename,rule)
##    print(projectlist)
    for project in projectlist:
        time.sleep(3)
        url = project[0]
        filename = home_dir + str(uid) + '_' + prefix + project[1]+ getDate() + '.xls'
        getAria2c(filename,url,cookies)
        
        
