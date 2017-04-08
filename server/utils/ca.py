"""Общие классы для обслуживания элементов чистой архитектуры."""


class SuccessResponse:
    """Класс результата работы сценария при отсутствии ошибок."""

    __slots__ = ("data",)

    def __init__(self, data=None):
        self.data = data

    def __bool__(self):
        return True


class ErrorResponse:
    """Класс результата работы сценария при возникновении ошибки."""

    def __init__(self, errors):
        self.errors = errors

    def __bool__(self):
        return False

    @property
    def value(self) -> dict:
        return {"message": self.errors}

    @classmethod
    def build_from_invalid_request(cls, invalid_request: RequestToUseCase):
        message = ""
        if invalid_request.has_errors():
            list_errors = ["{0}: {1}".format(error['parameter'], error['message']) for error in invalid_request.errors]
            message = "\n".join(list_errors)
        return cls(message)

    @classmethod
    def build_system_error(cls, error_message: str):
        return cls(error_message)


class RequestToUseCase:
    """Класс идентифицирующий запрос.
    
    Требует перекрытия init с передачей аргументов необходимых конкретному сценарию.
    В нем осуществить загрузку данных и их валидацию.
    
    """

    errors = None

    def __init__(self):
        super().__init__()
        self.errors = []

    def __bool__(self):
        return not self.has_errors()

    def add_error(self, parameter: str, message: str):
        """Добавляет ошибку запроса."""
        if not isinstance(self.errors, list):
            self.errors = []
        self.errors.append({"parameter": parameter, "message": message})

    def has_errors(self) -> bool:
        """Вернет True если в запросе найдены ошибки."""
        return isinstance(self.errors, list) and (len(self.errors) > 0)


class UseCase:
    """Класс для последующих реализаций слоя сценариев.

    В нем реализуется бизнес-логика модуля. Один класс - один сценарий, один запрос - один результат сценария.

    """

    async def process_request(self, request_object: RequestToUseCase):
        """Обработка запроса для конкретного сценария, требует перекрытия."""
        raise NotImplementedError(
            "process_request() not implemented by UseCase class {}".format(self.__class__.__name__)
        )

    async def execute(self, request_object: RequestToUseCase):
        """Общий метод вызывающий работу сценария и перехватывающий его исключения."""
        if not request_object:
            return ErrorResponse.build_from_invalid_request(request_object)

        try:
            return await self.process_request(request_object)
        except Exception as e:
            return ErrorResponse.build_system_error("{0}: {1}".format(e.__class__.__name__, str(e)))
