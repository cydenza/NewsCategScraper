# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
from bs4 import BeautifulSoup
#from selenium import webdriver
#from urllib.request import urlopen
#import ssl
import datetime

days_range = []

start = datetime.datetime.strptime("2021-04-29", "%Y-%m-%d")
end = datetime.datetime.strptime("2021-05-03", "%Y-%m-%d")

date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

for date in date_generated:
    days_range.append(date.strftime("%Y-%m-%d"))


url = "https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=100"              #정치
url = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=100&sid2=264"    #청와대
#url = "https://news.naver.com/main/read.nhn?mode=LS2D&mid=shm&sid1=100&sid2=264&oid=011&aid=0003907365"
#url = "https://news.naver.com/main/read.nhn?mode=LS2D&mid=shm&sid1=101&sid2=259&oid=014&aid=0004634895"

#context = ssl._create_unverified_context()
#html = urlopen(url, context=context)
#bsObj = BeautifulSoup(html.read(), "html.parser")

#req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
#bsObj = BeautifulSoup(req.text, "html.parser")

def getLinks(url):
    req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    bsObj = BeautifulSoup(req.text, "html.parser")
    return bsObj

bsObj = getLinks(url)

print("########  Find Next News Pages ")

# 뉴스 페이지들 얻는다. 추후 클릭해서 다음 페이지로 넘어가기 위함
listb = bsObj.find("div", {"class":"paging"})
print(listb)
a = listb.findAll("a")
for i in a:
    if 'href' in i.attrs:
        print(i)

print("########  Find News List ")
# 뉴스목록에서 해당 뉴스를 클릭해서 간다.
#nameList = bsObj.findAll("div", {"class":"list_body"})
div = bsObj.find("div", {"class":"list_body newsflash_body"})
NewsListUrl = []
aTag = div.findAll("a")
for i in aTag:
    if 'href' in i.attrs:
        NewsListUrl.append(i.attrs['href'])
        #print(i)

#print(NewsListUrl)

# 뉴스 내용 얻어온다.
for i in NewsListUrl:
    print(i)
    news = getLinks(i)
    print(news)
    quit()

# 다시 뉴스 목록으로 돌아간다.


#print(nameList.get_text())
print(a)
#for name in nameList:
#    print(name.get_text())
quit()

"""
driver = webdriver.Chrome('chromedriver')

url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query=주식"

driver.get(url)
req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')

print(soup)

articles = soup.select('#main_pack > div.news.mynews.section._prs_nws > ul > li')

for article in articles:
    a_tag = article.select_one('dl > dt > a')

    title = a_tag.text
    print(title)

driver.quit()
"""