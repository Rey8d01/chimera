"""
Набор классов реализующих базовые методы для работы с MongoDB. Через них будет происходить обращение к базе данных и тут будут
реализованы методы исправляющие некоторые косяки при работе с MotorEngine и другими библиотеками для доступа к БД.
"""

from motorengine import Document
from motorengine.queryset import QuerySet


class BaseDocument(Document):
    """
    Базовый документ. От него необходимо наследовать все документы с котороыми будет происходить работа.
    """

    def __init__(self, **kw):
        """

        :return:
        """
        Document.__init__(self, **kw)

    def to_son(self) -> dict:
        """
        Подготовка документа для перевода его в JSON.
        """
        data = dict()

        for name, field in list(self._fields.items()):
            value = self.get_field_value(name)
            result = field.to_son(value)
            if type(result) is not dict and type(result) is not list:
                result = str(result)
            data[field.db_field] = result

        return data

# Хаки по восполнению недостающего функционала


def sort(self, field_name, direction=1):
    """
    Функция сортировки order_by имеет левые проверки которые позволяют применять сортировку только по полям
    главной модели

    :param field_name:
    :param direction:
    :return:
    """
    self._order_fields.append((field_name, direction))
    return self

QuerySet.sort = sort


