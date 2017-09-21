# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys,os,xlrd,re,datetime,dateutil.relativedelta
from django.db import models
reload(sys)
sys.setdefaultencoding('utf8')
# Create your models here.

class HWapp(models.Model):
	GENDER_CHOICES=((1,'男'),(2,'女'),)
	mianmao_CHOICES=((1,'共青团员'),(2,'党员'),(3,'其他'),)
	id = models.BigIntegerField(primary_key=True)
	banji = models.CharField(max_length=8,default="C0000")
	name = models.CharField(max_length=20)
	xingbie = models.IntegerField(choices=GENDER_CHOICES,default=1)
	shengri = models.DateField(null=True)
	zhengzhimianmao = models.IntegerField(choices=mianmao_CHOICES,default=3)
	banjizhiwu = models.CharField(max_length=20,blank=True,null=True)
	xueshenghuizhiwu = models.CharField(max_length=20,blank=True,null=True)
	qingshi = models.CharField(max_length=20,default=u"男0#000")
	chuangpu = models.IntegerField(default=0)
	dianhua = models.BigIntegerField(blank=True,null=True)
	qq = models.BigIntegerField(blank=True,null=True)
	email = models.CharField(max_length=40,blank=True,null=True)
	koufen = models.IntegerField(default=0)
	tongbao = models.IntegerField(default=0)

	def __unicode__(self):
		return self.name


