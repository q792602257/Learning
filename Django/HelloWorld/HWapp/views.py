# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from models import HWapp
import sys,os,xlrd,re,datetime,dateutil.relativedelta
reload(sys)
sys.setdefaultencoding('utf8')
# Create your views here.

class AddForm(forms.Form):
	method = forms.CharField(max_length=8)

class UserForm(forms.Form):
	method = forms.CharField()
	file1 = forms.FileField()

def getdata(request):
	if request.method=="POST":
		if request.POST.get("method",False):
			if request.POST["method"] == "query":
				return HttpResponse(request.POST["method"])
			elif request.POST["method"] == "add":
				return HttpResponse(request.POST["method"])
			elif request.POST["method"] == "modify":
				return HttpResponse(request.POST["method"])
			elif request.POST["method"] == "upload":
				myFile=request.FILES.get("file1",False)
				if not myFile:
					return render(request,"post.html",{'form':UserForm()})
				else:
					f = open(os.path.join("upload",myFile.name),'wb+')
					for chunk in myFile.chunks():
						f.write(chunk)
					f.close
					return HttpResponse(request.POST["method"])
			else:
				return HttpResponse("Something Wrong Happend,System is Already Logged This Issue")
		else:
			return HttpResponse("Something Wrong Happend,System is Already Logged This Issue")
	else:
		return render(request,"post.html",{'form':AddForm()})

