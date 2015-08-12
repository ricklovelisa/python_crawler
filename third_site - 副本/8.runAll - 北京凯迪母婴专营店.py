# -*- coding: gbk -*-
from __future__ import print_function
import os,sys,re
from _SYCM_SHOP_FACT_GET import *
from _SYCM_CAT_KEYWORD_SYCM_GET import *
from _SYCM_ITEM_SUM_GET import *
from _SYCM_ITEM_KEYWORD_GET import *
from _SYCM_ITEM_UVSRC_GET import *

# README
# 使用说明:
# 配置项目对应的数据库
# 如果第一次运行，则需要将<初始化>参数设置为 1
# END
def main():
    
    host = '192.168.1.90'
    port = 33060
    user = 'kettle'
    password = 'root'
    database = 'db_762410960'
    uid = 762410960
    # <生意参谋下载行业关键词的URL>参数 
    token = '9aa4c520a'
    # <初始化>参数
    initial = 0
    
    get_sycm_shop_fact(uid,host,port,user,password,database,initial)
    get_sycm_cat_keyword(uid,token,host,port,user,password,database,initial)
    get_item_sum(uid,host,port,user,password,database,initial)
    get_item_keyword(uid,host,port,user,password,database,initial)
    get_item_uvsrc(uid,host,port,user,password,database,initial)

if __name__ == "__main__":
    main()
