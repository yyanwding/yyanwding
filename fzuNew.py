import requests
from bs4 import BeautifulSoup
sessions = requests.session()
i = 1  # 对应第1页信息
page = '_' + str(i)
if i == 1:
    newsMainUrl = 'https://news.fzu.edu.cn/fdyw.htm'
elif i != 1:
    newsMainUrl = 'https://news.fzu.edu.cn/fdyw.htm' + page + '.html'

newsMainHeader = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Host': 'news.fzu.edu.cn',
    'Referer': 'https://news.fzu.edu.cn/html/fdyw/2.html',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
}
# get 请求
rsp = sessions.get(newsMainUrl, headers=newsMainHeader)
# 获取网页
content = rsp.content.decode('utf-8')
# soup用来解析网页的
soup = BeautifulSoup(content, 'html.parser')
# 获取所有dvi 并且calss为con-right fr"的标签
dvs = soup.find_all('div', class_="list_main_content")
for dv in dvs:
    # 获取div中所有的a标签
    items = dv.find_all('a')
    for item in items:
        print(item.contents)