"""Группа основных обработчиков запросов по выводу результатов работы, авторизации в системе, обработки исключений и т.д."""
from json.decoder import JSONDecodeError

import graphql.execution.base
import tornado.escape
import tornado.web
from graphql.execution.base import ExecutionResult
from graphql.execution.executors.asyncio import AsyncioExecutor

from modules.schema import main_schema
from utils.exceptions import Response
from utils.token import JWTError, JWT_NAME_HEADER, Token


class AuthorizationMiddleware:
    """Класс проверки авторизации на этапе отработки запросов к GraphQL."""

    def resolve(self, next, root, args, context, info):
        if context["current_user"] is None:
            return None
        return next(root, args, context, info)


class BaseHandler(tornado.web.RequestHandler):
    """BaseHandler - основной перекрытый обработчик от которого наследовать все остальные."""

    def initialize(self):
        """Инициализация базового обработчика запросов."""

    def on_finish(self):
        """Завершение обработки запроса.

        Не может редактировать содержимое выводимого результата (не может ничего отправлять пользователю в принципе).

        """

    def write_error(self, status_code, **kwargs):
        """Перехват ошибок возникающих через исключения."""
        exc_info = kwargs['exc_info']
        # type_exception = exc_info[0]
        exception = exc_info[1]
        # traceback = exc_info[0]

        # Исключение которое было возбуждено феймворком - попытка отработать его корректно для клиента и привести к строковому виду.
        result = {
            "errors": [str(exception)]
        }

        self.finish(result)

    def set_default_headers(self):
        """Перекрытый метод установки ряда стандартных заголовков необходимых для CORS."""
        self.set_header('Content-Type', 'application/json; charset="utf-8"')
        self.set_header('Access-Control-Allow-Origin', self.settings["host"])  # * | http://chimera.rey
        self.set_header('Access-Control-Allow-Headers', 'X-Requested-With')
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header('Access-Control-Max-Age', '600')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET')

    # def get_bytes_body_argument(self, name: str, default=None) -> str:
    #     """Вернет значение переданного параметра от клиента.
    #
    #     Тестовый хак для обработки данных приходящих с приложения angular
    #
    #     :param name: Название свойства (поля) с которого будут считываться данные;
    #     :param default: Значение по умолчанию в случае отсутствия данных;
    #     :return: Обычно данные будут приходить в строковом формате;
    #     """
    #     return self.get_bytes_body_source().get(name, default)

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

    def data_received(self, chunk):
        """Перекрытие для скрытия предупреждений."""


class PublicHandler(BaseHandler):
    """Публичный API - без требований авторизации.

    На этом этапе обработчик - есть общая точка входа для всех запросов. Нет механизма идентификации.

    """

    async def get(self):
        """GraphQL GET - запрос данных.

        http://graphql.org/learn/serving-over-http/#get-request
        http://graphql.org/learn/queries/#arguments

        """
        client_redis = self.settings.get("client_redis", None)
        client_motor = self.settings.get("client_motor", None)
        query = self.get_argument(name="query")

        result = main_schema.execute(
            request_string=query,
            executor=AsyncioExecutor(),
            return_promise=True,
            context_value={
                "current_user": self.current_user,
                "client_redis": client_redis,
                "client_motor": client_motor,
            },
        )

        if not isinstance(result, graphql.execution.base.ExecutionResult):
            result = await result

        raise Response(result)

    async def post(self):
        """GraphQL POST - модификация данных.

        http://graphql.org/learn/serving-over-http/#post-request
        http://graphql.org/learn/queries/#variables

        """
        client_redis = self.settings.get("client_redis", None)
        client_motor = self.settings.get("client_motor", None)
        request = self.get_bytes_body_source()
        query = request.get("query", "")
        operation_name = request.get("operationName", "")
        variables = request.get("variables", {})

        result = main_schema.execute(
            request_string=query,
            operation_name=operation_name,
            variable_values=variables,
            executor=AsyncioExecutor(),
            return_promise=True,
            context_value={
                "current_user": self.current_user,
                "client_redis": client_redis,
                "client_motor": client_motor,
            },
            # middleware=[AuthorizationMiddleware()]
        )

        if not isinstance(result, graphql.execution.base.ExecutionResult):
            result = await result

        raise Response(result)


class PrivateHandler(PublicHandler):
    """Приватный API - требуется авторизация.

    Точка входа для запросов, для которых необходимо идентифицировать пользователя.

    """

    async def prepare(self):
        """Метод вернет объект пользователя исходя из информации токена, что был передан в заголовке с имененем 'token', в объекте request.

        Срабатывает перед методами get/post/...

        """
        from modules.user.repositories import UserRepository
        repository_user = UserRepository(client_motor=self.settings.get("client_motor", None))
        current_user = None
        try:
            token = Token.decode_from_str(repository_user, self.request.headers.get(JWT_NAME_HEADER, ""))
            is_valid = await token.is_valid()
            if is_valid:
                current_user = await token.get_user()
        except JWTError as _:
            pass

        if not current_user:
            raise Response(ExecutionResult(errors=("Пользователь не авторизован",)))

        self.current_user = current_user
