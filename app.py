import os, uuid, datetime, bleach, math
from urllib.parse import urlparse
import motor.motor_tornado
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler
from slugify import slugify




class HomePageHandler(RequestHandler):
  def get(self):
    self.redirect('/news/1')


class NewsListHandler(RequestHandler):
  async def get(self, page):
    db = self.settings['db']
    news = db.news

    #pagination
    amount_of_news = await news.find({}).count()
    news_per_page = 2
    current_page = int(page)
    news_to_skip = (current_page - 1) * news_per_page
    amount_of_pages = math.ceil(amount_of_news / news_per_page)

    if current_page+1 <= amount_of_pages:
      next_page = current_page+1
    else:
      next_page = None

    if current_page-1 >= 1:
      prev_page = current_page-1
    else:
      prev_page = None

    pagination = {
      "current_page": current_page,
      "next_page": next_page,
      "prev_page": prev_page,
      "first_page": 1,
      "last_page": amount_of_pages,
    }


    items = []
    async for document in news.find({}).sort("_id", -1).skip(news_to_skip).limit(news_per_page):
      document['datetime'] = document['datetime'].strftime("%Y-%m-%d %H:%M")
      items.append(document)

    self.render("index.html", items=items, pagination=pagination)


class AddNewsHandler(RequestHandler):

  def get(self):
    self.render("add_news.html")

  def post(self):
    db = self.settings['db']
    news = db.news
    title = self.get_argument("title")
    body = self.get_argument("body")
    now = datetime.datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')
    day = now.strftime('%d')
    url = "%s/%s/%s/%s" % (year, month, day, slugify(title))

    #body validation
    def filter_src(name, value):
      if name == 'src':
        url = urlparse(value)
        if url.netloc in ['youtube.com', 'play.md', 'vimeo.com']:
          return True

    tags = ['p','a','b','i','strong','em', 'img','iframe']
    attrs = {
      '*': ['class'],
      'a': ['href'],
      'img': ['src'],
      'iframe': filter_src
    }
    cleaned_body = bleach.clean(body)

    #image validation
    fileinfo = self.request.files['image'][0]
    fname = fileinfo['filename']
    extn = os.path.splitext(fname)[1]
    if extn == ".jpg" or ".jpeg":
      cname = str(uuid.uuid4()) + extn
      upload_path = self.settings['static_path'] + '/uploaded_images/'
      fh = open(upload_path + cname, 'wb')
      fh.write(fileinfo['body'])
      img_url = '/' + upload_path + cname
      print('img_url', img_url)
    else:
      self.finish('Фото должно быть расширения .jpg или .jpeg')

    #insert document into database
    document = {
      "title": title,
      "body": cleaned_body,
      "url": url,
      "datetime": now,
      "img_url": img_url
    }
    news.insert(document)

    self.redirect(document['url'])


class SingleNewsPageHandler(RequestHandler):
  async def get(self, *args):
    db = self.settings['db']
    news = db.news
    url = ('%s/%s/%s/%s') % tuple(args)
    item = await news.find_one({"url": url}) 
    item['datetime'] = item['datetime'].strftime("%Y-%m-%d %H:%M")
    self.render("single_news.html", item=item)



def main():
  db = motor.motor_tornado.MotorClient('localhost', 27017).simpals
  app = Application(
    [
      (r"^/$", HomePageHandler),
      (r"^/news/(?P<page>[0-9]+)$", NewsListHandler),
      # /news/year/month/day/slug
      (r"^/news/([0-9]{4})/([0-9]{2})/([0-9]{2})/([a-z0-9-]+)$", SingleNewsPageHandler),
      (r"^/news/add$", AddNewsHandler),
    ],
    db=db,
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=True
  )
  app.listen(8888)
  IOLoop.current().start()

if __name__ == "__main__":
  main()
