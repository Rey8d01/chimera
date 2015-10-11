# todo
import tornado.escape
import json


class ResultMessage():
    """
    Класс в котором собирается ответ для клиента в виде json
    """

    _message = None

    def __init__(self):
        """
        Описание формата ответа
        :return:
        """

        self._message = {
            "error": None,
            "content": {},
            "maintenance": {
                "redirect": None,
                "refresh": None,
                "delay": None,
                "cookie": None
            }
        }

    def __str__(self):
        """
        При обращении к результирующему ответу как к строке - ответ преобразуется в json
        :return:
        """
        return tornado.escape.json_encode(self._message)

    def update_content(self, data):
        """
        Обновление словаря с результирующими данными
        :param data:
        :return:
        """
        self._message["content"].update(data)

    def set_cookie(self, cookie):
        # self._message["maintenance"]["cookie"] = str(cookie)[len("Set-Cookie: chimera_user="):]
        self._message["maintenance"]["cookie"] = str(cookie)[len("Set-Cookie: "):]

    def get_message(self):
        return self._message