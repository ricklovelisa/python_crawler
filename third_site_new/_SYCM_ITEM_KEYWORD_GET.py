#!/usr/bin/python
# encoding:utf8
# All competitors
# Copyright(c)2012 vsu@opensuse.org


import sys,os,MySQLdb,time,datetime
import webbrowser


def getDate(delta_days=0):
    date = (datetime.datetime.now()-datetime.timedelta(delta_days)).strftime("%Y-%m-%d")
    return date

def openRecruit(url):

    webbrowser.open_new_tab(url)
    return webbrowser.get()

def item_keyword(host,port,user,password,database,tablename,rule):
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        queryTask = "SELECT `auction_id` FROM %s.%s %s"
        #queryTask = "SELECT itemid from raw_crawl_shop_item where updatetime = '2015-5-4' and uid = '831007526' and itemid not in (select auction_id from dim_auction)"
        dbconn.execute(queryTask % (database,tablename,rule))
        #dbconn.execute(queryTask)
        result = dbconn.fetchall()
        db.commit()
    except Exception,e:
        print(e)
        result = []
    dbconn.close()
    return result
def item_keyword_url(itemid,date_str):
    order_rule = 'expose'
    url = 'http://bda.sycm.taobao.com/download/excel/items/itemanaly/ItemKeywordAnalysisExcel.do?device=1&itemId='+str(itemid)+'&dateRange='+date_str+'|'+date_str+'&dateType=recent1&order='+order_rule+'&orderType=asc&search=&searchType=taobao'
    # expose
    # avgSeRank
    return url

def get_item_keyword(uid,host,port,user,password,database,initial=0):
    tablename = 'dim_auction'

    rule = "where seller_id = '"+str(uid)+"' order by auction_id asc"
        
    projectlist = item_keyword(host,port,user,password,database,tablename,rule)

    #项目初始化使用
    weekday = int(datetime.datetime.now().strftime('%w'))
    if initial == 1:
        id_range = 8
    else:
        if weekday == 1:
            id_range = 4
        else:
            id_range = 2
            
    # 逐个日期执行
    for id in range(1,id_range):
        for project in projectlist:
            openRecruit(item_keyword_url(project[0],getDate(id)))
            time.sleep(2)

    

