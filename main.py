# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#from selenium import webdriver
#from urllib.request import urlopen
#import ssl

import requests
from bs4 import BeautifulSoup
import datetime
import os

# 다운로드 받을 디렉토리
download_directory = "D:\\news_scrap\\"
download_directory = download_directory + datetime.datetime.today().strftime("%Y%m%d%H%M") + "\\"
print(download_directory)

# 아래는 네이버
#url = "https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=100"              #정치
#url = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=100&sid2=264"    #청와대
#url = "https://news.naver.com/main/read.nhn?mode=LS2D&mid=shm&sid1=100&sid2=264&oid=011&aid=0003907365"
#url = "https://news.naver.com/main/read.nhn?mode=LS2D&mid=shm&sid1=101&sid2=259&oid=014&aid=0004634895"

# 여기는 네이트
urlList = [["정치", "청와대", "https://news.nate.com/subsection?mid=n0202"],
           ["정치", "국회/정당", "https://news.nate.com/subsection?mid=n0203"],
           ["정치", "외교/국방", "https://news.nate.com/subsection?mid=n0204"],
           ["정치", "북한", "https://news.nate.com/subsection?mid=n0205"],
           ["정치", "행정", "https://news.nate.com/subsection?mid=n0206"],
           ["정치", "정치일반", "https://news.nate.com/subsection?mid=n0207"],
           ["경제", "생활경제", "https://news.nate.com/subsection?mid=n0302"]]


"""
### 네이트는 일주일치 뉴스만 제공하기 때문에 아래의 날짜 계산을 할 필요가 없다.
### 그냥 하단 네이게이션 버튼을 클릭하면 된다.

# 날짜 기간을 지정하여 뉴스 얻기 위한 준비
days_range = []

start = datetime.datetime.strptime("2021-04-29", "%Y-%m-%d")
end = datetime.datetime.strptime("2021-05-03", "%Y-%m-%d")

date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

for date in date_generated:
    days_range.append(date.strftime("%Y-%m-%d"))

print(days_range)
"""

#context = ssl._create_unverified_context()
#html = urlopen(url, context=context)
#bsObj = BeautifulSoup(html.read(), "html.parser")

def getLinks(url):
    if url[0] == "/" :
        url = "http:" + url
        print(url)
    req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    bsObj = BeautifulSoup(req.text, "html.parser")
    return bsObj

download_count = 0

for urlstr in urlList:
    print("### Navigate : ", urlstr)
    category_1 = urlstr[0]
    category_2 = urlstr[1]
    url = urlstr[2]

    bsObj = getLinks(url)

    print("########  Find Next Date News Pages ")

    # 일주일 치 뉴스 페이지들 얻는다. 추후 클릭해서 다음 페이지로 넘어가기 위함
    NextDaysPages = []
    NextDaysPageIndex = 0

    listb = bsObj.find("div", {"class":"weekpagingNotCal f_clear"})
    print(listb)
    a = listb.findAll("a")
    for i in a:
        if 'href' in i.attrs:
            NextDayPage = i.attrs['href']
            if NextDayPage.startswith("/"):
                NextDayPage = "http://news.nate.com" + NextDayPage
            print(NextDayPage)
            NextDaysPages.append(NextDayPage)

    print("### 날짜페이지 목록: ", NextDaysPages)

    for dayPage in NextDaysPages:
        print("### NextDaysPageIndex : ", NextDaysPageIndex)
        if NextDaysPageIndex != 0:
            url = dayPage
            bsObj = getLinks(url)
        NextDaysPageIndex = NextDaysPageIndex + 1

        print("########  Find Next News Pages ")

        # 뉴스 페이지들 얻는다. 추후 클릭해서 다음 페이지로 넘어가기 위함
        NextPages = []
        NextPageIndex = 0

        listb = bsObj.find("div", {"class":"paging"})
        #print(listb)
        a = listb.findAll("a")
        for i in a:
            if 'href' in i.attrs:
                NextPage = i.attrs['href']
                if NextPage.startswith("/"):
                    NextPage = "http://news.nate.com" + NextPage
                print(NextPage)
                NextPages.append(NextPage)

        for page in NextPages:
            print("### NextPageIndex : ", NextPageIndex)
            if NextPageIndex != 0:
                url = page
                bsObj = getLinks(url)
            NextPageIndex = NextPageIndex + 1

            print("########  Find News List ")
            # 뉴스목록에서 해당 뉴스를 클릭해서 간다.

            div = bsObj.find("div", {"id":"newsContents"})
            #print(div)
            aTag = div.findAll("a", {"class":"lt1"})
            print(aTag)

            NewsListUrl = []

            for i in aTag:
                if 'href' in i.attrs:
                    NewsListUrl.append(i.attrs['href'])
                    print(i)

            print("###########  뉴스 URL 목록")
            print(NewsListUrl)

            # 뉴스 내용 얻어온다.
            print("######## Get News Contents")
            for i in NewsListUrl:
                print(i)
                news = getLinks(i)
                #print(news)

                rNews = news.find("div", {"id": "realArtcContents"})

                ass = rNews.findAll("a")
                for i in range(len(ass)):
                    rNews.find("a").extract()

                print(rNews.get_text().strip())

                download_count = download_count + 1
                if not os.path.isdir(download_directory):
                    os.mkdir(download_directory)
                download_file = download_directory + str(download_count) + ".txt"
                print(download_file)
                with open(download_file, 'w', encoding='UTF-8') as f:
                    f.write(category_1)
                    f.write("\n")
                    f.write(category_2)
                    f.write("\n")
                    f.write(rNews.get_text().strip())

                break       # 뉴스목록 중 하나만 읽고 끝
                #quit()
            break           # 뉴스 페이지 중 첫페이지만 읽고 끝

        #break               # 뉴스 날짜 중 첫 날짜 페이지만 읽고 끝

        #print(nameList.get_text())
        #print(a)
        #for name in nameList:
        #    print(name.get_text())
quit()

"""
# 아래는 Selenium을 이용한 스크래핑

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