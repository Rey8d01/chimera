"""Набор исключений применимых в системе и вызывающихся по ходу ее работы.

Поскольку каждая ошибка-исключение, но не каждое исключение-ошибка - в рамках химеры предпринята попытка стандартизировать ответ
возвращаемый клиенту, независимо от происходящего внутри системы.
Это значит что и фатальная ошибка и ожидаемый результат и допустимый результат (при передаче пороговых или запредельных значений в
обработчики) должны возвращать один и тот же, по своей структуре, результат.

"""
import tornado.escape


class ResultMessage:
    """Класс в котором собирается ответ для клиента в виде json и возвращается через специальный обработчик исключений.

    Ответ должен содержать в себе всю необходимую информмацию для возбуждения адекватной реакции клиента:
    - список ошибок возникших в результате обработки запроса;
    - запрошенный контент;
    - необходимые действия для обслуживания клиента;

    :type _message: dict Формируемый ответ в виде определенной структуры;
    """

    _message = None

    def __init__(self, error: str = None, content: dict = None):
        """При инициализации происходит описание формата ответа и занесение его в свойство класса.

        :param error:
        :type error: str
        :param content:
        :type content: dict
        """

        self._message = {
            "error": error,
            "content": content if content is not None else {},
            "maintenance": {
                "redirect": None,
                "refresh": None,
                "delay": None,
                "cookie": None
            }
        }

    def __str__(self):
        """При обращении к результирующему ответу как к строке - ответ преобразуется в json."""
        return tornado.escape.json_encode(self._message)

    def update_content(self, data):
        """Обновление словаря с результирующими данными.

        :param data: Передаваемые данные могут быть любого типа, с которым не возникнет проблем при сериализации в json;
        """
        self._message["content"].update(data)

    def set_cookie(self, cookie: str):
        # todo ref
        # self._message["maintenance"]["cookie"] = str(cookie)[len("Set-Cookie: chimera_user="):]
        self._message["maintenance"]["cookie"] = str(cookie)[len("Set-Cookie: "):]

    def get_message(self) -> dict:
        """Вернет весь подготовленный ответ целиком.

        :return:
        :rtype: dict
        """
        return self._message


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

    """

    def __init__(self, *args, **kwargs):
        """Перекрытие инициализации для предачи аргументов в объект ResultMessage.

        Инициализация отличается от родительской тем что в качестве результирующего сообщения будет задан объект ResultMessage
        с результатом работы системы, при этом перевод в строку должен отрабатываться корректно поскольку вывод будет идти в виде json.

        :param error:
        :type error: str
        :param content:
        :type content: dict
        """
        self.message = ResultMessage(*args, **kwargs)


class ErrorResult(Result):
    """Ошибка при работе обработчиков."""


class NotFound(ErrorResult):
    """Запрошенного контента в системе не найдено."""
