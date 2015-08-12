#!/usr/bin/python
# -*- coding: utf-8 -*-
# All competitors
# Copyright(c)2012 vsu@opensuse.org


import top.api

##    url = "http://localhost"
#    port = "80"
appkey = "21786895"
secret = "934fe5351c6d2c2a506aa97fdbd445b1"
req=top.api.ItemcatsGetRequest()
req.set_app_info(top.appinfo(appkey,secret))
req.parent_cid=0
req.fields="cid,parent_cid,name,is_parent"
try:
	resp= req.getResponse()
	print("Fetched")
except Exception,e:
	print(e)
dataset = resp.get('itemcats_get_response').get('item_cats').get('item_cat')
print(dataset)

