from bs4 import BeautifulSoup
import urllib.request


source = "https://point.md/ru/rss/novosti/"
req = urllib.request.urlopen(source)
xml = BeautifulSoup(req, 'lxml')

counter = 0
for item in xml.findAll('item'):
  # if counter > 1:
  #   break
  # else:
    url = item.guid.text
    print('url: ', url)
    news = urllib.request.urlopen(url).read()
    # print(news)
    html = BeautifulSoup(news,'lxml')
    article = html.find('article', class_="post-text js-comments-article")
    text = article.find_all('p')
    print(text)
    # counter += 1
    print('===================================')