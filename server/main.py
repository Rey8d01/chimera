# -*- coding: utf-8 -*-
"""
-=! Главная стартовая площадка !=-
Основные модули
import tornado.web  # веб фреймворк, на котором построен FriendFeed. web содержит большинство важных функций Tornado
import tornado.escape     # методы кодирования/декодирования XHTML, JSON и URL
import tornado.database   # Простая обертка вокруг MySQLdb для упрощения спользования СУБД MySQL
import tornado.template   # язык шаблонов, в основу которого положен синтаксис языка Python
import tornado.httpclient # неблокирующий HTTP клиент для работы с модулями web и httpserver
import tornado.auth       # реализация схем аутентификации и авторизации от третих разработчиков (Google OpenID/OAuth,
 Facebook Platform, Yahoo BBAuth, FriendFeed OpenID/OAuth, Twitter OAuth)
import tornado.locale     # поддержка локализации/интернационализации
import tornado.options    # синтаксический анализатор файлов настроек и аргументов коммандной строки,
 оптимизированный для использования в среде сервера
Низкоуровневые модули
import tornado.httpserver  # очень простой HTTP сервер, на основе которого построен модуль web
import tornado.iostream   # простая обертка вокруг неблокирующих сокетов для обеспечения общих шаблонов
 считывания и записи
import tornado.ioloop  # основная петля ввода/вывода
import tornado.websocket  #
"""

from tornado.options import options
from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.platform.asyncio import AsyncIOMainLoop
AsyncIOMainLoop().install()  # motor init IOLoop
# import tornado.log

from asyncio import get_event_loop
from settings import settings, ssl_ctx
from routes import routes


if __name__ == "__main__":
    # Передача настроек, создание приложения и его запуск.
    options.parse_command_line()
    application = Application(routes, **settings)

    http_server = HTTPServer(application, ssl_options=ssl_ctx)
    http_server.listen(options.port)

    get_event_loop().run_forever()
