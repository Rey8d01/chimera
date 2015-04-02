__author__ = 'rey'

from motorengine import Document, StringField, BaseField
from system.components.recommendations.statistic import Similarity
from abc import abstractmethod

# Вектор для задачи про фильмы
top250 = [
    'tt0111161', 'tt0068646', 'tt0071562', 'tt0468569', 'tt0110912', 'tt0060196', 'tt0050083', 'tt0108052', 'tt0167260',
    'tt0137523', 'tt0120737', 'tt0080684', 'tt0109830', 'tt1375666', 'tt0073486', 'tt0167261', 'tt0099685', 'tt0816692',
    'tt0133093', 'tt0076759', 'tt0047478', 'tt0317248', 'tt0114369', 'tt0114814', 'tt0102926', 'tt0038650', 'tt0064116',
    'tt0110413', 'tt0118799', 'tt0034583', 'tt0082971', 'tt0120586', 'tt0120815', 'tt0021749', 'tt0054215', 'tt0245429',
    'tt0047396', 'tt2582802', 'tt1675434', 'tt0027977', 'tt0103064', 'tt0209144', 'tt0120689', 'tt0253474', 'tt0407887',
    'tt0043014', 'tt0078788', 'tt0172495', 'tt0057012', 'tt0088763', 'tt0078748', 'tt0482571', 'tt0032553', 'tt0405094',
    'tt0110357', 'tt1853728', 'tt1345836', 'tt0095765', 'tt0081505', 'tt0050825', 'tt0169547', 'tt0910970', 'tt0053125',
    'tt0090605', 'tt0033467', 'tt0052357', 'tt0211915', 'tt0022100', 'tt0095327', 'tt0082096', 'tt0364569', 'tt0435761',
    'tt0119698', 'tt0086190', 'tt0087843', 'tt0066921', 'tt0105236', 'tt0075314', 'tt0036775', 'tt0112573', 'tt0180093',
    'tt0056592', 'tt0056172', 'tt0051201', 'tt0338013', 'tt0093058', 'tt0045152', 'tt0070735', 'tt0040522', 'tt0086879',
    'tt0071853', 'tt0208092', 'tt0119488', 'tt0042876', 'tt0059578', 'tt0062622', 'tt0012349', 'tt0053604', 'tt0042192',
    'tt0361748', 'tt0053291', 'tt0097576', 'tt0040897', 'tt0041959', 'tt1832382', 'tt0114709', 'tt0055630', 'tt0372784',
    'tt0986264', 'tt0017136', 'tt0105695', 'tt0086250', 'tt0081398', 'tt2562232', 'tt1049413', 'tt0071315', 'tt1187043',
    'tt0057115', 'tt0363163', 'tt0095016', 'tt0047296', 'tt0457430', 'tt0031679', 'tt1065073', 'tt2106476', 'tt0113277',
    'tt0050212', 'tt2267998', 'tt0119217', 'tt0116231', 'tt0096283', 'tt0050976', 'tt0044741', 'tt0015864', 'tt0080678',
    'tt0993846', 'tt0089881', 'tt0050986', 'tt0083658', 'tt0017925', 'tt0120735', 'tt1305806', 'tt0112641', 'tt1205489',
    'tt1291584', 'tt0118715', 'tt0434409', 'tt0032976', 'tt0347149', 'tt0405508', 'tt0077416', 'tt0025316', 'tt0061512',
    'tt0892769', 'tt0055031', 'tt0116282', 'tt0117951', 'tt0031381', 'tt1979320', 'tt0758758', 'tt0268978', 'tt0033870',
    'tt0046912', 'tt0167404', 'tt0046268', 'tt0395169', 'tt0084787', 'tt0266543', 'tt0978762', 'tt0477348', 'tt0064115',
    'tt0266697', 'tt0091763', 'tt0079470', 'tt1255953', 'tt0292490', 'tt2015381', 'tt2024544', 'tt0074958', 'tt0052311',
    'tt0046911', 'tt0075686', 'tt0093779', 'tt0469494', 'tt0092005', 'tt2278388', 'tt0401792', 'tt0052618', 'tt0053198',
    'tt0245712', 'tt0107207', 'tt0405159', 'tt0032551', 'tt1028532', 'tt0032138', 'tt0060827', 'tt2084970', 'tt0036868',
    'tt0848228', 'tt0087544', 'tt0083987', 'tt0440963', 'tt0246578', 'tt1954470', 'tt0056801', 'tt0044079', 'tt0338564',
    'tt0114746', 'tt1130884', 'tt0079944', 'tt0073195', 'tt0169102', 'tt0044706', 'tt1877832', 'tt0038787', 'tt0112471',
    'tt0088247', 'tt1504320', 'tt0107048', 'tt1201607', 'tt0083922', 'tt1220719', 'tt0075148', 'tt0058946', 'tt0048424',
    'tt0072890', 'tt0198781', 'tt0113247', 'tt0353969', 'tt0072684', 'tt0325980', 'tt0047528', 'tt0061184', 'tt0058461',
    'tt0092067', 'tt0120382', 'tt0038355', 'tt1454029', 'tt0107290', 'tt0046250', 'tt0061722', 'tt0054997', 'tt0070511',
    'tt0101414', 'tt0118694', 'tt1392214', 'tt0154420', 'tt0040746', 'tt0374546', 'tt0381681'
]


class KohonenClusterDocument(Document):
    __collection__ = "kohonenCluster"

    name = StringField()
    vector = BaseField()


class KohonenExceptionClustering(Exception):
    """
    Исключение для процесса кластеризации
    """
    pass


class ItemExtractor():
    """
    Интерфейсный класс который необходимо отнаследовать для класса с образцами данных.
    Методы этого интерфейса должны реализовать функционал для доступа к данным образца.
    """
    @abstractmethod
    def get_item_id(self):
        """
        Должен вернуть уникальный id образца, например id в БД.

        :return: str
        """
        pass

    @abstractmethod
    def get_item_name(self):
        """
        Должен вернуть человекопонятное имя образца, например имя человека.

        :return: str
        """
        pass

    @abstractmethod
    def get_item_vector(self):
        """
        Должен вернуть массив с данными для кластеризации, например массив оценок к фильмам.

        dict(id1: rate1, id2: rate2, ... idN: rateN)

        :return: dict
        """
        pass

    @abstractmethod
    def associate_cluster(self, cluster_name):
        """
        Методу передается имя кластера к которому будет принадлежать образец. Для удобства воспроизведение этой информации
        желательно ее записать в специальное поле.
        """
        pass


class Kohonen(Similarity):
    """
    Сеть Кохонена для кластеризации

    :type _similarity: callable Функция расчета коэффициента сходства
    :type _allowable_similarity: float Минимальный допустимый коэффициент сходства для присоединения образца к существующему кластеру
    :type _acceptable_similarity: float Минимальный приемлемый коэффициент сходства для присоединения образца к существующему кластеру
                                        без изменения его прототипа
    :type _alpha_learning: float Коэффициент обучения, понижающийся в процессе
    :type _clusters: dict[dict] Массив данных кластеров
    :type _item_cluster: dict[list] Временная информация о закрепленных к кластерам обрзцах
    :type _source: list[ItemExtractor] Массив данных образцов для обучения
    :type _max_deep: int Макисмальная глубина рекурсии по достижении которого обучение останавливается
    :type _current_deep: int Текущий уровень глубины рекурсии при обучении
    """

    _similarity = None
    _allowable_similarity = None
    _acceptable_similarity = None
    _alpha_learning = None
    _clusters = None
    _item_cluster = None
    _source = None
    _max_deep = None
    _current_deep = 0

    @property
    def clusters(self):
        """
        :return: dict[dict]
        """
        return self._clusters

    def __init__(self, list_cluster=None, list_source=None, similarity=None, allowable_similarity=None,
                 acceptable_similarity=None, _max_deep=None):
        """
        Инициализация кластеров. Инстанс сети Кохонена содержит в свойстве resource список кластеров фильмов и весов.

        :type list_cluster: list[KohonenClusterDocument] Список кластеров (список из классов KohonenClusterDocument)
        :type list_source: list[ItemExtractor]
        :type similarity: callable
        :type allowable_similarity: float
        :type acceptable_similarity: float
        :return:
        """
        print("Инициализация сети Кохонена")

        # Установка стандартных значений на этапе инициализации
        self._similarity = similarity if similarity is not None else self.euclid
        self._allowable_similarity = allowable_similarity if allowable_similarity is not None else 0.55
        self._acceptable_similarity = acceptable_similarity if acceptable_similarity is not None else 0.95
        self._max_deep = _max_deep if _max_deep is not None else 200

        if list_cluster is None or not isinstance(list_cluster, list) or len(list_cluster) <= 0:
            list_cluster = []
        clusters = {}
        for document_cluster in list_cluster:
            clusters[str(document_cluster.name)] = document_cluster.vector
        self._clusters = clusters
        print("Инициализировано кластеров " + str(len(self._clusters)))
        self._item_cluster = {}

        # Если сеть пустая то создадим тестовый кластер для начала работы
        if len(self._clusters) == 0:
            self.create_cluster()

        self._source = list_source
        print("Кластеризацию ожидают образцов " + str(len(self._source)))

    def create_cluster(self, vector=None):
        """
        Создание универсального кластера необходимо для динамического создания нейронов.
        Что бы создать универсальный кластер необходимо посчитать количество фильмов (М)
        создать случайный вектор весов (количество весовых коэфициентов = М).
        Для кластеров выделена отдельная коллекция, каждый кластер имеет свой документ.

        Так как количество фильмов может динамически изменятся,
        то необходимо контролировать идентефикаторы для весов и фильмов к которым они соотносятся

        Возвращается человеческий ид кластера для последующего к нему обращения

        :type vector: dict
        :return:
        """
        print("Начато создание нового кластера")

        # Расчет значения весового коэффициента принимаемого по умолчанию
        default_weight = 1 / pow(len(top250), 1 / 2)

        cluster_name = "cluster" + str(len(self._clusters) + 1)
        # Заполняем новый кластер стандартными значениями весов для каждого фильма или веса задаются под вектор
        if vector is None:
            cluster_vector = {id: default_weight for id in top250}
        else:
            keys_vector = list(vector.keys())
            cluster_vector = {id: vector[id] if id in keys_vector else default_weight for id in top250}

        # Добавляем новый класстер в сеть
        self._clusters[cluster_name] = cluster_vector

        print("Создание нового кластера завершено, кластеров в сети " + str(len(self._clusters)))
        return cluster_name

    def actualize_clusters(self):
        """
        Ищет и удаляет неиспользуемые кластеры и сохраняет изменения в кластерах в бд

        :return:
        """
        # Сбор уникальных имен используемых кластеров
        used_clusters_name = list(self._item_cluster.values())
        used_cluster = []
        [used_cluster.append(item) for item in used_clusters_name if item not in used_cluster]
        # Удаление кластеров, которые не приписаны ни одному образцу
        all_clusters_name = list(self._clusters.keys())
        [self._clusters.pop(cluster_name) for cluster_name in all_clusters_name if cluster_name not in used_cluster]
        print("Актуализация завершена, в сети кластеров " + str(len(self._clusters)))

    def save(self):
        """
        Сохранение кластера в бд

        :return:
        """
        # Оищение базы перед сохранением
        KohonenClusterDocument.objects.delete()
        # Сохранение кластеров в бд
        for (cluster_name, cluster_vector) in self._clusters.items():
            cluster_document = KohonenClusterDocument()
            cluster_document.name = cluster_name
            cluster_document.vector = cluster_vector
            cluster_document.save()

    def get_result_clustering(self):
        """
        Итог обучения
        Список фенотипов и их прототипов

        :return:
        """
        cluster_item = {}
        for (cluster_name, cluster_vector) in self._clusters.items():
            cluster_item[cluster_name] = [item_id for (item_id, item_cluster_name) in self._item_cluster.items() if
                                          item_cluster_name == cluster_name]
            print(cluster_name + " - " + str(cluster_item[cluster_name]))
        return cluster_item

    def learning(self, start_alpha_learning=0.8):
        """
        Процесс обучения сети по массе образцов

        :type start_alpha_learning: int Начальный коэффициент при обучении, по умолчанию стремится к 1
        :return:
        """
        self._alpha_learning = start_alpha_learning
        try:
            # Перебор всех элементов для их кластеризации
            for item in self._source:
                item_id = item.get_item_id()
                item_name = item.get_item_name()
                item_vector = self.normalize_vector(item.get_item_vector())
                self.clustering(item_id, item_name, item_vector)
        except KohonenExceptionClustering:
            self._current_deep += 1
            if self._current_deep < self._max_deep:
                # Создаем новый кластер - новый кластер наследует характеристики основателя (текущего образца)
                self.create_cluster(item_vector)
                # Перезапускаем процесс кластеризации для того, что бы новый кластер тоже учитывался при сравнении со всеми образцами
                print("Переобучение сети, глубина " + str(self._current_deep))
                return self.learning(self._alpha_learning)
            else:
                print("Достигнута максимальная глубина, дальнейшее обучение сети невозможно!")

        print("Завершение кластеризации")
        self.actualize_clusters()

    def working(self, item, start_alpha_learning=0.1):
        """
        Процесс работы сети по одному экземпляру

        :type start_alpha_learning: int Начальный коэффициент при работе много меньше чем при обучении
        :param item: ItemExtractor
        :return:
        """
        self._alpha_learning = start_alpha_learning
        try:
            item_id = item.get_item_id()
            item_name = item.get_item_name()
            item_vector = self.normalize_vector(item.get_item_vector())
            return self.clustering(item_id, item_name, item_vector)
        except KohonenExceptionClustering:
            return False

    def clustering(self, item_id, item_name, item_vector):
        """
        Процесс кластеризации по одному объекту.

        :type item_id: str
        :type item_name: str
        :type item_vector: dict
        :return:
        """

        # dict - матрица расстояний (точнее коэффициенты сходства) от текущего элемента до каждого кластера
        similarity = {cluster_name: self._similarity(item_vector, cluster_vector)
                      for (cluster_name, cluster_vector) in self._clusters.items()}

        # После сравнения всех кластеров с текущим элементом - получаем максимальный коэффициент сходства
        # (минимальное расстояние, максимальную корреляцию, максимальная близость)
        cluster_name_max_similarity = max(similarity, key=similarity.get)
        max_similarity = similarity[cluster_name_max_similarity]

        # Условие допустимого сходства
        if max_similarity < self._allowable_similarity:
            # Если коэффициент сходства, среди всех кластеров, меньше допустимого порога, это значит что образец находится слишком далеко
            # и на этапе обучения это порождает новый кластер, а на этапе работы сети следует оценить необходимость переобучения сети
            raise KohonenExceptionClustering
        else:
            # Если расчитанный максимальный коэффициент сходства удовлетворяет условию
            # минимального допустимого коэффициента сходства то интегрируем образец в кластер
            # Но если степень сходимости меньше минимальное приемлемой,
            # то прототип кластера необходимо скорректировать - иначе говоря обучить сеть,
            # скорректировать ее веса
            if max_similarity < self._acceptable_similarity:
                # Коррекция весов только по тем позициям, которые имеются в новом фенотипе
                # Обучение методом поиска среднего
                # for (id, weight) in item_vector.items():
                # self._clusters[cluster_name_max_similarity][id] = \
                # (weight * max_similarity + self._clusters[cluster_name_max_similarity][id]) / 2
                # Обучение методом уравнения Кохонена
                for (id, weight) in item_vector.items():
                    self._clusters[cluster_name_max_similarity][id] += self._alpha_learning * (weight - self._clusters[
                        cluster_name_max_similarity][id])

                self._alpha_learning -= 0.001 if self._alpha_learning > 0.1 else 0

        self._item_cluster[item_id] = cluster_name_max_similarity
        item.associate_cluster(cluster_name_max_similarity)
        return cluster_name_max_similarity


if __name__ == "__main__":
    print("Демонстрация сети Кохонена")

    cl1 = KohonenClusterDocument()
    cl2 = KohonenClusterDocument()
    cl3 = KohonenClusterDocument()
    cl1.name = 'cl1'
    cl2.name = 'cl2'
    cl3.name = 'cl3'
    cl1.vector = {top250[0]: 1.0, top250[1]: 0.9, top250[2]: 0.9, top250[3]: 0.5, top250[4]: 0.3}
    cl2.vector = {top250[0]: 0.4, top250[1]: 0.2, top250[2]: 0.2, top250[3]: 0.6, top250[4]: 0.3}
    cl3.vector = {top250[0]: 0.5, top250[1]: 0.1, top250[2]: 0.9, top250[3]: 0.1, top250[4]: 0.5}
    list_clusters = [cl1, cl2, cl3]

    class UserItemExtractor(ItemExtractor):
        id = None
        name = None
        vector = None

        def get_item_id(self):
            return self.id

        def get_item_name(self):
            return self.name

        def get_item_vector(self):
            return self.vector

    u1 = UserItemExtractor()
    u2 = UserItemExtractor()
    u3 = UserItemExtractor()
    u4 = UserItemExtractor()
    u5 = UserItemExtractor()
    u1.id = 1
    u2.id = 2
    u3.id = 3
    u4.id = 4
    u5.id = 5
    u1.name = "A"
    u2.name = "B"
    u3.name = "C"
    u4.name = "D"
    u5.name = "E"
    u1.vector = Similarity.normalize_vector(
        {top250[0]: 0.9, top250[1]: 0.9, top250[2]: 1.0, top250[3]: 0.6, top250[4]: 0.4})  # Близок к 1 кластеру
    u2.vector = Similarity.normalize_vector({top250[0]: 0.3, top250[1]: 0.1, top250[2]: 0.1, top250[3]: 0.5, top250[4]: 0.5})  # Близок к 2
    u3.vector = Similarity.normalize_vector({top250[0]: 0.5, top250[1]: 0.1, top250[2]: 1.0, top250[3]: 0.05, top250[4]: 0.4})  # Близок к 3
    u4.vector = Similarity.normalize_vector({top250[0]: 0.7, top250[1]: 0.5, top250[2]: 0.6, top250[3]: 0.6, top250[4]: 0.3})  # Между 1 и 2
    u5.vector = Similarity.normalize_vector({top250[0]: 0.1, top250[1]: 0.5, top250[2]: 0.5, top250[3]: 1.0, top250[4]: 1.0})  # Сам по себе
    print("euclid clusters")

    # Кластеры равно удалены друг от друга
    print("cl1 - cl2 = " + str(Similarity.euclid(cl1.vector, cl2.vector)))
    print("cl2 - cl3 = " + str(Similarity.euclid(cl2.vector, cl3.vector)))
    print("cl1 - cl3 = " + str(Similarity.euclid(cl1.vector, cl3.vector)))
    print("euclid clusters - users")
    print(str(Similarity.euclid(cl1.vector, u1.vector)) + "; " + str(Similarity.euclid(cl2.vector, u1.vector)) + "; " + str(
        Similarity.euclid(cl3.vector, u1.vector)))
    print(str(Similarity.euclid(cl1.vector, u2.vector)) + "; " + str(Similarity.euclid(cl2.vector, u2.vector)) + "; " + str(
        Similarity.euclid(cl3.vector, u2.vector)))
    print(str(Similarity.euclid(cl1.vector, u3.vector)) + "; " + str(Similarity.euclid(cl2.vector, u3.vector)) + "; " + str(
        Similarity.euclid(cl3.vector, u3.vector)))
    print(str(Similarity.euclid(cl1.vector, u4.vector)) + "; " + str(Similarity.euclid(cl2.vector, u4.vector)) + "; " + str(
        Similarity.euclid(cl3.vector, u4.vector)))
    print(str(Similarity.euclid(cl1.vector, u5.vector)) + "; " + str(Similarity.euclid(cl2.vector, u5.vector)) + "; " + str(
        Similarity.euclid(cl3.vector, u5.vector)))

    list_user = [u1, u2, u3, u4, u5]
    net = Kohonen(
        list_cluster=[],  # list_clusters
        list_source=list_user,
        similarity=Kohonen.euclid,
        allowable_similarity=0.8,
        acceptable_similarity=0.9,
        # similarity=Kohonen.manhattan,
        # allowable_similarity=0.15,
        # acceptable_similarity=0.9,
    )
    net.clustering()
    net.get_result_clustering()
    print(net.clusters)
