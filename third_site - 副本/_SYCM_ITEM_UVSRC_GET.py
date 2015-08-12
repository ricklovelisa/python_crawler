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

def item_uvsrc(host,port,user,password,database,tablename,rule):
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
def item_uvsrc_url(itemid,devid,date_str1,date_str2):
    order_rule = 'expose'
    #url = 'http://bda.sycm.taobao.com/download/excel/items/itemanaly/ItemKeywordAnalysisExcel.do?device=1&itemId='+str(itemid)+'&dateRange='+date_str+'|'+date_str+'&dateType=recent1&order='+order_rule+'&orderType=asc&search=&searchType=taobao'
    #url = 'http://bda.sycm.taobao.com/download/excel/items/itemanaly/ItemTrendExcel.do?dateRange='+date_str1+'|'+date_str2+'&dateType=range&itemId='+str(itemid)+'&device=1'
    url = 'http://bda.sycm.taobao.com/download/excel/items/itemanaly/ItemLev1FromToExcel.do?device='+str(devid)+'&itemId='+str(itemid)+'&dateRange='+date_str1+'|'+date_str2+'&dateType=day&reqIndex=uv'
    # expose
    # avgSeRank
## 
    return url

def get_item_uvsrc(uid,host,port,user,password,database,initial=0):
    tablename = 'dim_auction'
    rule = "where seller_id = '"+str(uid)+"' order by recent_sold_quantity desc limit 100"
    projectlist = item_uvsrc(host,port,user,password,database,tablename,rule)

    #项目初始化使用
    weekday = int(datetime.datetime.now().strftime('%w'))
    if initial == 1:
        id_range = 32
    else:
        if weekday == 1:
            id_range = 4
        else:
            id_range = 2
            
    # 逐个日期执行
    for id in range(1,id_range):
        for project in projectlist:
            time.sleep(1)
            for devid in (1,2):
                openRecruit(item_uvsrc_url(project[0],devid,getDate(id),getDate(id)))
                time.sleep(2)


