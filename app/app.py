#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Основные модули
import tornado.web        # веб фреймворк, на котором построен FriendFeed. web содержит большинство важных функций Tornado          
import tornado.escape     # методы кодирования/декодирования XHTML, JSON и URL
# import tornado.database   # Простая обертка вокруг MySQLdb для упрощения спользования СУБД MySQL                  
# import tornado.template   # язык шаблонов, в основу которого положен синтаксис языка Python                  
# import tornado.httpclient # неблокирующий HTTP клиент для работы с модулями web и httpserver                  
import tornado.auth       # реализация схем аутентификации и авторизации от третих разработчиков (Google OpenID/OAuth, Facebook Platform, Yahoo BBAuth, FriendFeed OpenID/OAuth, Twitter OAuth)                  
# import tornado.locale     # поддержка локализации/интернационализации                  
import tornado.options    # синтаксический анализатор файлов настроек и аргументов коммандной строки, оптимизированный для использования в среде сервера              
# Низкоуровневые модули
import tornado.httpserver # очень простой HTTP сервер, на основе которого построен модуль web                  
# import tornado.iostream   # простая обертка вокруг неблокирующих сокетов для обеспечения общих шаблонов считывания и записи              
import tornado.ioloop     # основная петля ввода/вывода              
import tornado.websocket  #
import logging            #

import json
import uuid
import os.path

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

# config for tornado
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "template/static"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "xsrf_cookies": True,
}

# config for my app
config = {
    "db" : {
        "host" : "qaz",
        "user" : "qaz",
        "pass" : "qaz"
    }
}


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("testr_user")


class MainHandler(BaseHandler):
    def get(self):
        # index.html
        if not self.current_user:
            user = "noname"
        else:
            user = self.current_user


        items = ["Item 1", "Item 2", "Item 3"]
        self.render("template/index.html", title="My title", items=items, peremenaya=config, user=user)
        # self.write("Hello, world")

class TestrHandler(BaseHandler):
    def get(self, id):
        # self.write("Param = " + id)

        if not self.current_user:
            user = "noname"
        else:
            user = self.current_user

        self.write("Param = " + user)


class AuthLoginHandler(BaseHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Google auth failed")


        #  {'first_name': u'\u0415\u0432\u0433\u0435\u043d\u0438\u0439', 'claimed_id': u'https://www.google.com/accounts/o8/id?id=AItOawkxRej7aruukIo2aVl5XSzw-yPiZ9sju4k', 'name': u'\u0415\u0432\u0433\u0435\u043d\u0438\u0439 \u0420\u0430\u0434\u0447\u0435\u043d\u043a\u043e', 'locale': u'ru', 'last_name': u'\u0420\u0430\u0434\u0447\u0435\u043d\u043a\u043e', 'email': u'rey.8d01@gmail.com'}
        # first_name
        # name
        # locale
        # last_name
        # email
        self.set_secure_cookie("testr_user", user["first_name"])
        self.redirect(self.get_argument("next", "/"))



class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("testr_user")
        self.redirect(self.get_argument("next", "/"))



def main():
    tornado.options.parse_command_line()

    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/tr/([0-9]+)", TestrHandler),
        (r"/login", AuthLoginHandler),
        (r"/logout", AuthLogoutHandler),
    ], **settings)

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

