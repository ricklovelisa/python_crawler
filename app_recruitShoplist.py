#!/usr/bin/python
# encoding:utf8
# All competitors
# Copyright(c)2012 vsu@opensuse.org


import sys,os,MySQLdb,time
import webbrowser
os.system('"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"')

def openRecruit(uid):
        url = 'http://qudao.gongxiao.tmall.com/supplier/json/invite_result_json.htm?action=user/invitation_action&event_submit_do_invite=t&_input_charset=utf-8&&_ksTS=1402050059791_95&trade_type=1&userIdNum='+str(uid)
##        url = uid
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
    main()
##    print(openRecruit('baidu.com'))
