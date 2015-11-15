"""Набор исключений применимых в системе и вызывающихся по ходу ее работы.

Поскольку каждая ошибка-исключение, но не каждое исключение-ошибка - в рамках химеры предпринята попытка стандартизировать ответ
возвращаемый клиенту, независимо от происходящего внутри системы.
Это значит что и фатальная ошибка и ожидаемый результат и допустимый результат (при передаче пороговых или запредельных значений в
обработчики) должны возвращать один и тот же, по своей структуре, результат.

"""
from system.utils.result import ResultMessage


class ChimeraException(Exception):
    """Базовый класс исключений для системы.

    :type message: str Текст при выводе исключения;
    """

    message = None

    def __init__(self, message: str):
        """Инициализация базового класса исключений.

        :param message: Текст для сообщения в исключении;
        :type message: str
        """

        self.message = message

    def __str__(self):
        """Базовый вывод текста исключения."""
        return str(self.message)


class Result(ChimeraException):
    """Базовое исключение для вывода результата работы обработчиков.

    Возбуждение этого исключения и его наследников должно свидетельствовать о корректном завершении работы над запросом
    (даже если нельзя считать его удачным).

    :type _error_code: int Унифицированный код ошибки для определения поведения в различных похожих ситуациях;
    """

    _error_code = 0
    _error_message = None

    def __init__(self, content: dict = None, error_message: str = None, error_code: int = None):
        """Перекрытие инициализации для предачи аргументов в объект ResultMessage.

        Инициализация отличается от родительской тем что в качестве результирующего сообщения будет задан объект ResultMessage
        с результатом работы системы, при этом перевод в строку должен отрабатываться корректно поскольку вывод будет идти в виде json.

        """
        error_code = error_code if error_code is not None else self._error_code
        error_message = error_message if error_message is not None else self._error_message
        self.message = ResultMessage(content=content, error_message=error_message, error_code=error_code)


class ErrorResult(Result):
    """Ошибка при работе обработчиков."""
    _error_code = 1
    _error_message = "Неизвестная ошибка"


class UserError(ErrorResult):
    """Группа ошибок связанные с пользователем/авторизацией."""
    _error_code = 10
    _error_message = "Ошибка при обработке данных пользователя"


class UserNotAuth(UserError):
    """Пользователь не авторизован."""
    _error_code = 11
    _error_message = "Пользователь не авторизован"


class UserNotFound(UserError):
    """Пользователь не найден."""
    _error_code = 12
    _error_message = "Пользователь не найден"


class ContentError(ErrorResult):
    """Группа ошибок связанная с доступом к контенту по запросу."""
    _error_code = 20
    _error_message = "Ошибка при запросе данных для страницы"


class NotFound(ContentError):
    """Запрошенного контента в системе не найдено."""
    _error_code = 21
    _error_message = "Запрошенного контента в системе не найдено"
