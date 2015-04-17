__author__ = 'rey'

from motorengine import Document, StringField, EmbeddedDocumentField, BaseField
from system.components.recommendations.cpn import ItemExtractor, ClusterExtractor


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
    cluster = StringField()


class UserItemExtractor(UserDocument, ItemExtractor):
    """
    Внутренний класс для определения ключевых позиций необходимых для кластеризации
    """
    __collection__ = UserDocument.__collection__

    def get_item_id(self):
        return str(self._id)

    def get_item_name(self):
        return self.info.name

    def get_item_vector(self):
        return self.critic.copy()

    def associate_cluster(self, cluster_name):
        self.cluster = str(cluster_name)
