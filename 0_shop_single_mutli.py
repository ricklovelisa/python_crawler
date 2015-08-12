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
import yaml

#tracking datetime begin
def getDate():
    date=time.strftime("%Y-%m-%d",time.localtime())
    return date
def getTask(host,port,user,password,database,tablename,itemstage = 1):
    db=MySQLdb.connect(host=host,user=user,passwd=password,db=database,port=port,charset="utf8")
    dbconn=db.cursor()
    try:
        queryTask = "SELECT `dbname`,r_table,w_table,keyword,rule FROM %s.%s WHERE taskid = '%s'"
        print(queryTask % (database,tablename,itemstage))
        dbconn.execute(queryTask % (database,tablename,itemstage))
        result = dbconn.fetchall()
        db.commit()
    except:
        result = []
    dbconn.close()
    return result

def makeOpener():
    # 代理 IP 使用
    # post cookie
    cookie=cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cookie)
    opener=urllib2.build_opener(cookie_support,urllib2.HTTPHandler)
    return opener

def openPage(opener,keyword,pagenumber,rule):
    #
    # keyword : 关键词
    # pagenumber : 页数
    # ratesum : 等级选择
    # location : 地址选择
    # cat ：类目选择
    # brand ：品牌选择
    # ppath ：客户喜欢选择
    # sort ： 排序方式可选 sale-desc/credit-desc
    #
    
    keyword = urllib.quote(keyword.encode("utf8"))
    pagenumber = int(pagenumber) -1
    urllib2.install_opener(opener)

    url='http://s.taobao.com/search?q='+keyword+'&app=shopsearch'+str(rule)+'&cps=1&fs=1&sort=&spm=1.1000386.5803581.d4908513&initiative_id=tbindexz_'+time.strftime("%Y%m%d",time.localtime())+'&s='+str(pagenumber*20)
    url_referer='http://s.taobao.com/search?q='+keyword+'&app=shopsearch'+str(rule)+'&cps=1&fs=1&sort=&spm=1.1000386.5803581.d4908513&initiative_id=tbindexz_'+time.strftime("%Y%m%d",time.localtime())+'&s='+str((pagenumber-1)*20)
    if pagenumber == 0:
        print(url)
    headers = {
        "GET":url,
        "Accept":"*/*",
        "Connection":"keep-alive",
        "Host":"s.taobao.com",
        "Referer":url_referer,
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.69 Safari/537.36"
        }
    
    req=urllib2.Request(url)
    for header in headers:
        req.add_header(header,headers[header])
    page=opener.open(req)
    # 页面打开错误返回类型
    return page
def soupPage(page,encode = "utf8"):
    # Soup the Page
    soup=BeautifulSoup(page,fromEncoding=encode)
    return soup
def getPageSize(soup):
    pagesize = soup.findAll(attrs={"class":"shop-count"})
    print(pagesize)
    print("$$$$$$$$$$$$$$$$$$$")
    print(str(pagesize[0]))
    print("###################")
    full_pagenum = int(re.findall('<b>(\d+)</b>',str(pagesize))[0])/20
    print(full_pagenum)
    return full_pagenum
def getData(soup,pageno):
    shoplist = soup.findAll(attrs={"class":"list-item"})
    z = len(shoplist)
##    if pageno == 64:
##        print(shoplist)
    data =[]
    for x in range(0,len(shoplist)):
##        print(x+1,end="")
        shoplist_data = re.sub(r'\r|\n|\t','',str(shoplist[x]))
        shoplist_data = re.sub("&lt;","<",shoplist_data)
        shoplist_data = re.sub("&gt;",">",shoplist_data)
        shoplist_data = re.sub("\s+<","<",shoplist_data)
        shoplist_data = re.sub(">\s+",">",shoplist_data)
        shoplist_data = re.sub("\s\s+","",shoplist_data)
        z=z-1
        if (z+x)!=(len(shoplist)-1):
            print("error:"+str(x)+":",end='')
        try:
            shop_info = re.findall('<h4><a trace="shop" data-uid="(\d+)" href="//shop(\d+).taobao.com" class="shop-name J_shop_name" target="_blank">(.*)</a><a trace="shop" data-uid="',str(shoplist_data))
            #shop_info = re.findall('<h4><a trace="shop" data-uid="(\d+)" href="http://shop(\d+).taobao.com"',str(shoplist_data))
            uid =shop_info[0][0]
            shopid =shop_info[0][1]
            print('>',end="")
            #shopname ="店铺名称将不作更新"
            shopname=re.sub('</span>|<span class="H">|\s+','',shop_info[0][2])
            #print(shop_info)
            #shopname = re.sub('</span>|<span class="H">',"",re.findall('<a trace="shop" data-uid="\d+" href="http://shop\d+.taobao.com" class="shop-name J_shop_name" target="_blank">?\n(.*)</a>',str(shoplist_data))[0].strip())
        except:
            uid ='-1'
            shopid ='-1'
            print(":shopid_error:",end="")
            shopname = '-1'

        try:
            mainsell = re.sub('</span>|<span class="H">',"",re.findall('<p class="main-cat"><label>主营:</label><a trace="shop" data-uid="\d+" href="http://shop\d+.taobao.com" target="_blank">(.*)</a></p><p class="shop-info">',str(shoplist_data))[0])
        except:
            mainsell = '-1'
        try:
            sellernick = re.sub('</span>|<span class="H">',"",urllib.unquote(re.findall('<span class="J_WangWang" data-encode="true" data-nick="(.*)" data-display="inline" data-item="\d+"',str(shoplist_data))[0]))
        except:
            sellernick = '-1'
            print(":sellernick_error:",end="")
        try:
            address = re.findall('<span class="shop-address">(\W+)<',str(shoplist_data))[0]
        except:
            address = '-1'
        try:
            sales = re.findall('<span class="info-sale">\W+<em>(\d+)',str(shoplist_data))[0]
        except:
            sales = '-1'
        try:
            number = re.findall('<span class="info-sum">\W+<em>(\d+)',str(shoplist_data))[0]
        except:
            number = '-1'
        try:
            itemnew = re.findall('上新<span>(\d+)</span>',str(shoplist_data))[0]
        except:
            itemnew = '-1'
        try:
            itempromo = re.findall('上新<span>(\d+)</span>',str(shoplist_data))[0]
        except:
            itempromo = '-1'
        try:
            data_dsr = re.findall('data-dsr=.({.*}).><div class="descr-icon">',shoplist_data)
            dsr = json.loads(data_dsr[0].decode("utf8"))
            
            '''总好评数量'''
            ratenumber = int(dsr["srn"])
            
            
            '''主营类目好评数占比'''
            rate = float(re.sub("%","",dsr["sgr"]))/100
            
            
            '''描述相符度'''
            dsr_desc = float(dsr["mas"])
            
            '''描述相符度高于行业'''
            mg = float(re.sub("%","",dsr["mg"]))/100
            
            '''服务态度'''
            dsr_srv = float(dsr["sas"])
            
            '''服务态度高于行业'''
            sg = float(re.sub("%","",dsr["sg"]))/100
            
            '''发货速度'''
            dsr_ship = float(dsr["cas"])
            
            '''发货速度高于行业'''
            cg = float(re.sub("%","",dsr["cg"]))/100

            '''uid_encrypted'''
            uid_encrypted = dsr["encryptedUserId"]
            
            maincat = "TB_NoData"
        except:
            ratenumber = '0'
            '''主营类目好评数占比'''
            rate =  '0'
            '''主营类目'''
            maincat =  '-1'
            '''描述相符度'''
            dsr_desc =  '0'
            '''描述相符度高于行业'''
            mg = '0'
            '''服务态度'''
            dsr_srv = '0'
            '''服务态度高于行业'''
            sg =  '0'
            '''发货速度'''
            dsr_ship = '0'
            '''发货速度高于行业'''
            cg = '0'

            uid_encrypted = '-1'

            maincat = "TB_NoData"
        '''天猫店铺没有此类数据'''
        try:
            rank = re.findall('class="rank (seller-rank-\d+)" target="_blank">',str(shoplist_data))[0]
            shoptype = '0'
        except:
            rank = ''
            shoptype = '1'
        try:
            goodcomment = float(re.findall('<div class="good-comt">\W+(\d+.\d+)%</div>',str(shoplist_data))[0])/100
        except:
            goodcomment = '0'
        datatemp = (pageno,shopid,sellernick,shopname,shoptype,mainsell,maincat,address,number,sales,itemnew,itempromo,uid,uid_encrypted,rank,ratenumber,rate,goodcomment,dsr_desc,dsr_srv,dsr_ship,mg,sg,cg)
        if x>0 :
            data.append(datatemp)
        else:
            data = [datatemp]
    return data
def do_crawl_shop(tasklist):
    try:
        host = tasklist[0]
        port = tasklist[1]
        user = tasklist[2]
        password = tasklist[3]
        database = tasklist[4]
        tablename = tasklist[5]
        keyword = tasklist[6]
        rule_json = json.loads(tasklist[7].encode('utf-8'))
        search_rule = rule_json["search_rule"]
    except Exception,e:
        
        print("project_could_not_take_task",e)
    #  单个项目设定单个跟踪 cookie 防止其他问题产生
    opener = makeOpener()
    # 关键词由数据库读取
    soup = soupPage(openPage(opener,keyword,1,search_rule),"gbk")
    pagenumber = getPageSize(soup)
    # 循环页面抽取结果可换作多线程
    datestr = time.strftime("%Y-%m-%d",time.localtime())+":"
    print("\n"+datestr+database+":"+tablename+":",end='')
    for i in range(1,pagenumber+1):
        print('Done'+str(i)+"-")
        resulttemp = getData(soupPage(openPage(opener,keyword,i,search_rule),"gbk"),i)
        j = 1
        if i>0 :
            if j > 0:
                j = 1
                result = resulttemp
                db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
                dbconn=db.cursor()
                DataInsert = "REPLACE INTO "+tablename+" (updatetime,pageno,shopid,sellernick,shopname,shoptype,mainsell,maincat,address,item_num,sales,item_new_num,item_promo_num,uid,uid_encrypted,rank,rate_num,good_comment_rate,good_comment_num,dsr_desc,dsr_srv,dsr_ship,mg,sg,cg,keyword) VALUES ('"+time.strftime("%Y-%m-%d",time.localtime())+"',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'"+keyword+"')"
                dbconn.executemany(DataInsert,result)
                db.commit()
                db.close()
                result = resulttemp
            else:
                result.extend(resulttemp)
                j = j +1
	    
        else:
            result = resulttemp
            j = 1

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

##    print(result)
def multiTask(tasklist,host,port,user,password):
    for i in range(0,len(tasklist),10):
        task = tasklist[i:i+10]
        job=[]
        if i <10:
            print(getDate()+":"+"Begin_Project:"+str(len(tasklist)))
        print(getDate()+":"+"Process:"+str(round((i+10)*100/len(tasklist),0))+"%")
        for j in range(0,len(task)):
            print(task[j])
            ptask = (host,port,user,password,task[j][0],task[j][2],task[j][3],task[j][4]) 
##            print(getDate()+":"+"Begin_Shop:"+str(len(tasktemp)))
            p = multiprocessing.Process(target = do_crawl_shop,args=(ptask,))
            p.start()
            job.append(p)
        for p in job:
            p.join()
def runJob(task,host,port,user,password,shoplist_table):
    for j in range(0,len(task)):
        initialTable(host,port,user,password,task[j][0],task[j][2],shoplist_table)
        do_crawl_shop((host,port,user,password,task[j][0],task[j][2],task[j][3],task[j][4]))
            
def main():
    #########################################################
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
    initial_str = sql['raw_crawl_shop_list']

    #########################################################
    try:
        shopstage = sys.argv[1]
    except:
        shopstage =2016
    #for shopstage in range(0,1):       
    tasklist = getTask(host,port,user,password,database,tablename,shopstage)
    if tasklist == 0:
        print("no task")
    else:
        runJob(tasklist,host,port,user,password,initial_str)

if __name__ =="__main__":
    main()

