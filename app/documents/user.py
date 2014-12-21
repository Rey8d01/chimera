__author__ = 'rey'

from motorengine import Document, EmbeddedDocumentField, StringField, ListField, JsonField, DateTimeField, connection


class UserOAuthDocument(Document):
    type = StringField(required=True)  # twitter
    id = StringField(required=True)  # 1234

    name = StringField()  # John Doe
    alias = StringField()  # john87
    avatar = StringField()
    email = StringField()  # john@doe.com
    raw = JsonField()


class UserInfoDocument(Document):
    data = JsonField()


class UserMetaDocument(Document):
    date_registration = DateTimeField(auto_now_on_insert=True)
    date_last_activity = DateTimeField(auto_now_on_update=True)


class UserDocument(Document):
    __collection__ = "user"

    info = EmbeddedDocumentField(UserInfoDocument)
    meta = EmbeddedDocumentField(UserMetaDocument)
    oauth = ListField(EmbeddedDocumentField(UserOAuthDocument))

