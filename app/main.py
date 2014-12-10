# -*- coding: utf-8 -*-
# -=! Главная стартовая площадка !=-

__author__ = 'rey'

# Основные модули
import tornado.web        # веб фреймворк, на котором построен FriendFeed. web содержит большинство важных функций Tornado
# import tornado.escape     # методы кодирования/декодирования XHTML, JSON и URL
# import tornado.database   # Простая обертка вокруг MySQLdb для упрощения спользования СУБД MySQL
# import tornado.template   # язык шаблонов, в основу которого положен синтаксис языка Python
# import tornado.httpclient # неблокирующий HTTP клиент для работы с модулями web и httpserver
# import tornado.auth       # реализация схем аутентификации и авторизации от третих разработчиков (Google OpenID/OAuth, Facebook Platform, Yahoo BBAuth, FriendFeed OpenID/OAuth, Twitter OAuth)
# import tornado.locale     # поддержка локализации/интернационализации
# import tornado.options    # синтаксический анализатор файлов настроек и аргументов коммандной строки, оптимизированный для использования в среде сервера
# Низкоуровневые модули
import tornado.httpserver # очень простой HTTP сервер, на основе которого построен модуль web
# import tornado.iostream   # простая обертка вокруг неблокирующих сокетов для обеспечения общих шаблонов считывания и записи
import tornado.ioloop     # основная петля ввода/вывода
# import tornado.websocket  #
# import logging            #

from tornado.options import define, options

from handlers.main import MainerHandler
from handlers.navigator import NavigatorHandler
from handlers.collection import CollectionHandler
from handlers.post import PostHandler
import system.base.handler

define("port", default=8888, help="run on the given port", type=int)

settings = {
    "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    # "login_url": "/login",

    "twitter_consumer_key": "54HALYb2DrpC3VmdDN5jM9HZB",
    "twitter_consumer_secret": "RtkuUQPhKkk3uk1HclggzCPJk1L3jLfc6P7L6Hz6mZ5Lsadhqt",

    "google_oauth": {
        "key": "484611128919-82v2ugod9iam9v1ipvmo61bfsvhj3c6q.apps.googleusercontent.com",
        "secret": "_ITW0YImv3pfxjJN1UVYoPdU"
    }
}


# см пример по блогу - для оформления стартующего аппа
def main():
    tornado.options.parse_command_line()

    application = tornado.web.Application([
        (r"/index", MainerHandler),
        (r"/auth", system.base.handler.AuthHandler),
        (r"/navigator", NavigatorHandler),
        (r"/post/([\w-]+)", PostHandler),
        # (r"/collection", CollectionHandler),
        (r"/collection/([\w-]+)/([\d+]+)", CollectionHandler),
        # Neuron
        # (r"/cinema/process/([\w-]+)", CollectionHandler),
        # (r"/cinema/harvest/([\w-]+)", CollectionHandler),
        # (r"/cinema/result/([\w-]+)", CollectionHandler),
    ], **settings)

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
