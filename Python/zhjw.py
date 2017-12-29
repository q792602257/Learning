import requests
from selenium import webdriver

def login(u,p):
	url = "http://zhjw1.jju.edu.cn/default2.aspx"
	b = webdriver.Firefox()
	b.get(url)
	username = b.find_element_by_css_selector("input#txtUserName")
	username.send_keys(u)
	password = b.find_element_by_css_selector("input#TextBox2")
	password.send_keys(p)
	yzm = b.find_element_by_css_selector("input#txtSecretCode")
	a = input("please Input The f**king Code")
	yzm.send_keys(str(a))
	ratio = b.find_element_by_css_selector("input#RadioButtonList1_2")
	ratio.click()
	login = b.find_element_by_css_selector("input#Button1")
	login.click()

