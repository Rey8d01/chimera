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

from handlers.main import MainHandler
from handlers.navigator import NavigatorHandler
from handlers.collection import CollectionHandler
from handlers.post import PostHandler

define("port", default=8888, help="run on the given port", type=int)

# см пример по блогу - для оформления стартующего аппа
def main():
    tornado.options.parse_command_line()

    application = tornado.web.Application([
        (r"/index", MainHandler),
        (r"/navigator", NavigatorHandler),
        (r"/post/([\w-]+)", PostHandler),
        (r"/collection", CollectionHandler),
        (r"/collection/([\w-]+)", CollectionHandler),
        # Neuron
        # (r"/cinema/process/([\w-]+)", CollectionHandler),
        # (r"/cinema/harvest/([\w-]+)", CollectionHandler),
        # (r"/cinema/result/([\w-]+)", CollectionHandler),
    ])

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
