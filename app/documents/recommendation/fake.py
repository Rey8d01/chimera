"""Документы для работы с тестовым набором данных."""
from motorengine import Document, StringField, EmbeddedDocumentField, BaseField
from documents.recommendation.cpn import UserItemExtractor


class FakeUserInfoDocument(Document):
    name = StringField()
    country = StringField()
    email = StringField()
    city = StringField()


class FakeUserDocument(Document):
    __collection__ = "fakeUser"
    fake_id = StringField()
    info = EmbeddedDocumentField(FakeUserInfoDocument)
    critic = BaseField()
    cluster = StringField()

    def get_user_name(self) -> str:
        return self.info.name


class FakeUserItemExtractor(FakeUserDocument, UserItemExtractor): pass
