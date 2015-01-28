__author__ = 'rey'

from motorengine import Document, StringField, IntField, EmbeddedDocumentField, BaseField


class UserInfoDocument(Document):
    name = StringField()
    country = StringField()
    email = StringField()
    city = StringField()


class UserDocument(Document):
    __collection__ = "fakeUser"

    fake_id = StringField()
    info = EmbeddedDocumentField(UserInfoDocument)
    critic = BaseField()
