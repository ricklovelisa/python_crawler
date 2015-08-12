#!/usr/bin/python
# encoding:utf8
# All competitors
# Copyright(c)2012 vsu@opensuse.org


import sys,os,MySQLdb,time

def getDate(delta_days=0):
    date = (datetime.datetime.now()-datetime.timedelta(delta_days)).strftime("%Y-%m-%d")
    return date

def getTask(host,port,user,password,database,tablename,rule):
    db=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=database,charset="utf8")
    dbconn=db.cursor()
    try:
        queryTask = "SELECT `cat_id` FROM %s.%s %s"
        dbconn.execute(queryTask % (database,tablename,rule))
        result = dbconn.fetchall()
        db.commit()
    except Exception,e:
        print(e)
        result = []
    dbconn.close()
    return result
def geturl(cid):
    url = 'http://app.gxt.alibaba.com/panoramic/proxy/api/v1/gql?app=panoramic&sql=select+group_count%28tag_amt_alipay_pre_month%29%2Cgroup_count%28tag_num_alipay_pre_month%29%2Cgroup_count%28tag_age_level_id%29%2Cgroup_count%28tag_gender%29%2Cgroup_count%28tag_buy_grade%29%2Cgroup_count%28tag_education%29%2Cgroup_count%28vip_level%29%2Cgroup_count%28tag_star_level_id%29%2Cgroup_count%28china_regions%29%2Cgroup_count%28city_tier%29%2Cgroup_count%28tag_province_id%29%2Cgroup_count%28tag_career%29%2Cgroup_count%28tag_buy_time_range_most%29+from+datas.cross+where+cat_id+in+%28%27'+str(cid)+'%27%29+and+year_month+%3E%3D+201412+and+year_month+%3C%3D+201506+&_=1433922687682'
    
    return url

def getAria2c(cid,cookie):
    url = geturl(cid)
    command = 'D:\\bin\\aria2c.exe -o "'+str(cid)+'.txt" --load-cookie="'+str(cookie)+'" "'+str(url)+ '"'
    print(command)
    os.system(command)
    return
    
    



    
def main():
    host = '192.168.1.90'
    port = 33060
    user = 'kettle'
    password = 'root'
    database = 'db_831007526'
    tablename = 'dim_itemcat_gxt'

    rule = "order by cat_id asc"
    cookie = 'C:\Users\db\AppData\Roaming\Mozilla\Firefox\Profiles\lvqnhsmk.default\cookies.sqlite'
##    cid = '1512'
    projectlist = getTask(host,port,user,password,database,tablename,rule)
##    getAria2c(cid,cookie)
##    print(projectlist)
    for project in projectlist:
        getAria2c(project[0],cookie)
        time.sleep(2)
        
if __name__ == "__main__":
    main()
##    print(openRecruit('baidu.com'))
