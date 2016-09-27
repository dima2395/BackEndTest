from bs4 import BeautifulSoup
import urllib.request


source = "https://point.md/ru/rss/novosti/"
req = urllib.request.urlopen(source)
xml = BeautifulSoup(req, 'lxml')


#takes bodys of articles
for item in xml.findAll('item'):
    url = item.guid.text
    news = urllib.request.urlopen(url).read()
    html = BeautifulSoup(news,'lxml')
    article = html.find('article', class_="post-text js-comments-article")
    text = article.find_all('p')
    print('URL:',url)
    print('Article body:', text)
    print('='*15)