from motorengine import Document, StringField, BaseField
from system.components.recommendations.cpn import ClusterExtractor, OutStarExtractor


class ClusterDocument(Document):
    __collection__ = "netKohonenCluster"

    name = StringField()
    vector = BaseField()


class KohonenClusterExtractor(ClusterDocument, ClusterExtractor):
    __collection__ = ClusterDocument.__collection__

    def get_cluster_id(self):
        return self.name

    def set_cluster_id(self, cluster_id):
        self.name = cluster_id

    def get_cluster_vector(self):
        return self.vector

    def set_cluster_vector(self, cluster_vector):
        self.vector = cluster_vector


class OutStarDocument(Document):
    __collection__ = "netOutStar"

    learning = BaseField()
    vector = BaseField()


class GrossbergOutStarExtractor(OutStarDocument, OutStarExtractor):
    __collection__ = OutStarDocument.__collection__

    def get_out_star_vector(self):
        return self.vector

    def get_beta_learning(self):
        return self.learning