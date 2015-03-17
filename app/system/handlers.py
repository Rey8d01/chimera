# Основной обработчик запросов торнадо tornado.web.RequestHandler от которого наследуем все остальные обработчики
# через базовый BaseHandler в котором воплотим основные используемые функции
# GET — получение ресурса
# POST — создание ресурса
# PUT — обновление ресурса
# DELETE — удаление ресурса

__author__ = 'rey'

import tornado.web
from tornado import gen
import tornado.escape
import tornado.auth

from system.utils.result_message import ResultMessage

# from system.components.environment import Environment
# from system.configuration import Configuration
from system.utils.exceptions import ChimeraHTTPError
from documents.user import UserDocument, UserOAuthDocument, UserMetaDocument


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
        print(error_message)

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
        user_data = self.get_secure_cookie("chimera_user")
        if user_data:
            return self.escape.json_decode(user_data)
        else:
            return None

    @gen.coroutine
    def get_data_current_user(self):
        """
        Вернуть данные из базы по текущему пользователю
        """
        user_data = self.get_current_user()

        document_user = UserDocument()
        users = yield document_user.objects.filter({UserDocument.oauth.name: {"$elemMatch": {
            UserOAuthDocument.type.name: user_data["type"],
            UserOAuthDocument.id.name: user_data["id"]
        }}}).find_all()

        return users[0]


class MainHandler(BaseHandler):
    """
    Главный обработчик наследники которого требуют авторизацию со стороны пользователя для своих действий
    """

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

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        """
        test
        """
        print('get')
        print(self.cookies)

    @tornado.web.asynchronous
    @gen.coroutine
    def head(self):
        """
        test
        """
        # document_user = UserDocument()

        # users = yield document_user.objects.filter({"oauth": {"$elemMatch": {
        # "type": "twitter",
        #     "id": "2213719321"
        # }}}).find_all()
        #
        print(UserDocument.info)
        # self.write({"dd":66})

    def _load_user_from_post(self, auth_type, user_id):
        """
        Сборка документа пользователя для его сохранения

        Вынесли всякое добро в отдельный метод, может потом с изменением архитектуры удобнее это будет вообще
        держать подальше
        """
        document_user = UserDocument()
        document_user_oauth = UserOAuthDocument()
        document_user_meta = UserMetaDocument()
        document_user.oauth = [document_user_oauth]
        document_user.meta = document_user_meta

        user_info_raw = {key: value for key, value in self.request.arguments.items() if
                         key.startswith("user_info[raw]")}

        document_user_oauth.type = auth_type
        document_user_oauth.id = user_id

        document_user_oauth.name = self.get_argument("user_info[name]", "")
        document_user_oauth.alias = self.get_argument("user_info[alias]", "")
        document_user_oauth.avatar = self.get_argument("user_info[avatar]", "")
        document_user_oauth.email = self.get_argument("user_info[email]", "")
        document_user_oauth.raw = user_info_raw

        return document_user


    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        """
        Авторизация
        """
        # Основные данные это тип соцсети и ид в ней
        auth_type = self.get_argument("auth_type")
        user_id = self.get_argument("user_id")

        # Документ пользователя при поиске опирается на ид и тип соцсети
        document_user = UserDocument()
        users = yield document_user.objects.filter({UserDocument.oauth.name: {"$elemMatch": {
            UserOAuthDocument.type.name: auth_type,
            UserOAuthDocument.id.name: user_id
        }}}).find_all()

        if len(users) == 0:
            document_user = self._load_user_from_post(auth_type, user_id)
            yield document_user.save()

        chimera_user = self.escape.json_encode({"type": auth_type, "id": user_id})
        self.set_secure_cookie("chimera_user", chimera_user, domain=".chimera.rey")

        self.result.update_content({
            "auth": True
        })
        self.write(self.result.get_message())


class LogoutHandler(BaseHandler):
    """
    Класс для выхода из системы - очистка кук
    """

    def get(self):
        self.clear_cookie("chimera_user")


class AuthHandler(BaseHandler):
    """
    Класс прямой авторизации - использовать в предполагаемом сценарии серверной авторизации
    В данном варианте не используется
    """
    pass
