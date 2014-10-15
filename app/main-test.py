# -*- coding: utf-8 -*-

__author__ = 'rey'


# Основные модули
import tornado.web  # веб фреймворк, на котором построен FriendFeed. web содержит большинство важных функций Tornado
import tornado.escape  # методы кодирования/декодирования XHTML, JSON и URL
# import tornado.database   # Простая обертка вокруг MySQLdb для упрощения спользования СУБД MySQL
# import tornado.template   # язык шаблонов, в основу которого положен синтаксис языка Python
# import tornado.httpclient # неблокирующий HTTP клиент для работы с модулями web и httpserver
# import tornado.auth       # реализация схем аутентификации и авторизации от третих разработчиков (Google OpenID/OAuth, Facebook Platform, Yahoo BBAuth, FriendFeed OpenID/OAuth, Twitter OAuth)
# import tornado.locale     # поддержка локализации/интернационализации
import tornado.options  # синтаксический анализатор файлов настроек и аргументов коммандной строки, оптимизированный для использования в среде сервера
# Низкоуровневые модули
import tornado.httpserver  # очень простой HTTP сервер, на основе которого построен модуль web
# import tornado.iostream   # простая обертка вокруг неблокирующих сокетов для обеспечения общих шаблонов считывания и записи
import tornado.ioloop  # основная петля ввода/вывода
import tornado.websocket  #
import tornado.gen  #
import logging  #

import json
import uuid
import os.path

from tornado.options import define, options

import bson
import motor

# db = motor.MotorClient().db


class BaseHandler(tornado.web.RequestHandler):
    """
    BaseHandler - основной перекрытый обработчик от которого наследовать все остальные

    воплотить базовые функции для всех потомков
    """

    def on_finish(self):
        """
        loging
        :return:
        """
        pass
        # print(2)
        # print(dir(self))


class NavigatorHandler(BaseHandler):
    def get(self):
        pass


class CollectionHandler(BaseHandler):
    def get(self, id_collection):
        pass


class PostsHandler(BaseHandler):
    def get(self, id_post):
        pass


class TestHandler(BaseHandler):

    def initialize(self):
        self.tester = []

        self.tester.append('initialize')

    def prepare(self):
        self.tester.append('prepare')

    def get(self):
        self.tester.append('get')

        self.write(json.dumps(self.tester))

    def post(self):
        self.tester.append('post')

        self.write(json.dumps(self.tester))

define("port", default=8888, help="run on the given port", type=int)


def main():

    tornado.options.parse_command_line()

    application = tornado.web.Application([
        (r"/", TestHandler),
        (r"/post/(\d+)", PostsHandler),
        (r"/collection/([\w-]+)", CollectionHandler),
    ])

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
