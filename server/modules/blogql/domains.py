"""Blog domains."""


class Post:
    """Документ записи в блоге (пост)."""

    __slots__ = ("alias", "title", "text")

    def __init__(self, **kwargs):
        self.alias = kwargs.get("alias")
        self.title = kwargs.get("title")
        self.text = kwargs.get("text")
