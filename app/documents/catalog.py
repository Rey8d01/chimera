from motorengine import Document, StringField


class CatalogDocument(Document):
    """
    Каталог - папка для хранения информации. Каталоги имеют иерархичную структуру.

    :type title: Человеческий заголовок каталога
    :type alias: Псевдоним для вставки в url и однозначно идентифицирующий каталог
    :type parentAlias: Указатель на родительский каталог
    """

    __collection__ = "catalog"

    title = StringField()
    alias = StringField()
    # parentAlias =