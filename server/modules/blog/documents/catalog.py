"""Набор документов для формирования категории."""
from system.document import BaseDocument
from motorengine import StringField


class CatalogDocument(BaseDocument):
    """Каталог - папка для хранения информации. Каталоги имеют иерархичную структуру.

    :type DEFAULT_PARENT_ALIAS: str Базовый указатель на корневую директорию
    :type title: str Человеческий заголовок каталога
    :type alias: str Псевдоним для вставки в url и однозначно идентифицирующий каталог
    :type parentAlias: str Указатель на родительский каталог
    """

    __collection__ = "catalog"

    DEFAULT_PARENT_ALIAS = ""

    title = StringField(required=True)
    alias = StringField(required=True, unique=True)
    parentAlias = StringField(default=DEFAULT_PARENT_ALIAS)
