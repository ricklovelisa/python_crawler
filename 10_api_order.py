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
import yaml

def getDate():
    date=time.strftime("%Y-%m-%d",time.localtime())
    return date

def getTask(host,port,user,password,database,tablename,itemstage = 1):
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        queryTask = "SELECT `dbname`,`r_table`,`w_table`,rule FROM %s.%s WHERE taskid = '%s'"
        print(queryTask % (database,tablename,itemstage))
        dbconn.execute(queryTask % (database,tablename,itemstage))
        result = dbconn.fetchall()
        print(host,port,user,password,database,tablename)
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
        queryTask = "SELECT dbname,appkey,secret,sessionkey,seller_id,shop_id FROM %s.%s %s" % (database,read_table,query_rule)
        print(queryTask)
        dbconn.execute(queryTask)
        result = dbconn.fetchall()
        db.commit()
        
    except:
        result = []
        print("Error!SubTask")
    dbconn.close()
    return result

def getApiData(appkey,secret,sessionkey,pageno):
    req=top.api.TradesSoldGetRequest()
    req.set_app_info(top.appinfo(appkey,secret))

    req.fields="seller_nick, buyer_nick, created, tid, pay_time, orders.num, orders.num_iid, orders.sku_id, orders.status, orders.oid, orders.total_fee, orders.payment"
    req.rate_type="get"
    req.role="buyer"
    #req.start_date=startdate
    #req.end_date=enddate
    req.page_no=pageno
    req.page_size=100
    req.use_has_next='true'
    try:
        resp= req.getResponse(sessionkey)
        #print(resp)
    except Exception,e:
        print(e)
        resp = []
    
    dataset = resp.get('trades_sold_get_response').get('trades').get('trade')
    has_next = resp.get('trades_sold_get_response').get('has_next')
    #has_next = False
    return (dataset,has_next)
    
def getData(appkey,secret,sessionkey,seller_id,shop_id):
    data = []
    pageno = 1
    has_next = True
    #startdate,enddate,pageno
    while has_next == True:
        try:
            dataset_tmp = getApiData(appkey,secret,sessionkey,pageno)
            dataset = dataset_tmp[0]
            has_next = dataset_tmp[1]
        except Exception,e:
            print(e)
            has_next = False
            dataset = []
        print('is_continue:',str(pageno),':',has_next)
        pageno = pageno + 1
        for i in range(0,len(dataset)):
            try:
                
                parent_order_id = dataset[i].get('tid')
                seller_id = seller_id
                shop_id = shop_id
                buyer_id = dataset[i].get('buyer_nick')
                gmv_time = dataset[i].get('created')
                pay_time = dataset[i].get('pay_time')

                thedate = time.strftime('%Y-%m-%d',time.strptime(gmv_time,'%Y-%m-%d %H:%M:%S'))
     
                order_detail_data = dataset[i].get('orders').get('order')
                try:
                    for j in range(0,len(order_detail_data)):
                        order_id = order_detail_data[j].get('oid')
                        auction_id = order_detail_data[j].get('num_iid')
                        gmv_trade_amt = order_detail_data[j].get('total_fee')
                        gmv_auction_num = order_detail_data[j].get('num')
                        pay_amt = order_detail_data[j].get('payment')
                        order_status = order_detail_data[j].get('status')
                        sku_id = order_detail_data[j].get('sku_id')
                        
                        datatemp = (getDate(),thedate,order_id,parent_order_id,seller_id,shop_id,buyer_id,gmv_time,pay_time,auction_id,sku_id,gmv_trade_amt,gmv_auction_num,pay_amt,order_status)
                        data.append(datatemp)
                        
                except Exception,e:
                    print('Phrase/Data/Error',e)

            except Exception,e:
                print(e)
                print("nodata")
    return data

def api_data(info):
    host = info[0]
    port = info[1]
    user = info[2]
    password = info[3]
    database = info[4]
    tbname = info[5]
    appkey = info[6]
    secret = info[7]
    sessionkey = info[8]
    seller_id = info[9]
    shop_id = info[10]
    try:
        data = getData(appkey,secret,sessionkey,seller_id,shop_id)
        #print(data)
        db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
        dbconn=db.cursor()
        ItemDataInsert = "INSERT INTO "+str(tbname)+" (updatetime,thedate,order_id,parent_order_id,seller_id,shop_id,buyer_id,gmv_time,pay_time,auction_id,sku_id,gmv_trade_amt,gmv_auction_num,pay_amt,order_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE order_status = VALUES(order_status)"
        dbconn.executemany(ItemDataInsert,data)
        db.commit()
        db.close()
        print("MeiDeShuo,Done")
    except Exception,e:
        print(e)
        print("No Attrib")
    
    
    
def multiTask(tasklist,host,port,user,password,database,write_table,appkey,secret):
    for i in range(0,len(tasklist),20):
        tasktemp = tasklist[i:i+20]
        job=[]
        if i <20:
            print(getDate()+":"+"Begin_Project:"+str(len(tasklist)))
        print(getDate()+":"+"Process:"+str(round((i+10)*100/len(tasklist),0))+"%")
        for j in range(0,len(tasktemp)):
            ptask = (host,port,user,password,database,write_table,appkey,secret,tasktemp[j][0])
            # info
            p = multiprocessing.Process(target = api_pidvid_data,args=(ptask,))
            p.start()
            job.append(p)
        for p in job:
            p.join()

def initialTable(host,port,user,password,database,tbname,initial_sql):
    initial_str = initial_sql % str(tbname)
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



def do_run(host,port,user,password,database,read_table,write_table,rule,initial_sql):
    rule_json = json.loads(rule.encode('utf-8'))
    query_rule = rule_json["query_rule"]
    taskList = getSubTask(host,port,user,password,database,read_table,query_rule)
##    multiTask(taskList,host,user,password,database,write_table,appkey,secret)
    print("Total_task:",str(len(taskList)))
    for j in range(0,len(taskList)):
        initialTable(host,port,user,password,taskList[j][0],write_table,initial_sql)
        ptask = (host,port,user,password,taskList[j][0],write_table,taskList[j][1],taskList[j][2],taskList[j][3],taskList[j][4],taskList[j][5])
        api_data(ptask)

def main():
    # Connection Database
    conf_file_path = sys.path[0]+"/conf/crawl.conf"
    conf_file = open(conf_file_path)
    conf = yaml.load(conf_file)
    
    host = conf['host']
    port = conf['port']
    user = conf['user']
    password = conf['password']
    database = conf['conf_database']
    tablename = conf['conf_table']

    # Read initial_sql_table
    sql_file_path = sys.path[0]+"/conf/sql.ini"
    sql_file = open(sql_file_path)
    sql = yaml.load(sql_file)

    # SQL Section
    comment_table = sql['top_api_shop_order']

    try:
        itemstage = sys.argv[1]
    except:
        itemstage = 10
    projectlist = getTask(host,port,user,password,database,tablename,itemstage)
    for project in projectlist:
        do_run(host,port,user,password,project[0],project[1],project[2],project[3],comment_table)
if __name__ == "__main__":
    main()

##CREATE TABLE `src` (
##	`sellernick` VARCHAR(50) NULL DEFAULT NULL,
##	`sessionkey` VARCHAR(255) NULL DEFAULT NULL,
##	`appkey` VARCHAR(255) NULL DEFAULT NULL,
##	`secret` VARCHAR(255) NULL DEFAULT NULL
##)
##COLLATE='utf8_general_ci'
##ENGINE=InnoDB;

##Session
##https://oauth.taobao.com/authorize?response_type=token&client_id=21786895
