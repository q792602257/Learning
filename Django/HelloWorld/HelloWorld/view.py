#!/usr/bin/env python2
# -*- coding:utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from HWapp.models import HWapp
import random

def hello(request):
	context = {}
	#context['hello'] = 'Hello World!'
	context["test"] = "1"
	context["list1"] = range(10)
	return render(request, 'hello.html', context)
	#return HttpResponse("Hello world ! ")

def index(request):
	pass

def showdb(request):
	i = HWapp.objects.all().values_list('id','name','xingbie')[11:16]
	#get()Single One
	#order_by('name')[0:2]
	#filter(id=1) WHERE
	#delete()
	#for i in list:
	context = {}
	context["trlist"] = ["学号","姓名","性别"]
	context["datalist"] = i
	return render(request, 'infos.html', context)

def testdb(request):
    tid = random.randrange(0,100)
    return HttpResponse("<p>数据添加成功！</p></br><p>%s</p>"%(tid))


