import os, uuid, datetime, bleach
from urllib.parse import urlparse
import motor.motor_tornado
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler
from slugify import slugify




class MainHandler(RequestHandler):
  async def get(self):
    db = self.settings['db']
    collection = db.news
    items = []
    async for document in collection.find():
      document['datetime'] = document['datetime'].strftime("%Y-%m-%d %H:%M")
      items.append(document)
    self.render("index.html", items=items)

class AddNewsHandler(RequestHandler):
  def get(self):
    self.render("add_news.html")
  def post(self):
    db = self.settings['db']
    news = db.news

    title = self.get_argument("title")
    body = self.get_argument("body")
    url = slugify(title)

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
      img_url = upload_path + cname
      print('img_url', img_url)
    else:
      self.finish('Фото должно быть расширения .jpg или .jpeg')
    self.redirect("/")

    #insert document into database
    document = {
      "title": title,
      "body": cleaned_body,
      "url": url,
      "datetime": datetime.datetime.now(),
      "img_url": img_url
    }
    news.insert(document)

def main():
  db = motor.motor_tornado.MotorClient('localhost', 27017).simpals
  app = Application(
    [
      (r"/", MainHandler),
      (r"/add", AddNewsHandler),
    ],
    db=db,
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
  )
  app.listen(8888)
  IOLoop.current().start()

if __name__ == "__main__":
  main()
