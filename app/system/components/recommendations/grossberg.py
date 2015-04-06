__author__ = 'rey'

# from motorengine import Document, StringField, BaseField
from system.components.recommendations.statistic import Similarity
from system.components.recommendations.kohonen import Kohonen, KohonenClusterExtractor, ItemExtractor, top250
# from abc import abstractmethod

# Counterpropagation network


class Grossberg():
    """
    Сеть Гроссберга

    """
    _beta_learning = None
    _minus_beta = None
    _components = None

    def __init__(self, components=None, count_items=None):
        """

        :param components:
        :type components: list[str]
        :return:
        """
        print("Инициализация сети Гроссберга")

        self._components = components if components is not None else top250

        self._beta_vector = {}
        self._ideal_vector = {component: 0.6 for component in self._components}

        self._minus_beta = self._beta_learning / count_items if count_items > 0 else 0.0001

    def learning(self, item, cluster):
        """
        i индекс нейрона кохонена (его id или имя)
        j индекс параметра выхода (его imdb)
        beta коэффициент скорости обучения
        beta_vector

        vector

        :param item: Объект содержащий вектор входа в слой Кохонена, он же является желаемым выходом
        :type item: ItemExtractor
        :param cluster: Объект (нейрон-победитель слоя Кохонена) содержащий вектор выхода
        :type cluster: KohonenClusterExtractor
        :return:
        """
        item_vector = item.get_item_vector()
        cluster_vector = cluster.get_cluster_vector()
        cluster_id = cluster.get_cluster_id()

        # В случае если в сети Гроссберга нейрон Кохонена не был определен, для него создаются веса по умолчанию
        if cluster_id not in self._beta_vector:
            self._beta_vector[cluster_id] = {component: 0.6 for component in self._components}
        cluster_beta_vector = self._beta_vector[cluster_id]

        # Корректировка весов
        for component in self._components:
            cluster_beta_vector[component] += self._beta_learning * (item_vector[component] - cluster_beta_vector[component]) * \
                                              cluster_vector[component]

            self._ideal_vector[component] += self._beta_learning * (item_vector[component] - self._ideal_vector[component]) * \
                                             cluster_vector[component]

        # Понижение коэффициента обучения
        self._beta_learning -= self._minus_beta


class Nielsen():
    """

    """

    net_kohonen = None
    net_grossberg = None

    def __init__(self, net_kohonen=None, net_grossberg=None):
        """

        :type net_kohonen: Kohonen
        :type net_grossberg: Grossberg
        :return:
        """
        self.net_kohonen = net_kohonen
        self.net_grossberg = net_grossberg

    def run(self, source=None, start_alpha_learning=0.8, clustering=True):
        """

        :param source:
        :param start_alpha_learning:
        :param clustering:
        :return:
        """
        self.net_kohonen.learning(source=source,
                                  start_alpha_learning=start_alpha_learning,
                                  clustering=clustering,
                                  callback_after_learn_item=self._excitement_grossberg)

    def _excitement_grossberg(self, item, cluster):
        """
        Возбуждение нейронов Гроссберга, срабатывает после того как слой Кохонена сформирует ответ


        :return:
        """
        self.net_grossberg.learning(item, cluster)


if __name__ == "__main__":
    print("Демонстрация сети Гроссберга")
