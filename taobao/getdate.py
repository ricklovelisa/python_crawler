#!/usr/bin/python
# encoding:utf8
# All competitors
# Copyright(c)2012 vsu@opensuse.org

import time

class newdate:
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.aids = None
		self.fields = None

	def getDate(self):
		return 'taobao.bill.accounts.get'
