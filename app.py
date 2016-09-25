import os
import motor.motor_tornado
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler

class Main(RequestHandler):
  async def get(self):
    db = self.settings['db']
    collection = db.news
    result = await collection.find_one({"title": "Первая новость"})
    print(result)


def main():
  db = motor.motor_tornado.MotorClient('localhost', 27017).simpals
  app = Application(
    [
      (r"/", Main),
    ],
    db=db,
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
  )
  app.listen(8888)
  IOLoop.current().start()

if __name__ == "__main__":
  main()