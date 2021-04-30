# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import urlopen

html = urlopen("http://www.naver.com/")
bsObj = BeautifulSoup(html.read(), "html.parser")
print(bsObj)

quit()

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
