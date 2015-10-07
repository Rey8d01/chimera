# Базовая модель через которую будет происходить обращение к базе данных
from symbol import yield_arg


from motorengine import Document, DateTimeField

from motorengine.queryset import QuerySet


class BaseDocument(Document):

    def __init__(self, **kw):
        """

        :return:
        """
        Document.__init__(self, **kw)

    def to_son(self):
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


