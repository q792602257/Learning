from bs4 import BeautifulSoup as Soup

key = ["A","B","C","D","E"]

def errorHandle(Word):
	Word=Word.replace("正确答案是:","")
	return Word.split(",")
kww = open("1.txt","w",encoding="utf8")
for i in range(18):
	f = open("../%d.html"%(i),"r",encoding="utf8")
	soup = Soup(f,"html.parser")
	for k in soup.select("div.examPaper_subject"):
		ss = k.select_one("div.subject_key")
		tk = k.select_one("div.subject_stem")
		kww.write(tk.get_text().replace("\n", "").replace(" ", ""))
		if ss != None:
			a = k.select("div.nodeLab > label")
			t = ss.select_one("span.key_yes")
			if t != None:
				for aa in a:
					if "checked" in aa.select_one("input.mr5").attrs:
						kww.write(aa.select_one("span.mr5").get_text().replace("\n","").replace(" ",""))
				kww.write("\n")		
			else:
				for aa in errorHandle(ss.select_one("span.key_error").get_text()):
					kww.write(a[key.index(aa)].select_one("span.mr5").get_text().replace("\n", "").replace(" ", ""))
				kww.write("\n")
			for tmp in a:
				kww.write(tmp.get_text().replace("\n", "").replace(" ", ""))
				kww.write("\n")
		else:
			for a in k.select("div.answerKey_detail"):
				kww.write("\n")
				kww.write(a.get_text().replace("\n", "").replace(" ", ""))
			kww.write("\n")
		kww.write("\n")
	kww.write("\n\n\n\n")

"""
import tab
from time import sleep
from selenium import webdriver
b=webdriver.Firefox()
url="http://exam.zhihuishu.com/onlineExam/studentExam/stuExam"
b.get(url)


b.switch_to_window(b.window_handles[0])
a=b.find_elements_by_css_selector("a.course_ewname")
i=0
while True:
  a[i].location_once_scrolled_into_view
  a[i].click()
  sleep(5)
  b.switch_to_window(b.window_handles[1])
  with open("%d.html"%(i),"w",encoding="utf8") as f:
    sleep(3)
    f.write(b.page_source)
  b.close()
  sleep(1)
  i+=1
  b.switch_to_window(b.window_handles[0])
  sleep(1)
  a=b.find_elements_by_css_selector("a.course_ewname")
  if i >= len(a):
    break
"""
