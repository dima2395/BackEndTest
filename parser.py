from bs4 import BeautifulSoup
import urllib.request


source = "https://point.md/ru/rss/novosti/"
req = urllib.request.urlopen(source)
xml = BeautifulSoup(req, 'lxml')


for item in xml.findAll('item'):
    url = item.guid.text
    print('url: ', url)
    news = urllib.request.urlopen(url).read()
    html = BeautifulSoup(news,'lxml')
    article = html.find('article', class_="post-text js-comments-article")
    text = article.find_all('p')
    print(text)
    print('===================================')