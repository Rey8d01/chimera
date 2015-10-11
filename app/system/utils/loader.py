# todo
from system.utils.structure import Structure


class Loader(Structure):
    """
    Класс загрузчик данных из различных источников.
    Используется для загрузки данных в модели.

    """
    def __init__(self):
        Structure.__init__(self)

    def load_post(self, handler):
        """
        В соостветсвии со структурой загружает данные переданные через метод POST.

        :param handler:
        :return:
        """
        self.fill_by_method(handler.get_body_argument)
        return self

    def set_item_data(self, key, val):
        """
        Установить данные по ключу.

        :param key:
        :param val:
        :return:
        """
        self._data[key] = val