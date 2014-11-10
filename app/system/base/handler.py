# Основной обработчик запросов торнадо tornado.web.RequestHandler от которого наследуем все остальные обработчики
# через базовый BaseHandler в котором воплотим основные используемые функции

__author__ = 'rey'

import tornado.web
import tornado.escape

from system.utils.result_message import ResultMessage
# from system.components.environment import Environment
from system.configuration import Configuration


class BaseHandler(tornado.web.RequestHandler):
    """
    BaseHandler - основной перекрытый обработчик от которого наследовать все остальные

    воплотить базовые функции для всех потомков
    """
    web = None
    escape = None
    result = None
    config = None

    def initialize(self):
        self.web = tornado.web
        self.escape = tornado.escape
        self.result = ResultMessage()
        self.config = Configuration()

    def on_finish(self):
        """
        loging
        :return:
        """
        pass
        # print(2)
        # print(dir(self))

    def write_error(self, status_code, **kwargs):
        """
        Перехват ошибок возникающих через исключения

        :param status_code:
        :param kwargs:
        :return:
        """
        error_message = ''
        if 'exc_info' in kwargs:
            # kwargs['exc_info'][0]
            # kwargs['exc_info'][1]
            # kwargs['exc_info'][2]
            object_error = kwargs['exc_info'][1]

            if hasattr(object_error, 'error_message'):
                error_message = object_error.error_message
            else:
                error_message = object_error

        result = self.escape.json_encode({'error': error_message})
        self.write(result)

    def set_default_headers(self):
        """
        Перекрытый метод установки ряда стандартных заголовков

        :return:
        """
        self.set_header('Content-Type', 'application/json; charset="utf-8"')
        self.set_header('Access-Control-Allow-Origin', '*')