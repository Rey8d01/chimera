"""Набор классов для организации доступа к хранилищу информации нейронной сети."""
from system.document import BaseDocument
from motorengine import StringField, BaseField
from system.components.recommendations.cpn import ClusterExtractor, OutStarExtractor


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
        return self.vector

    def get_beta_learning(self):
        return self.learning