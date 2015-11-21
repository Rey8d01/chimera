"""Группа основных обработчиков запросов по выводу результатов работы, авторизации в системе, обработки исключений и т.д.

Основной обработчик запросов торнадо tornado.web.RequestHandler от которого наследуем все остальные обработчики
через базовый BaseHandler в котором воплощены основные используемые функции.

GET — получение;
POST — создание;
PUT — обновление;
DELETE — удаление;
"""
import tornado.web
import tornado.escape
import system.utils.exceptions
from json.decoder import JSONDecodeError
from documents.user import UserDocument, UserOAuthDocument, UserMetaDocument


class BaseHandler(tornado.web.RequestHandler):
    """BaseHandler - основной перекрытый обработчик от которого наследовать все остальные."""
    escape = None
    redis = None

    def initialize(self):
        """Инициализация базового обработчика запросов."""
        self.escape = tornado.escape
        self.redis = self.settings["redis"]

    def on_finish(self):
        """Завершение обработки запроса.

        Не может редактировать содержимое выводимого результата (не может ничего отправлять пользователю в принципе).

        """

    def write_error(self, status_code, **kwargs):
        """Перехват ошибок и других событий возникающих через исключения.

        :param status_code:
        :param kwargs:
        """
        exc_info = kwargs['exc_info']
        type_exception = exc_info[0]
        exception = exc_info[1]
        traceback = exc_info[0]

        # Попытка привести исключение к строковому виду.
        if isinstance(exception, system.utils.exceptions.Result):
            # Успешная отработка запроса
            self.set_status(200)
            result = str(exception)
        elif isinstance(exception, system.utils.exceptions.ChimeraException):
            # Относительно успешная отработка запроса - исключение которое не было правильно обработано.
            result = str(exception)
        else:
            # Системное исключение которое было возбуждено феймворком - попытка отработать его корректно для клиента.
            result_message = system.utils.exceptions.ResultMessage(error_message=str(exception), error_code=1)
            result = str(result_message)

        # Вывод результата обработки исключения.
        self.write(result)
        self.finish()

    def set_default_headers(self):
        """Перекрытый метод установки ряда стандартных заголовков."""
        self.set_header('Content-Type', 'application/json; charset="utf-8"')
        self.set_header('Access-Control-Allow-Origin', '*')

    async def get_current_user(self):
        """Перекрытый метод определения пользователя."""
        user_data = await self.get_user_session()
        if user_data:
            return self.escape.json_decode(user_data)
        else:
            raise system.utils.exceptions.UserNotAuth()

    async def set_user_session(self, chimera_user: str):
        """Запись данных пользователя в сессию.

        :param chimera_user: json строка с данными пользователя;
        """
        await self.redis.set("chimera_user", chimera_user)

    async def get_user_session(self) -> str:
        """Получение из сессии данных пользователя."""
        return await self.redis.get("chimera_user")

    async def clear_user_session(self):
        """Очищение данных пользователя из сессии."""
        await self.redis.delete("chimera_user")

    async def get_data_current_user(self) -> UserDocument:
        """Вернет данные из базы по текущему пользователю."""
        user_data = await self.get_current_user()

        document_user = UserDocument()
        users = await document_user.objects.filter({UserDocument.oauth.name: {"$elemMatch": {
            UserOAuthDocument.type.name: user_data[UserOAuthDocument.type.name],
            UserOAuthDocument.id.name: user_data[UserOAuthDocument.id.name]
        }}}).find_all()

        return users[-1]

    def get_bytes_body_argument(self, name, default=None) -> str:
        """Вернет значение переданного параметра от клиента.

        Тестовый хак для обработки данных приходящих с приложения angular

        :param name: Название свойства (поля) с которого будут считываться данные;
        :param default: Значение по умолчанию в случае отсутствия данных;
        :return: Обычно данные будут приходить в строковом формате;
        """
        return self.get_bytes_body_source().get(name, default)

    def get_bytes_body_source(self) -> dict:
        """Вернет словарь пришедших данных от клиента.

        Декодировка данных в теле запроса self.request.body и представление в виде словаря.

        :return: dict с клиентскими данными;
        """
        try:
            body_arguments = tornado.escape.to_unicode(self.request.body)
            return tornado.escape.json_decode(body_arguments)
        except (TypeError, JSONDecodeError):
            return {}


class MainHandler(BaseHandler):
    """Главный обработчик наследники которого требуют авторизацию со стороны пользователя для своих действий."""

    async def prepare(self):
        """Перекрытие срабатывает перед вызовом обработчиков и в случае отсутствия данных по пользователю возбуждает исключение."""
        await self.get_current_user()


class PrivateIntroduceHandler(BaseHandler):
    """Вход по парольной фразе для привелегированного пользователя."""

    async def post(self):
        """Авторизация по парольной фразе."""
        import bcrypt

        hash = '$2a$15$jsDxfdO6tL1gVLoUVZh4AuyBRg92e.sjYY/kA2xKSGM.0MBU7smSq'  # passphrase
        passphrase = self.get_bytes_body_argument("passphrase")

        result = {"auth": False}
        if bcrypt.hashpw(passphrase, hash) == hash:
            chimera_user = self.escape.json_encode({"type": "admin", "id": "-1"})
            result["auth"] = True
            self.set_secure_cookie("chimera_user", chimera_user, domain=".chimera.rey")
            self.set_secure_cookie("chimera_user", chimera_user, domain=".chimera.rey")

        raise system.utils.exceptions.Result(content=result)


class IntroduceHandler(BaseHandler):
    """Класс через который будет проводится представление пользователя системе, прошедшего авторизацию."""

    def _load_user_from_post(self, auth_type, user_id):
        """Сборка документа пользователя для его сохранения."""
        # todo Вынесли всякое добро в отдельный метод, может потом с изменением архитектуры удобнее это будет вообще держать подальше
        document_user = UserDocument()
        document_user_oauth = UserOAuthDocument()
        document_user_meta = UserMetaDocument()
        document_user.oauth = [document_user_oauth]
        document_user.meta = document_user_meta

        user_info_raw = {key: value for key, value in self.request.arguments.items() if
                         key.startswith("user_info[raw]")}

        document_user_oauth.type = auth_type
        document_user_oauth.id = user_id

        document_user_oauth.name = self.get_bytes_body_argument("user_info[name]", "")
        document_user_oauth.alias = self.get_bytes_body_argument("user_info[alias]", "")
        document_user_oauth.avatar = self.get_bytes_body_argument("user_info[avatar]", "")
        document_user_oauth.email = self.get_bytes_body_argument("user_info[email]", "")
        document_user_oauth.raw = user_info_raw
        document_user_oauth.main = True

        return document_user

    async def post(self):
        """Авторизация."""
        # Основные данные это тип соцсети и ид в ней
        auth_type = self.get_bytes_body_argument("auth_type")
        user_id = self.get_bytes_body_argument("user_id")

        # Документ пользователя при поиске опирается на ид и тип соцсети
        document_user = UserDocument()
        users = await document_user.objects.filter({UserDocument.oauth.name: {"$elemMatch": {
            UserOAuthDocument.type.name: auth_type,
            UserOAuthDocument.id.name: user_id
        }}}).find_all()

        if len(users) == 0:
            document_user = self._load_user_from_post(auth_type, user_id)
            await document_user.save()

        chimera_user = self.escape.json_encode({"type": auth_type, "id": user_id})
        self.set_secure_cookie("chimera_user", chimera_user, domain=".chimera.rey")
        await self.set_user_session(chimera_user)

        raise system.utils.exceptions.Result(content={"auth": True})


class LogoutHandler(MainHandler):
    """Класс для выхода из системы - очистка кук."""

    async def get(self):
        """Сброс авторизации."""
        self.clear_cookie("chimera_user")
        await self.clear_user_session()
