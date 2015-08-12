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

def item_sum(host,port,user,password,database,tablename,rule):
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

def item_sum_url(itemid,date_str1,date_str2):
    order_rule = 'expose'
    # expose
    # avgSeRank
    url = 'http://bda.sycm.taobao.com/download/excel/items/itemanaly/ItemTrendExcel.do?dateRange='+date_str1+'|'+date_str2+'&dateType=range&itemId='+str(itemid)+'&device=1'
    return url
    
def get_item_sum(uid,host,port,user,password,database,initial=0):

    tablename = 'dim_auction'
    rule = "where seller_id = '"+str(uid)+"' order by auction_id asc"
    projectlist = item_sum(host,port,user,password,database,tablename,rule)
##    print(projectlist)
    for project in projectlist:        
        openRecruit(item_sum_url(project[0],getDate(8),getDate(1)))
        time.sleep(3)
        

