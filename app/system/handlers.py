# Основной обработчик запросов торнадо tornado.web.RequestHandler от которого наследуем все остальные обработчики
# через базовый BaseHandler в котором воплотим основные используемые функции

__author__ = 'rey'

import tornado.web
import tornado.escape
import tornado.auth

from system.utils.result_message import ResultMessage
# from system.components.environment import Environment
# from system.configuration import Configuration
from system.utils.exceptions import ChimeraHTTPError
from tornado import gen

from time import sleep

from models.user import UserModel


class BaseHandler(tornado.web.RequestHandler):
    """
    BaseHandler - основной перекрытый обработчик от которого наследовать все остальные

    воплотить базовые функции для всех потомков
    """
    web = None
    escape = None
    result = None
    # config = None

    def initialize(self):
        self.web = tornado.web
        self.escape = tornado.escape
        self.result = ResultMessage()
        # self.config = Configuration()

        # sleep(1)

    def on_finish(self):
        """
        loging
        Срабатывает автоматически для гетов
        Не может редактировать содержимое выводимого результата (не может ничего отправлять пользователю в принципе)
        :return:
        """
        pass

    def write_error(self, status_code=404, **kwargs):
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

    def get_current_user(self):
        """
        Перекрытый метод определения пользователя
        :return:
        """
        return self.get_secure_cookie("chimera_user")
        # user_json = self.get_secure_cookie("chimera_user")
        # if not user_json:
        #     return None
        # return tornado.escape.json_decode(user_json)


class MainHandler(BaseHandler):
    """
    Главный обработчик наследники которого требуют авторизацию со стороны пользователя для своих действий
    """

    @tornado.web.authenticated
    def prepare(self):
        """
        Перекрытие срабатывает перед вызовом всяческих гетов и постов
        :return:
        """

        if self.current_user is None:
            raise ChimeraHTTPError(401, error_message=u"Неизвестный пользователь")


class IntroduceHandler(BaseHandler):
    """
    Класс через который будет проводится представление пользователя системе, прошедшего клиентскую авторизацию
    """

    def post(self):
        print('Introduce post')
        # auth_type = self.get_argument("auth_type")
        # user_id = self.get_argument("user_id")
        # user_info = self.get_arguments("user_info", False)

        # print(auth_type)
        # print(user_id)
        # print(user_info)
        # print(self.get_query_arguments("user_info", False))
        # print(self.get_body_arguments("user_info", False))
        # print(self.decode_argument("user_info", False))

        # print(self.request)


        # print(self.request.arguments)
        # oauthio_provider_twitter
        # print(self.request.cookies)
        # self.set_cookie()

        t = "t"
        model_user = UserModel()

        model_user["oauth[1].firstName"] = "345678"
        print(model_user.get_data())

        pass


class AuthHandler(BaseHandler):
    """
    Класс прямой авторизации - использовать в предполагаемом сценарии серверной авторизации
    В данном варианте не используется
    """
    pass


class LogoutHandler(BaseHandler):
    """
    Класс для выхода из системы - очистка кук
    """
    def get(self):
        self.clear_cookie("chimera_user")