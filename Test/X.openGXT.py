#!/usr/bin/python
# encoding:utf8
# All competitors
# Copyright(c)2012 vsu@opensuse.org


import sys,os,MySQLdb,time
import webbrowser
from selenium import webdriver
os.system('"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"')

def openRecruit(url):
        webbrowser.open_new_tab(url)
        return webbrowser.get()

def getTask(host,user,password,database,tablename,rule):
    db=MySQLdb.connect(host=host,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        queryTask = "SELECT `uid` FROM %s.%s %s"
        
        dbconn.execute(queryTask % (database,tablename,rule))
        result = dbconn.fetchall()
        db.commit()
    except Exception,e:
        print(e)
        result = []
    dbconn.close()
    return result

def main():
    host = '192.168.1.90'
    user = 'kettle'
    password = 'root'
    database = 'db_daifuni'
    tablename = 'meta_recruit_shoplist'
    rule = "where uid is not null  and group_id = '4004' limit 500"
        
    projectlist = getTask(host,user,password,database,tablename,rule)
    print(projectlist)
    for project in projectlist:
        time.sleep(3)
        openRecruit(project[0])
        
if __name__ == "__main__":
    print(openRecruit('http://baidu.com'))
##    main()
##    print(openRecruit('http://app.gxt.alibaba.com/panoramic/proxy/api/v1/gql?app=panoramic&sql=%20select%20count(distinct%20user_id),%20user_brand_brand_id%20from%20datas.cross%20where%20cat_id%20in%20(%271512%27)%20and%20user_brand_cat_id%20in%20(50014050,1512)%20and%20year_month%20%3E=%20201402%20and%20year_month%20%3C=%20201408%20group%20by%20user_brand_brand_id%20order%20by%20count(distinct%20user_id)%20desc%20limit%200,1000'))

