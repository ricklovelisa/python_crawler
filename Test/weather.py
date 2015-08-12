#!/usr/bin/python
# encoding:utf8
# Copyright(c)2012 vsu@opensuse.org

from __future__ import print_function
import sys,os,MySQLdb
import urllib2,urllib,time,datetime,re,socket,cookielib,random
import json
from BeautifulSoup import BeautifulSoup
import multiprocessing
#import yaml


def getDate():
    date=time.strftime("%Y-%m-%d",time.localtime())
    return date
def unixTime(timestr):
    value = time.gmtime(timestr)
    format = '%Y-%m-%d %H:%M:%S'
    return time.strftime(format,value)

def makeDate(datestr):
    date_ori = datetime.datetime.strptime(datestr.encode('utf-8'),'%Y年%m月%d日')
    date0 = datetime.datetime.strftime(date_ori,'%Y-%m-%d')
    date1 = datetime.datetime.strftime(date_ori + datetime.timedelta(days=1),'%Y-%m-%d')
    date2 = datetime.datetime.strftime(date_ori + datetime.timedelta(days=2),'%Y-%m-%d')
    date3 = datetime.datetime.strftime(date_ori + datetime.timedelta(days=3),'%Y-%m-%d')
    date4 = datetime.datetime.strftime(date_ori + datetime.timedelta(days=4),'%Y-%m-%d')
    date5 = datetime.datetime.strftime(date_ori + datetime.timedelta(days=5),'%Y-%m-%d')
    
    return [date0,date1,date2,date3,date4,date5]

def minmaxTemp(temp):
    tempdata = re.findall('(\d+).*?~(\d+)',temp)[0]
    return tempdata                                                           

def getTask(host,port,user,password,database,tablename,itemstage = 1):
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        queryTask = "SELECT `dbname`,r_table,w_table,rule FROM %s.%s WHERE taskid = '%s'"
        dbconn.execute(queryTask % (database,tablename,itemstage))
        result = dbconn.fetchall()
        db.commit()
    except:
        result = []
    dbconn.close()
    return result

def getSubTask(host,port,user,password,database,src_tbname,query_rule):
    # keyword,pagenumber = 1,ratesum = "",location = "",cat = "",brand = "",ppath = "",sort = "sale-desc")
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        queryTask = "SELECT cityid FROM %s.%s %s" % (database,src_tbname,query_rule)
        dbconn.execute(queryTask)
        result = dbconn.fetchall()
        print(result)
        db.commit()
        
    except Exception,e:
        print(e)
        result = []
    dbconn.close()
    return result
def getIp(host,port,user,password,database,tbname):
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        queryTask = "SELECT ipaddress,ipport FROM %s.%s where is_valid = '1' ORDER BY privige ASC limit 1" % (database,tbname)
        print(queryTask)
        dbconn.execute(queryTask)
        result = dbconn.fetchall()
        
    except Exception,e:
        print(e)
        result = []
    dbconn.close()
    return result

def markBannedIp(host,port,user,password,database,tbname,ip):
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        queryTask = "UPDATE %s.%s SET is_valid = '0' WHERE ipaddress = '%s' and ipport = '%s'" % (database,tbname,ip[0][0],ip[0][1])
        dbconn.execute(queryTask)
        result = dbconn.fetchall()
        db.commit()
    except Exception,e:
        print(e)
    dbconn.close()
    return


def makeCookie():
    # 代理 IP 使用
    # post cookie
    cookie=cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cookie)
    return cookie_support

def openPage(cityid,ip):
    #
    try:
        ipJson = {'http':'http://'+str(ip[0][0])+':'+str(ip[0][1])}
    except:
        ipJson = {}
    proxy_handler = urllib2.ProxyHandler(ipJson)
    opener=urllib2.build_opener(makeCookie(),urllib2.HTTPHandler,proxy_handler)
##    keyword = urllib.quote(keyword.encode("utf8"))
    urllib2.install_opener(opener)

    url = 'http://m.weather.com.cn/atad/'+str(cityid)+'.html'
    print(url)
    time.sleep(6)
    #url_referer= 'http://item.taobao.com/item.htm?spm=a230r.1.14.82.ReBj7G&id='+str(itemid)+'&ns=1&_u=mua6h780dc1'
    headers = {
        "GET":url,
        "Accept":"*/*",
        "Connection":"keep-alive",
        #"Host":"rate.taobao.com",
        #"Referer":url_referer,
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.69 Safari/537.36"
        }
    
    req = urllib2.Request(url)
    for header in headers:
        req.add_header(header,headers[header])
    page = opener.open(req,None,10)
    
    return page

def soupPage(page,encode="utf8"):
    soup = BeautifulSoup(page,fromEncoding=encode)
    return soup

def reSoup(soup):
    pageData =  re.sub("&gt;",">",str(soup))
    pageData =  re.sub("&lt;","<",str(soup))
    pageData =  re.sub("</span>","",str(soup))
    pageData =  re.sub("<span class=\"H\">","",str(pageData))
    return pageData
def FindJson(pageData):
    try:
        jsonData = json.loads(pageData)
        is_banned = 0
        #print('testtest###',jsonData["weatherinfo"])
    except Exception,e:
        print('#Banned!#',e)
        jsonData = ''
        is_banned = 1
        
    return [jsonData,is_banned]
def phraseWeather(weatherjson):
    try:
        newdate = makeDate(weatherjson["date_y"])
    except Exception,e:
        print('makeDate Error',e)
    
    city = weatherjson["city_en"]
    city_zh = weatherjson["city"]
    systime = weatherjson["fchh"]
    cityid = weatherjson["cityid"]
    

    # indexdate,systime,cid,city,city_zh,maxtemp,mintemp,weather,winddirection,windforce
    # %s,%s,%s,%s,%s,%s,%s,%s,%s,%s
    try:
        day1 = (newdate[0],systime,cityid,city,city_zh,minmaxTemp(weatherjson["temp1"])[0],minmaxTemp(weatherjson["temp1"])[1],weatherjson["weather1"],weatherjson["wind1"],weatherjson["fl1"])
        day2 = (newdate[1],systime,cityid,city,city_zh,minmaxTemp(weatherjson["temp2"])[0],minmaxTemp(weatherjson["temp2"])[1],weatherjson["weather2"],weatherjson["wind2"],weatherjson["fl2"])
        day3 = (newdate[2],systime,cityid,city,city_zh,minmaxTemp(weatherjson["temp3"])[0],minmaxTemp(weatherjson["temp3"])[1],weatherjson["weather3"],weatherjson["wind3"],weatherjson["fl3"])
        day4 = (newdate[3],systime,cityid,city,city_zh,minmaxTemp(weatherjson["temp4"])[0],minmaxTemp(weatherjson["temp4"])[1],weatherjson["weather4"],weatherjson["wind4"],weatherjson["fl4"])
        day5 = (newdate[4],systime,cityid,city,city_zh,minmaxTemp(weatherjson["temp5"])[0],minmaxTemp(weatherjson["temp5"])[1],weatherjson["weather5"],weatherjson["wind5"],weatherjson["fl5"])
        day6 = (newdate[5],systime,cityid,city,city_zh,minmaxTemp(weatherjson["temp6"])[0],minmaxTemp(weatherjson["temp6"])[1],weatherjson["weather6"],weatherjson["wind6"],weatherjson["fl6"])
    except Exception,e:
        print('#2#',e)

    return [day1,day2,day3,day4,day5,day6]
    
    
def PhraseImpressData(impressData,cityid):
    data = []

    try:
        impress = impressData["weatherinfo"] # No Need
        #print(impressData)
        if impress == {}:
            print("city id:",str(cityid))
    except Exception,e:
        print('Impression Data:',e)
        impress = {}
    
    if impress == {}:
        print("weather empty")
    else:
        try:
            tempdata = phraseWeather(impress)
            data.extend(tempdata)
        except:
            print('phraseWeather Error')

    return data

def getSingleData(cityid):
    #Initial
    taskLife = 4
    data = []

    #getData
    updatetime = getDate()
    while taskLife >0:
        ip = getIp('192.168.1.110',33060,'kettle','root','etc_crawl','ip_proxy')
        try:
            page = openPage(cityid,ip).read()
            try:
                soup = page.decode('utf8','ignore')
            except Exception,e:
                print("UTF8 decode Failed:",e)
                soup = page.decode('gbk')
            pageJsonData = FindJson(soup)
            
            
        except Exception,e:
            print('#FindJson Error:',e)
            pageJsonData = [0,1]
            print("TheShitIpProxy,replacing Now")
        if pageJsonData[1] == 1:
            taskLife = taskLife - 1
            markBannedIp('192.168.1.110',33060,'kettle','root','etc_crawl','ip_proxy',ip)
        else:
            try:
                try:
                    
                    fullData = PhraseImpressData(pageJsonData[0],cityid)
                    data.extend(fullData)
                except Exception,e:
                    print('Get Json Error:',e)
                    print('This Item No Impression Data')
                taskLife = 0
            except:
                taskLife = taskLife - 1
                time.sleep(5)
    return data

def crawl_item_data(info):
    host = info[0]
    port = info[1]
    user = info[2]
    password = info[3]
    database = info[4]
    tbname = info[5]
    cityid = info[6]

   
    itemdata = getSingleData(cityid)
    
    print("Wringting...",end='')
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    ItemDataInsert = "REPLACE INTO "+str(tbname)+"(indexdate,systime,cityid,city,city_zh,maxtemp,mintemp,weather,winddirection,windforce) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    dbconn.executemany(ItemDataInsert,itemdata)
    db.commit()
    db.close()
    print("Writen")
    
def multiTask(tasklist,host,port,user,password,database,item_tbname,keyword,search_rule):
    for i in range(0,len(tasklist),20):
        tasktemp = tasklist[i:i+20]
        job=[]
        if i <20:
            print(getDate()+":"+"Begin_Project:"+str(len(tasklist)))
        print(getDate()+":"+"Process:"+str(round((i+10)*100/len(tasklist),0))+"%")
        for j in range(0,len(tasktemp)):
            ptask = (host,port,user,password,database,w_tbname,tasktemp[j][0],tasktemp[j][1])
            # info
            p = multiprocessing.Process(target = crawl_item_data,args=(ptask,))
            p.start()
            job.append(p)
        for p in job:
            p.join()
def initialTable(host,port,user,password,database,tbname):
    initial_str = '''CREATE TABLE IF NOT EXISTS '''+str(tbname)+'''(  `indexdate` DATE NULL DEFAULT NULL,  `updatetime` DATETIME NULL DEFAULT NULL,  `cid` BIGINT(20) NULL DEFAULT NULL,  `city_zh` VARCHAR(10) NULL DEFAULT NULL,  `city` VARCHAR(20) NULL DEFAULT NULL,  `maxtemp` INT(11) NULL DEFAULT NULL,  `mintemp` INT(11) NULL DEFAULT NULL,  `weather` VARCHAR(50) NULL DEFAULT NULL,  `winddirection` VARCHAR(50) NULL DEFAULT NULL,  `windrank` VARCHAR(50) NULL DEFAULT NULL,  UNIQUE INDEX `indexdate_cid` (`indexdate`, `cid`),  INDEX `maxtemp` (`maxtemp`),  INDEX `mintemp` (`mintemp`),  INDEX `city` (`city`),  INDEX `cid` (`cid`),  INDEX `indexdate` (`indexdate`) ) COLLATE='utf8_general_ci' ENGINE=InnoDB; '''
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

def do_crawl_item(host,port,user,password,database,r_tbname,w_tbname,rule):
    rule_json = json.loads(rule.encode('utf-8'))
    query_rule = rule_json["query_rule"]
    search_rule = rule_json["search_rule"]
    taskList = getSubTask(host,port,user,password,database,r_tbname,query_rule)
##    multiTask(taskList,host,user,password,database,item_tbname,keyword,search_rule)
    tasktemp = taskList
    initialTable(host,port,user,password,database,w_tbname)
    for j in range(0,len(tasktemp)):
##    for j in range(0,1):
        print('task:',j,':')
        ptask = (host,port,user,password,database,w_tbname,tasktemp[j][0])
        crawl_item_data(ptask)

def writeStatus(host,port,user,password,database,shopid,pageinfo):
    '''
    Log and current job status sent
    '''
    # keyword,pagenumber = 1,ratesum = "",location = "",cat = "",brand = "",ppath = "",sort = "sale-desc")
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        writeStatus = "REPLACE INTO pool_error_crawl_shop_item (updatetime,shopid,msg) VALUES (%s,%s,%s) "
        dbconn.execute(writeStatus)
        db.commit()
    except:
        result = []
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
    host = '192.168.1.110'
    port = 33060
    user = 'kettle'
    password = 'root'
    database = 'etc_crawl'
    tablename = 'conf'
    try:
        itemstage = sys.argv[1]
    except:
        itemstage = 100
        
    projectlist = getTask(host,port,user,password,database,tablename,itemstage)
    print(projectlist)
    for project in projectlist:
        do_crawl_item(host,port,user,password,project[0],project[1],project[2],project[3])
if __name__ == "__main__":
    main()

## JSON COMMENTS
##{"weatherinfo":{
##//基本信息
##//fchh是系统更新时间
##"city":"北京","city_en":"beijing","date_y":"2011年10月23 日","date":"辛卯年","week":"星期 日","fchh":"11","cityid":"101010100",
##//6天内的温度
##"temp1":"16℃~6℃","temp2":"16℃~3℃","temp3":"16℃~6℃","temp4":"14℃~6℃",
##"temp5":"17℃~5℃","temp6":"18℃~8℃",
##//6天内华氏度
##"tempF1":"60.8℉~42.8℉","tempF2":"60.8℉~37.4℉","tempF3":"60.8℉~42.8℉",
##"tempF4":"57.2℉~42.8℉","tempF5":"62.6℉~41℉","tempF6":"64.4℉~46.4℉",
##//每日天气变化
##"weather1":" 小雨转晴","weather2":"晴","weather3":"晴转阴","weather4":"多云转阴","weather5":"阴转 晴","weather6":"晴转多 云",
##//天气描述（图片序号）
##"img1":"7","img2":"0","img3":"0","img4":"99","img5":"0","img6":"2","img7":"1",
##"img8":"2","img9":"2","img10":"0","img11":"0","img12":"1","img_single":"7",
##//天气描述（文字描述）
##"img_title1":" 小雨","img_title2":"晴","img_title3":"晴","img_title4":"晴","img_title5":" 晴",
##"img_title6":"阴","img_title7":"多云","img_title8":"阴","img_title9":" 阴","img_title10":"晴",
##"img_title11":"晴","img_title12":"多 云","img_title_single":"小雨",
##//风向描述
##"wind1":"北风4-5级","wind2":"北风3-4级转微 风","wind3":"微风","wind4":"微风","wind5":"微风",
##"wind6":"微风","fx1":"北 风","fx2":"北风",
##//风力描述
##"fl1":"4-5级","fl2":"3-4级转小于3级","fl3":"小于3级","fl4":"小于3 级","fl5":"小于3级","fl6":"小于3级",
##//今天穿衣指数
##"index":"温凉","index_d":"较凉爽，建议着夹衣加薄羊毛衫等春秋服 装。体弱者宜着夹衣加羊毛衫。因昼夜温差较大，注意增减衣服。",
##//48小时内穿衣指数
##"index48":"温凉","index48_d":"较凉爽，建议着夹衣加薄羊毛 衫等春秋服装。体弱者宜着夹衣加羊毛衫。因昼夜温差较大，注意增减衣服。",
##//紫外线
##"index_uv":"最弱","index48_uv":"中 等",
##//洗车
##"index_xc":"不宜",
##//旅游
##"index_tr":"适宜",
##//人体舒适度
##"index_co":"较舒 适",
##//未知
##"st1":"14","st2":"3","st3":"14","st4":"5","st5":"15","st6":"5",
##//晨练
##"index_cl":" 较不宜",
##//晾衣
##"index_ls":"不宜",
##//过敏
##"index_ag":"极不易发"}}
##当天基础天气接口
##http://www.weather.com.cn/data/cityinfo/101010100.html
##以下是http://www.weather.com.cn/data/cityinfo/101010100.html接口提供是Json格式提供，数据如下：
##//ptime为系统最后更新时间
##{"weatherinfo":{"city":"北 京","cityid":"101010100","temp1":"16℃","temp2":"6℃","weather":"小雨转 晴","img1":"d7.gif","img2":"n0.gif","ptime":"11:00"}}
##当天基础天气接口
##http://www.weather.com.cn/data/sk/101010100.html
##以下是http://www.weather.com.cn/data/sk/101010100.html接口提供是Json格式提供，数据如下：
##//temp为摄氏度
##//isRadar 应该是雷达返回成功标识
##//Radar是雷达编号
##//time是该数据更新时间
##{"weatherinfo":{"city":"北京","cityid":"101010100","temp":"10","WD":"东北 风","WS":"4 级","SD":"56%","WSE":"4","time":"16:40","isRadar":"1","Radar":"JC_RADAR_AZ9010_JB"}}
