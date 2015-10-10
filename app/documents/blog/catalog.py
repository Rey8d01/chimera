"""
Набор документов для формирования категории.
"""
from motorengine import Document, StringField


class CatalogDocument(Document):
    """
    Каталог - папка для хранения информации. Каталоги имеют иерархичную структуру.

    :type title: str Человеческий заголовок каталога
    :type alias: str Псевдоним для вставки в url и однозначно идентифицирующий каталог
    :type parentAlias: str Указатель на родительский каталог
    """

    __collection__ = "catalog"

    title = StringField()
    alias = StringField()
    parentAlias = StringField()
