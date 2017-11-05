#!/usr/bin/python
# -*- coding:utf8 -*-
import sys,os,xlrd,re,datetime,dateutil.relativedelta
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HelloWorld.settings")
import django
django.setup()
from HWapp.models import HWapp
reload(sys)
sys.setdefaultencoding('utf8')
 

class xlsMethod(object):

	def int2date(self,f=datetime.date(1899,12,30),t=35411):
		return f+dateutil.relativedelta.relativedelta(days=+t)

	def __init__(self,filename):
		data = xlrd.open_workbook(filename)
		self.table = data.sheets()[0]

	def prog(self):
		table=self.table
		xls = {}
		xls["class"]=re.findall(r'[AaBb]\d{4}',table.row_values(0)[0])[0]
		xls["bzr"]=re.findall(re.compile(u"班主任：([\S]+)"),table.row_values(1)[0])[0]
		xls["classroom"]=re.findall(re.compile(u"教室：([\S]+)"),table.row_values(1)[0])[0]
		xls["stu"]=[]
		for no in range(table.nrows-3):
			xls["stu"].append({})
			for i in range(len(table.row_values(2))):
				if type(table.row_values(no+3)[i]) == float:
					if u"出生" in table.row_values(2)[i]:
						#print "float"
						xls['stu'][no][table.row_values(2)[i]]=self.int2date(t=int(table.row_values(no+3)[i]))
					else:
						xls['stu'][no][table.row_values(2)[i]]=int(table.row_values(no+3)[i])
				else:
					xls['stu'][no][table.row_values(2)[i]]=table.row_values(no+3)[i]
		return xls

	def add(self,xls):
		for i in xls["stu"]:
			stu = HWapp()
			stu.banji = xls["class"]
			stu.id=i[u"学号"]
			stu.name=i[u"姓名"]
			if i[u"性别"] == u"男":
				stu.xingbie=1
			elif i[u"性别"] == u"女":
				stu.xingbie=2
			if u"团员" in i[u"政治面貌"]:
				stu.zhengzhimianmao=1
			elif u"党员" in i[u"政治面貌"]:
				stu.zhengzhimianmao=2
			else:
				stu.zhengzhimianmao=3
			stu.qingshi=i[u"寝室号"]
			stu.shengri=i[u"出生年月"]
			try:
				stu.save()
			except Exception as e:
				print stu
				print i[u"出生年月"]

a= xlsMethod("./1.xls")
p = a.prog()
#for j in p['stu']:
	#for i in j:
		#print "% 6s\t%s"%(i,j[i])
a.add(p)
