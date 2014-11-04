# -*- coding: utf-8 -*-

__author__ = 'rey'

import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import define, options

from handlers.main import MainHandler
from handlers.navigator import NavigatorHandler
from handlers.collection import CollectionHandler
from handlers.post import PostHandler

define("port", default=8888, help="run on the given port", type=int)

# см пример по блогу - для оформления стартующего аппа
def main():
    tornado.options.parse_command_line()

    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/navigator/", NavigatorHandler),
        (r"/post/([\w-]+)", PostHandler),
        (r"/collection/", CollectionHandler),
        (r"/collection/([\w-]+)", CollectionHandler),
        # Neuron
        (r"/cinema/process/([\w-]+)", CollectionHandler),
        (r"/cinema/harvest/([\w-]+)", CollectionHandler),
        (r"/cinema/result/([\w-]+)", CollectionHandler),
    ])

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
