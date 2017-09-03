"""Набор общих исключений, которые выбрасываются по ходу работы.

В рамках торнадо имеется базовое исключение, которое можно выбрасывать при генерации ответа Finish,
при этом оно не будет интерпретироваться как ошибка. Result - его наследник, перекрытый для своих нужд.

Поскольку каждая ошибка - исключение, но не каждое исключение - ошибка -
предпринята попытка, в рамках химеры, стандартизировать ответ возвращаемый клиенту,
независимо от происходящего внутри системы.

Это значит что и фатальная ошибка и ожидаемый результат и допустимый результат
(при передаче пороговых или запредельных значений в обработчики)
должны возвращать один и тот же, по своей структуре, результат.

"""
import graphql.execution.base
from tornado.web import Finish


class Result(Finish):
    _error_code = 0
    _error_message = None

    def __init__(self, content: dict = None, error_message: str = None, error_code: int = None):
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


class NotFound(Result):
    """Запрошенного контента в системе не найдено."""
    _error_code = 21
    _error_message = "Запрошенного контента в системе не найдено"


class Response(Finish):
    """Базовое исключение для вывода результата работы обработчиков.

    Возбуждение этого исключения и его наследников должно свидетельствовать о корректном завершении работы над запросом
    (даже если нельзя считать его удачным).

    """

    def __init__(self, result: graphql.execution.base.ExecutionResult):
        """Перекрытие инициализации для передачи аргументов в объект Finish.

        Ответ должен содержать в себе всю необходимую информацию для адекватной реакции клиента:
        - список ошибок возникших в результате обработки запроса;
        - запрошенный контент;

        Инициализация отличается от родительской тем что в данном исключении приводится структура ответа к единому виду
        в соответствии со стандартом GraphQL.

        """
        if result.errors or result.invalid:
            super().__init__({"errors": [str(error) for error in result.errors]})
        else:
            super().__init__({"data": result.data})
