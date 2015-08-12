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
import mysql.connector
#import yaml


def getDate():
    date=time.strftime("%Y-%m-%d",time.localtime())
    return date

def getTask(host,user,password,database,tablename):
    db=MySQLdb.connect(host=host,user=user,passwd=password,db=database,port=33060,charset="utf8")
    dbconn=db.cursor()
    try:
        queryTask = "SELECT pid FROM etc_calc.dim_tag WHERE cid in (SELECT cid FROM %s.%s) GROUP BY pid"
        print(queryTask % (database,tablename))
        dbconn.execute(queryTask % (database,tablename))
        result = dbconn.fetchall()
        db.commit()
    except:
        result = []
    dbconn.close()
    return result

def getSubTask(host,user,password,database,shop_tbname,query_rule):
    # keyword,pagenumber = 1,ratesum = "",location = "",cat = "",brand = "",ppath = "",sort = "sale-desc")
    db=MySQLdb.connect(host=host,user=user,passwd=password,db=database,port=33060,charset="utf8")
    dbconn=db.cursor()
    try:
        queryTask = "SELECT uid FROM %s.%s %s" % (database,shop_tbname,query_rule)
        dbconn.execute(queryTask)
        result = dbconn.fetchall()
        db.commit()
        
    except Exception,e:
        print(e)
        result = []
    dbconn.close()
    return result


def rephrase(data):
    data_colum = data.split(',')
    initial_str = ''
    for i in range(0,len(data_colum)):
        data_column_phrased = "'"+re.sub(":","','",data_colum[i])+"'"
        if i == 0:
            initial_str = initial_str + 'COLUMN_CREATE('+data_column_phrased+')'
        else:
            initial_str = 'COLUMN_ADD(' + initial_str + ',' + data_column_phrased + ')'
    return initial_str

def newmany(data):
    NewSQLString = ''
    newmany = '''('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','''
    newmany2 = ''','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')'''
    for i in range(0,len(data)):
        # Function for DYNAMIC COLUMN
        rephrased_str = rephrase(data[i][38])
        #
        NewSQLString = NewSQLString+newmany %  data[i][:38] + rephrased_str + newmany2 % data[i][39:] +','
    return NewSQLString[:-1]
def crawl_item_data(info):
    host = info[0]
    user = info[1]
    password = info[2]
    database = info[3]
    tbname = info[4]
    keyword = info[5]
    search_rule = info[6]
    uid = info[7]
    
    try:
    	itemdata = getData(uid,keyword,search_rule,4)
    except:
        itemdata =[(getDate(),0,-1,-1,-1,uid,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,NULL,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1)]
    if itemdata == []:
        itemdata =[(getDate(),0,-1,-1,-1,uid,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,NULL,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1)]

    db=MySQLdb.connect(host=host,user=user,passwd=password,db=database,port=33060,charset="utf8")
    dbconn=db.cursor()
    #cnx = mysql.connector.connect(host=host,user=user,passwd=password,db=database,port=33060,charset='utf8',use_unicode = False)
    #dbconn = cnx.cursor()
    #ItemDataInsert = '''INSERT IGNORE INTO '''+str(tbname)+''' (updatetime,total_fee,price,bid,title,uid,quantity,total_sold_quantity,people_num,ordercost,dsr_desc,auction_type,cid,support_cod,support_xcard,spuid,reserve_price,spuprice,old_starts,sellernick,ratesum,shipping_fee,comment_count,isprepay,user_type,promoted_service,auction_tag,auction_tag2,itemid,biz30day,volume30day,zk_time,promotions,promoted_type,options,enddate,activity_id,cc_score1,pidvid,scid,startdate,support_bonus,vip,catmap,tag_price,sku_tagprice_min,sku_tagprice_max,zk_final_min,zk_final_price,zk_time_wap,zk_rate_wap,zk_type_wap,zk_group_wap,zk_final_price_wap,sp_service,ext_discount_price,ext_pict_url) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',COLUMN_CREATE(%s),'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');'''

    NewSQLString = newmany(itemdata)
    NewSQLString = NewSQLString.encode('utf-8')

    ItemDataInsert = "INSERT IGNORE INTO "+str(tbname)+" (updatetime,total_fee,price,bid,title,uid,quantity,total_sold_quantity,people_num,ordercost,dsr_desc,auction_type,cid,support_cod,support_xcard,spuid,reserve_price,spuprice,old_starts,sellernick,ratesum,shipping_fee,comment_count,isprepay,user_type,promoted_service,auction_tag,auction_tag2,itemid,biz30day,volume30day,zk_time,promotions,promoted_type,options,enddate,activity_id,cc_score1,pidvid,scid,startdate,support_bonus,vip,catmap,tag_price,sku_tagprice_min,sku_tagprice_max,zk_final_min,zk_final_price,zk_time_wap,zk_rate_wap,zk_type_wap,zk_group_wap,zk_final_price_wap,sp_service,ext_discount_price,ext_pict_url) VALUES" + NewSQLString
    try:
        dbconn.execute(ItemDataInsert)
    except Exception,e:
        print(e)
    db.commit()
    db.close()

    

    
    
def multiTask(tasklist,host,user,password,database,item_tbname,keyword,search_rule):
    for i in range(0,len(tasklist),20):
        tasktemp = tasklist[i:i+20]
        job=[]
        if i <20:
            print(getDate()+":"+"Begin_Project:"+str(len(tasklist)))
        print(getDate()+":"+"Process:"+str(round((i+10)*100/len(tasklist),0))+"%")
        for j in range(0,len(tasktemp)):
            ptask = (host,user,password,database,item_tbname,keyword,search_rule,tasktemp[j][0])
            # info
            p = multiprocessing.Process(target = crawl_item_data,args=(ptask,))
            p.start()
            job.append(p)
        for p in job:
            p.join()

def do_crawl_item(host,user,password,database,shop_tbname,write_table,keyword,rule):
    rule_json = json.loads(rule.encode('utf-8'))
    query_rule = rule_json["query_rule"]
    search_rule = rule_json["search_rule"]
    taskList = getSubTask(host,user,password,database,shop_tbname,query_rule)
##    multiTask(taskList,host,user,password,database,item_tbname,keyword,search_rule)
    initialTable(host,user,password,database,write_table)
    for j in range(0,len(taskList)):
        ptask = (host,user,password,database,write_table,keyword,search_rule,taskList[j][0])
        crawl_item_data(ptask)
        
def initialTable(host,user,password,database,tbname):
    initial_str = '''CREATE TABLE IF NOT EXISTS '''+str(tbname)+'''( `updatetime` DATE NULL DEFAULT NULL, `uid` BIGINT(20) NULL DEFAULT NULL COMMENT '用户id', `sellernick` VARCHAR(50) NULL DEFAULT NULL COMMENT '卖家昵称', `user_type` INT(11) NULL DEFAULT NULL COMMENT '是否卖家', `ratesum` INT(11) NULL DEFAULT NULL COMMENT '卖家等级', `itemid` BIGINT(20) NULL DEFAULT NULL COMMENT '产品ID', `title` VARCHAR(255) NULL DEFAULT NULL COMMENT '标题', `old_starts` BIGINT(20) NULL DEFAULT NULL COMMENT '宝贝创建日期', `bid` BIGINT(20) NULL DEFAULT NULL, `cid` BIGINT(20) NULL DEFAULT NULL COMMENT '类目', `price` BIGINT(20) NULL DEFAULT NULL, `shipping_fee` FLOAT(15,2) NULL DEFAULT NULL COMMENT '邮费', `dsr_desc` FLOAT(5,2) NULL DEFAULT NULL COMMENT '描述评分', `ordercost` INT(11) NULL DEFAULT NULL COMMENT '宝贝收藏量', `people_num` INT(11) NULL DEFAULT NULL COMMENT '客户数', `total_sold_quantity` INT(11) NULL DEFAULT NULL COMMENT '总销量', `quantity` INT(11) NULL DEFAULT NULL COMMENT '库存', `biz30day` INT(11) NULL DEFAULT NULL COMMENT '30天成交', `auction_type` VARCHAR(2) NULL DEFAULT NULL, `support_cod` INT(11) NULL DEFAULT NULL COMMENT '货到付款', `support_xcard` INT(11) NULL DEFAULT NULL COMMENT '信用卡', `spuid` BIGINT(20) NULL DEFAULT NULL COMMENT 'SKU识别码', `reserve_price` FLOAT(15,2) NULL DEFAULT NULL COMMENT '标签价格', `spuprice` FLOAT(15,2) NULL DEFAULT NULL, `comment_count` INT(11) NULL DEFAULT NULL COMMENT '评价数量', `isprepay` INT(11) NULL DEFAULT NULL COMMENT '预付', `promoted_service` INT(11) NULL DEFAULT NULL COMMENT '7天退换货', `auction_tag` VARCHAR(255) NULL DEFAULT NULL COMMENT '促销标签', `auction_tag2` VARCHAR(255) NULL DEFAULT NULL COMMENT '促销标签2', `volume30day` INT(11) NULL DEFAULT NULL COMMENT '30天售出', `total_fee` INT(11) NULL DEFAULT NULL, `zk_time` BIGINT(20) NULL DEFAULT NULL, `promotions` INT(11) NULL DEFAULT NULL COMMENT '促销幅度%', `promoted_type` INT(11) NULL DEFAULT NULL COMMENT '促销类型', `options` BIGINT(20) NULL DEFAULT NULL, `startdate` BIGINT(20) NULL DEFAULT NULL, `enddate` BIGINT(20) NULL DEFAULT NULL, `activity_id` VARCHAR(500) NULL DEFAULT NULL, `cc_score1` FLOAT(15,6) NULL DEFAULT NULL, `pidvid` blob, `scid` VARCHAR(500) NULL DEFAULT NULL, `support_bonus` INT(11) NULL DEFAULT NULL, `vip` INT(11) NULL DEFAULT NULL COMMENT '支持vip折扣', `catmap` VARCHAR(255) NULL DEFAULT NULL, `tag_price` VARCHAR(50) NULL DEFAULT NULL COMMENT '标签价格', `sku_tagprice_max` VARCHAR(50) NULL DEFAULT NULL COMMENT 'SKU最高标价', `sku_tagprice_min` VARCHAR(50) NULL DEFAULT NULL COMMENT 'SKU最低标价', `zk_final_price` FLOAT(15,2) NULL DEFAULT NULL COMMENT '最高售价', `zk_final_min` FLOAT(15,2) NULL DEFAULT NULL COMMENT '最低售价', `ext_discount_price` FLOAT(15,2) NULL DEFAULT NULL COMMENT '最低折扣价', `zk_time_wap` BIGINT(20) NULL DEFAULT NULL COMMENT '手机时间', `zk_rate_wap` INT(11) NULL DEFAULT NULL COMMENT '手机评价', `zk_type_wap` VARCHAR(50) NULL DEFAULT NULL COMMENT '手机活动类型', `zk_group_wap` VARCHAR(50) NULL DEFAULT NULL COMMENT '手机支持', `zk_final_price_wap` FLOAT(15,4) NULL DEFAULT NULL COMMENT '手机售价', `sp_service` VARCHAR(50) NULL DEFAULT NULL COMMENT '其他信息', `ext_pict_url` VARCHAR(255) NULL DEFAULT NULL COMMENT '图片地址', UNIQUE INDEX `itemid` (`itemid`, `updatetime`) ) COLLATE='utf8_general_ci' ENGINE=InnoDB;'''
    db=MySQLdb.connect(host=host,user=user,passwd=password,db=database,port=33060,charset="utf8")
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
##    conf_file = open('/etc/crawl/item_conf')
##    conf = yaml.load(conf_file)
##    host = conf['host']
##    user = conf['user']
##    password = conf['password']
##    database = conf['database']
##    tablename = conf['tablename']
    host = 'localhost'
    user = 'kettle'
    password = 'root'
    database = 'db_test'
    tablename = 'crawl_shop_item'
    try:
        itemstage = sys.argv[1]
    except:
        itemstage = 2
    projectlist = getTask(host,user,password,database,tablename)
    #print(projectlist)
    #for project in projectlist:
    #    do_crawl_item(host,user,password,project[0],project[1],project[2],project[3],project[4])
if __name__ == "__main__":
    main()
    
