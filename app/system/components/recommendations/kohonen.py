__author__ = 'rey'

from motorengine import Document, StringField, BaseField
from documents.fake import UserDocument
from system.components.recommendations.statistic import Similarity

from tornado import gen

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
    pass


class ItemExtractor():
    def get_item_id(self):
        pass

    def get_item_name(self):
        pass

    def get_item_vector(self):
        pass


class Kohonen(Similarity):
    """
    Сеть Кохонена для кластеризации
    """

    similarity = None
    # Минимальная допустимая сепень схожести для присоединения к существующему кластеру
    allowable_similarity = 0.2
    # Минимальная приемлемая степень схожести для присоединения к сущесвующему кластеру без изменения его прототипа
    acceptable_similarity = 0.9
    _clusters = None
    _item_cluster = None
    _source = None

    deep = 0

    @property
    def clusters(self):
        """
        :return: dict
        """
        return self._clusters

    @property
    def source(self):
        """
        :return: list[ItemExtractor]
        """
        return self._source

    @gen.engine
    def __init__(self, list_cluster=None, list_source=None, similarity=None):
        """
        Инициализация кластеров. Инстанс сети Кохонена содержит в свойстве resource список кластеров фильмов и весов.

        :param list_cluster: Список кластеров (список из классов KohonenClusterDocument)
        :return:
        """

        self.similarity = similarity if similarity is not None else self.pearson

        # Населяем сеть кластерами из базы или по переданной информации
        if list_cluster is None:
            pass
            # todo
            # list_cluster = yield KohonenClusterDocument().objects.find_all()
        if not isinstance(list_cluster, list) or not len(list_cluster) > 0:
            list_cluster = []

        clusters = {}
        for document_cluster in list_cluster:
            clusters[str(document_cluster.name)] = document_cluster.vector
        self._clusters = clusters
        self._item_cluster = {}

        # Если сеть пустая то создадим тестовый кластер для начала работы
        if len(self._clusters) == 0:
            self.create_cluster()

        self._source = list_source

    def create_cluster(self, vector=None):
        """
        Создание универсального кластера необходимо для динамического создания нейронов.
        Что бы создать универсальный кластер необходимо посчитать количество фильмов (М)
        создать случайный вектор весов (количество весовых коэфициентов = М).
        Для кластеров выделена отдельная коллекция, каждый кластер имеет свой документ.

        Так как количество фильмов может динамически изменятся,
        то необходимо контролировать идентефикаторы для весов и фильмов к которым они соотносятся

        Возвращается человеческий ид кластера для последующего к нему обращения
        :return:
        """
        document_cluster = KohonenClusterDocument()
        document_cluster.name = "cluster" + str(len(self._clusters) + 1)
        # заполняем новый кластер случайными значениями весов для каждого фильма
        # или не случайными если кластер задается под вектор
        if vector is None:
            document_cluster.vector = {id: 0 for id in top250}
        else:
            keys_vector = list(vector.keys())
            document_cluster.vector = {id: vector[id] if id in keys_vector else 0 for id in top250}

        # Добавляем новый класстер в сеть
        self._clusters[document_cluster.name] = document_cluster.vector

        # document_cluster.save()
        return document_cluster.name

    def processing(self, ):
        """

        :type source: list[ItemExtractor]
        :return:
        """
        source = self._source

        try:
            # Перебор всех элементов для их кластеризации
            for item in source:
                item_id = item.get_item_id()
                item_name = item.get_item_name()
                item_vector = self.normalize_vector(item.get_item_vector())

                # dict в котором будут храниться информация о расстояниях (схожести)
                # от текущего элемента до каждого кластера
                similarity = {}
                for (cluster_name, cluster_vector) in self._clusters.items():
                    similarity[cluster_name] = self.similarity(item_vector, cluster_vector)
                # После сравнения всех кластеров с текущим элементом - получаем максимальную степень схожести
                # (минимальное расстояние, максимальную корреляцию, максимальная близость)
                cluster_name_max_similarity = max(similarity, key=similarity.get)
                max_similarity = similarity[cluster_name_max_similarity]

                # Условие допустимой схожести
                if max_similarity < self.allowable_similarity:
                    # print("max_similarity < self.allowable_similarity")

                    # Если степень схожести, среди всех кластеров, меньше допустимого порога,
                    # то создаем новый кластер, к которому будет относится данный образец
                    # Создаем новый кластер - новый кластер наследует характеристики основателя (текущего образца)
                    self.create_cluster(item_vector)
                    # Перезапускаем процесс кластеризации для того, что бы новый кластер тоже учитывался
                    # при сравнении со всеми образцами
                    raise KohonenExceptionClustering
                else:
                    # Если расчитанная максимальная схожесть удовлетворяет условию минимальной допустимой схожести
                    # то интегрируем образец в кластер
                    # Но если степень сходимости меньше минимальное приемлемой,
                    # то прототип кластера необходимо скорректировать - иначе говоря обучить сеть, скорректировать ее веса
                    if max_similarity < self.acceptable_similarity:
                        # print("max_similarity < self.acceptable_similarity")
                        # print(item_vector.items())
                        # Коррекция весов только по тем позициям, которые имеются в новом фенотипе
                        for (id, weight) in item_vector.items():
                            self._clusters[cluster_name_max_similarity][id] = \
                                (weight * max_similarity + self._clusters[cluster_name_max_similarity][id]) / 2

                            # запись изменений

                self._item_cluster[item_id] = cluster_name_max_similarity
        except KohonenExceptionClustering:
            self.deep += 1
            if self.deep < 100:
                return self.processing()
            else:
                print("max recursion")

        self.delete_empty_clusters()
        print("deep="+str(self.deep))

    def delete_empty_clusters(self):
        """
        Ищет и удаляет неиспользуемые кластеры

        :return:
        """
        # Сбор уникальных имен используемых кластеров
        used_clusters_name = list(self._item_cluster.values())
        used_cluster = []
        [used_cluster.append(item) for item in used_clusters_name if item not in used_cluster]
        # Удаление кластеров, которые не приписаны ни одному образцу
        all_clusters_name = list(self._clusters.keys())
        print("к этому моменту создано кластров "+str(len(all_clusters_name)))
        [self._clusters.pop(cluster_name) for cluster_name in all_clusters_name if cluster_name not in used_cluster]

    def clustering(self):
        """
        Задача универсального кластера - если расстояние между входным вектором и нейроном кластера минимально то этот вектор относится к этому кластеру.
        Процесс кластеризации. На входе функция получает массив кластеров и наборы данных
        :return:
        """
        pass


