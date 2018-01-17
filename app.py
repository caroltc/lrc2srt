import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import settings
from handlers import *

def make_app():
    db = None
    handlers = [
    (r"/", MainHandler),
    (r"/covert", CovertHandler)
    ]
    config = {"template_path":settings.TEMPLATE_PATH, "static_path":settings.ASSETS_PATH, "cookie_secret":settings.COOKIE_SECRET, "debug":True}
    return tornado.web.Application(handlers, **config)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(settings.SERVER_PORT)
    tornado.ioloop.IOLoop.instance().start()
