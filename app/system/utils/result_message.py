import tornado.escape


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
            "content": None,
            "maintenance": {
                "redirect": None,
                "refresh": None,
                "delay": None
            }
        }

    def __str__(self):
        """
        При обращении к резульирующему ответу как к строке - ответ преобразуется в json
        :return:
        """
        return tornado.escape.json_encode(self._message)