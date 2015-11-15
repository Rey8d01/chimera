"""Класс в котором собирается ответ для клиента в виде json и возвращается через специальный обработчик исключений.

Ответ должен содержать в себе всю необходимую информмацию для возбуждения адекватной реакции клиента:
- список ошибок возникших в результате обработки запроса;
- запрошенный контент;
- необходимые действия для обслуживания клиента;

"""

import tornado.escape


class ResultMessage:
    """Результат выполнения запроса в виде готовой структуры.

    :type _message: dict Формируемый ответ, структура которого определена в инициализаторе;
    :type _error_code: int Код ошибки для унификации;
    """

    _message = None

    def __init__(self, content: dict = None, error_message: str = None, error_code: int = None):
        """При инициализации происходит описание формата ответа и занесение его в свойство класса.

        :param content:
        :param error_message:
        :param error_code:
        """

        self._message = {
            "error": {
                "message": error_message,
                "code": error_code
            },
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
