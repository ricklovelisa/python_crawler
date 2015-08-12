# -*- coding: gbk -*-
from __future__ import print_function
import os,sys,re
from _SYCM_SHOP_FACT_GET import *
from _SYCM_CAT_KEYWORD_SYCM_GET import *
from _SYCM_ITEM_SUM_GET import *
from _SYCM_ITEM_KEYWORD_GET import *
from _SYCM_ITEM_UVSRC_GET import *

# README
# ʹ��˵��:
# ������Ŀ��Ӧ�����ݿ�
# �����һ�����У�����Ҫ��<��ʼ��>��������Ϊ 1
# END
def main():
    
    host = '192.168.1.90'
    port = 33060
    user = 'kettle'
    password = 'root'
    database = 'db_1069756170'
    uid = 1069756170
    # <�����ı������ҵ�ؼ��ʵ�URL>����
    # ???token������û�д���
    token = '9eb58791a'
    # <��ʼ��>����
    initial = 0
    
    get_sycm_shop_fact(uid,host,port,user,password,database,initial)
    get_sycm_cat_keyword(uid,token,host,port,user,password,database,initial)
    get_item_sum(uid,host,port,user,password,database,initial)
    get_item_keyword(uid,host,port,user,password,database,initial)
    get_item_uvsrc(uid,host,port,user,password,database,initial)

if __name__ == "__main__":
    main()
