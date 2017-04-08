"""Набор классов для организации доступа к хранилищу информации нейронной сети."""
from motorengine import StringField, BaseField

from documents.user import UserDocument
from modules.recommendation.lib.cpn import ItemExtractor, ClusterExtractor, OutStarExtractor
from utils.document import BaseDocument


class ClusterDocument(BaseDocument):
    """Документ для хранения информации по кластерам."""
    __collection__ = "netKohonenCluster"

    name = StringField()
    vector = BaseField()


class KohonenClusterExtractor(ClusterDocument, ClusterExtractor):
    """Класс-прослойка для извлечения информации по кластерам.

    Наследуется от ClusterDocument для получения возможности пользоваться актуальным источником данных.

    """
    __collection__ = ClusterDocument.__collection__

    def get_cluster_id(self):
        return self.name

    def set_cluster_id(self, cluster_id):
        self.name = cluster_id

    def get_cluster_vector(self):
        return self.vector

    def set_cluster_vector(self, cluster_vector):
        self.vector = cluster_vector


class OutStarDocument(BaseDocument):
    """Документ для хранения информации по работе звезды Гроссберга."""
    __collection__ = "netOutStar"

    learning = BaseField()
    vector = BaseField()


class GrossbergOutStarExtractor(OutStarDocument, OutStarExtractor):
    """Класс-прослойка для извлечения информации по звезде Гроссберга.

    Наследуется от OutStarDocument для получения возможности пользоваться актуальным источником данных.

    """
    __collection__ = OutStarDocument.__collection__

    def get_out_star_vector(self):
        return super().vector

    def get_beta_learning(self):
        return super().learning


class UserItemExtractor(UserDocument, ItemExtractor):
    """Внутренний класс для определения ключевых позиций у пользователя необходимых для кластеризации."""
    __collection__ = UserDocument.__collection__

    def get_item_id(self):
        return str(super()._id)

    def get_item_name(self):
        return super().get_user_name()

    def get_item_vector(self):
        return super().critic.copy()

    def associate_cluster(self, cluster_name):
        super().cluster = str(cluster_name)
