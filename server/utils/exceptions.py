"""Набор исключений применимых в системе и вызывающихся по ходу ее работы.

В рамках торнадо имеется базовое исключение, которое можно выбрасывать при генерации ответа Finish,
при этом оно не будет интерпретироваться как ошибка. Result - его наследник, перекрытый для своих нужд.

Поскольку каждая ошибка-исключение, но не каждое исключение-ошибка -
предпринята попытка, в рамках химеры, стандартизировать ответ возвращаемый клиенту,
независимо от происходящего внутри системы.
Это значит что и фатальная ошибка и ожидаемый результат и допустимый результат
(при передаче пороговых или запредельных значений в обработчики)
должны возвращать один и тот же, по своей структуре, результат.

"""
from tornado.web import Finish


class Result(Finish):
    """Базовое исключение для вывода результата работы обработчиков.

    Возбуждение этого исключения и его наследников должно свидетельствовать о корректном завершении работы над запросом
    (даже если нельзя считать его удачным).

    :type _error_code: int Унифицированный код ошибки для определения поведения в различных похожих ситуациях;
    """

    _error_code = 0
    _error_message = None

    def __init__(self, content: dict = None, error_message: str = None, error_code: int = None):
        """Перекрытие инициализации для передачи аргументов в объект Finish.

        Ответ должен содержать в себе всю необходимую информацию для адекватной реакции клиента:
        - список ошибок возникших в результате обработки запроса;
        - запрошенный контент;

        Инициализация отличается от родительской тем что в данном исключении приводится структура ответа к единому виду
        при этом перевод в строку должен отрабатываться корректно поскольку вывод будет идти в виде json, перевод в который обеспечит
        сам tornado через обработку исключения Finish и выводом (не как ошибки) через стандартный механизм ответов.

        """
        error_code = error_code if error_code is not None else self._error_code
        error_message = error_message if error_message is not None else self._error_message

        message = {
            "error": {
                "message": error_message,
                "code": error_code
            },
            "content": content if content is not None else {},
        }
        super().__init__(message)


class ResponseTest(Finish):
    def __init__(self, content: dict = None):
        super().__init__({"data": content if content is not None else {}})


import graphql.execution.base


class Response(Finish):
    def __init__(self, result: graphql.execution.base.ExecutionResult):
        if result.invalid:
            super().__init__({"errors": [error.message for error in result.errors]})
        else:
            super().__init__({"data": result.data})


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
