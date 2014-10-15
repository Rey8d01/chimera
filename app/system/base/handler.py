# Основной обработчик запросов торнадо tornado.web.RequestHandler от которого наследуем все остальные обработчики
# через базовый BaseHandler в котором воплотим основные используемые функции

__author__ = 'rey'

import tornado.web
import tornado.escape

from system.utils.result_message import ResultMessage


class BaseHandler(tornado.web.RequestHandler):
    """
    BaseHandler - основной перекрытый обработчик от которого наследовать все остальные

    воплотить базовые функции для всех потомков
    """
    web = None
    escape = None
    result = None

    def initialize(self):
        self.web = tornado.web
        self.escape = tornado.escape
        self.result = ResultMessage()

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
            error_message = object_error.error_message

        result = self.escape.json_encode({'error': error_message})
        self.write(result)