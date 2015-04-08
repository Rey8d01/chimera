__author__ = 'rey'

from system.components.recommendations.statistic import Similarity
from abc import abstractmethod, abstractproperty
import operator

class KohonenExceptionClustering(Exception):
    """
    Исключение для процесса кластеризации
    """
    pass


class ClusterExtractor():
    """
    Класс прослойка для реализации методов пригодных для работы с каждым нейроном сети
    """

    @abstractmethod
    def get_cluster_id(self):
        pass

    @abstractmethod
    def set_cluster_id(self, cluster_id):
        pass

    @abstractmethod
    def get_cluster_vector(self):
        pass

    @abstractmethod
    def set_cluster_vector(self, cluster_vector):
        pass


class ItemExtractor():
    """
    Интерфейсный класс который необходимо отнаследовать для класса с образцами данных.
    Методы этого интерфейса должны реализовать функционал для доступа к данным образца, которые пройдут этап кластеризации.
    """

    @abstractmethod
    def get_item_id(self):
        """
        Должен вернуть уникальный id образца, например id в БД.

        :return: str
        """

    @abstractmethod
    def get_item_name(self):
        """
        Должен вернуть человекопонятное имя образца, например имя человека.

        :return: str
        """

    @abstractmethod
    def get_item_vector(self):
        """
        Должен вернуть массив с данными для кластеризации, например массив оценок к фильмам.

        dict(id1: rate1, id2: rate2, ... idN: rateN)

        :return: dict
        """

    @abstractmethod
    def associate_cluster(self, cluster_name):
        """
        Методу передается имя кластера к которому будет принадлежать образец. Для удобства воспроизведение этой информации
        желательно ее записать в специальное поле.
        """

    count_recommendation = 10
    list_recommendation = None

    def set_item_recommendation(self, beta_vector):
        # Сортировка оценок в порядке убывания: начиная с наибольшей, заканчивая наименьшей
        # Выполняется срез по установленному количеству
        return sorted(beta_vector.items(), key=lambda x: -x[1])[:self.count_recommendation]


class Kohonen(Similarity):
    """
    Сеть Кохонена для кластеризации.

    1. Определяются образцы для классификации/кластеризации. Если сеть уже была в работе и сохранила свои результаты их так же можно
    передать.
    2. Задаются критерии работы сети (функция расчета коэффициента сходства, коэффициенты для обучения сети).
    3. На начальном этапе обучения сети рекомендуется провести кластеризацию на ограниченной выборке случайных образцов.
    4. Для продолжения обучения сети следует передать оставшиеся образцы для классификации по созданным кластерам.
    5. Работа сети может осуществлятся с передачей ей определенного образца для определения его класса.

    :type _similarity: callable Функция расчета коэффициента сходства
    :type _allowable_similarity: float Минимальный допустимый коэффициент сходства для присоединения образца к существующему кластеру
    :type _acceptable_similarity: float Минимальный приемлемый коэффициент сходства для присоединения образца к существующему кластеру
                                        без изменения его прототипа
    :type _alpha_learning: float Коэффициент обучения, понижающийся в процессе. Альфа потому что первый, первый слой в сети.
    :type _clusters: list[ClusterExtractor] Массив данных кластеров
    :type _item_cluster: dict[list] Временная информация о закрепленных к кластерам обрзцах
    :type _max_deep: int Макисмальная глубина рекурсии по достижении которого обучение останавливается
    :type _current_deep: int Текущий уровень глубины рекурсии при обучении
    :type _components: list[str] Компоненты векторов (список ид всех параметров которые могут быть у образцов и обязательно все будут в
                                 кластерных векторах)
    :type _cluster_class: ClusterExtractor
    :type _default_weight: int
    """

    _similarity = None
    _allowable_similarity = None
    _acceptable_similarity = None
    _alpha_learning = None
    _clusters = None
    _cluster_class = None
    _item_cluster = None
    _max_deep = None
    _current_deep = 0
    _components = None
    _default_weight = 0

    @property
    def clusters(self):
        """
        :return: dict[dict]
        """
        return self._clusters

    def __init__(self, list_cluster=None, similarity=None, allowable_similarity=None,
                 acceptable_similarity=None, _max_deep=None, components=None, cluster_class=None):
        """
        Инициализация кластеров. Инстанс сети Кохонена содержит в свойстве resource список кластеров фильмов и весов.

        :param list_cluster: Список кластеров (список из классов KohonenClusterDocument)
        :type list_cluster: list[KohonenClusterDocument]
        :param similarity:
        :type similarity: callable
        :param allowable_similarity:
        :type allowable_similarity: float
        :param acceptable_similarity:
        :type acceptable_similarity: float
        :param components:
        :type components: list[str]
        :param cluster_class:
        :type cluster_class: ClusterExtractor
        :return:
        """
        print("Инициализация сети Кохонена")
        # Установка стандартных значений на этапе инициализации
        self._similarity = similarity if similarity is not None else self.euclid
        self._allowable_similarity = allowable_similarity if allowable_similarity is not None else 0.55
        self._acceptable_similarity = acceptable_similarity if acceptable_similarity is not None else 0.95
        self._max_deep = _max_deep if _max_deep is not None else 200
        self._components = components if components is not None else top250
        self._clusters = list_cluster if list_cluster is not None else []
        self._cluster_class = cluster_class if cluster_class is not None else ClusterExtractor
        print("Инициализировано кластеров " + str(len(self._clusters)))
        self._item_cluster = {}
        # Расчет значения весового коэффициента принимаемого по умолчанию
        self._default_weight = 1 / pow(len(self._components), 1 / 2)

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
        # Экземпляр нового кластера
        cluster = self._cluster_class()
        # Установка его ид
        cluster.set_cluster_id("cluster" + str(len(self._clusters) + 1))

        # Заполняем новый кластер стандартными значениями весов для каждого фильма или веса задаются под вектор
        if vector is None:
            cluster_vector = {component: self._default_weight for component in self._components}
        else:
            vector_components = list(vector.keys())
            cluster_vector = {component: vector[component] if component in vector_components else self._default_weight
                              for component in self._components}
        cluster.set_cluster_vector(cluster_vector)
        # Добавляем новый класстер в сеть
        self._clusters.append(cluster)
        print("Создание нового кластера завершено, кластеров в сети " + str(len(self._clusters)))

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
        list_cluster = [cluster for cluster in self._clusters if cluster.get_cluster_id() in used_cluster]
        self._clusters = list_cluster
        print("Актуализация завершена, в сети кластеров " + str(len(self._clusters)))

    def get_result_clustering(self):
        """
        Итог обучения
        Список фенотипов и их прототипов

        :return:
        """
        cluster_item = {}
        for cluster in self._clusters:
            cluster_id = cluster.get_cluster_id()
            cluster_item[cluster_id] = [item_id for (item_id, item_cluster_name) in self._item_cluster.items() if
                                        item_cluster_name == cluster_id]
            print(cluster_id + " - " + str(cluster_item[cluster_id]))
        return cluster_item

    def learning(self, source=None, start_alpha_learning=0.8, clustering=True, callback_after_learn_item=None):
        """
        Процесс обучения сети по массе образцов.

        :param source: Массив данных образцов для обучения
        :type source: list[ItemExtractor]
        :param start_alpha_learning:  Начальный коэффициент при обучении, по умолчанию стремится к 1
        :type start_alpha_learning: float
        :return:
        """
        self._alpha_learning = start_alpha_learning
        try:
            # Перебор всех элементов для их кластеризации
            for item in source:
                item_id = item.get_item_id()
                item_name = item.get_item_name()
                item_vector = self.normalize_vector(item.get_item_vector())
                cluster = self._clustered(item_id, item_name, item_vector) if clustering else \
                    self._classify(item_id, item_name, item_vector)
                item.associate_cluster(cluster.get_cluster_id())
                import types
                if callback_after_learn_item is not None:
                    # :type callback_after_learn_item: callable
                    callback_after_learn_item(item, cluster)
        except KohonenExceptionClustering:
            self._current_deep += 1
            if self._current_deep < self._max_deep:
                # Создаем новый кластер - новый кластер наследует характеристики основателя (текущего образца)
                self.create_cluster(item_vector)
                # Перезапускаем процесс кластеризации для того, что бы новый кластер тоже учитывался при сравнении со всеми образцами
                print("Переобучение сети, глубина " + str(self._current_deep))
                return self.learning(source=source,
                                     start_alpha_learning=self._alpha_learning,
                                     callback_after_learn_item=callback_after_learn_item)
            else:
                print("Достигнута максимальная глубина, дальнейшее обучение сети невозможно!")

        print("Завершение кластеризации")
        self.actualize_clusters()

    def classify_item(self, item, start_alpha_learning=0.1):
        """
        Процесс работы сети по одному экземпляру.

        :type start_alpha_learning: int Начальный коэффициент при работе много меньше чем при обучении
        :param item: ItemExtractor
        :return:
        :rtype: ClusterExtractor
        """
        self._alpha_learning = start_alpha_learning

        item_id = item.get_item_id()
        item_name = item.get_item_name()
        item_vector = self.normalize_vector(item.get_item_vector())
        return self._classify(item_id, item_name, item_vector)

    def _clustered(self, item_id, item_name, item_vector):
        """
        Процесс кластерного анализа по одному объекту.
        Для создания кластера используется матрица расстояний и коэффцициент минимального допустимого сходства.

        :param item_id:
        :type item_id: str
        :param item_name:
        :type item_name: str
        :param item_vector:
        :type item_vector: dict
        :return: ClusterExtractor
        :rtype: ClusterExtractor
        """
        # После сравнения всех кластеров с текущим элементом - получаем максимальный коэффициент сходства
        # (минимальное расстояние, максимальную корреляцию, максимальная близость)
        similarity_cluster, max_similarity = self.get_similarity_cluster(item_vector)

        # Условие допустимого сходства
        if max_similarity < self._allowable_similarity or (similarity_cluster is None):
            # Если коэффициент сходства, среди всех кластеров, меньше допустимого порога, это значит что образец находится слишком далеко
            # и на этапе обучения это порождает новый кластер, а на этапе работы сети следует оценить необходимость переобучения сети.
            raise KohonenExceptionClustering

        # Если расчитанный максимальный коэффициент сходства удовлетворяет условию минимального допустимого коэффициента сходства 
        # то интегрируем образец в кластер. Но если степень сходимости меньше минимальное приемлемой, то прототип кластера необходимо 
        # скорректировать - иначе говоря обучить сеть, скорректировать ее веса.
        if max_similarity < self._acceptable_similarity:
            cluster_vector = similarity_cluster.get_cluster_vector()
            # Коррекция весов только по тем позициям, которые имеются в новом фенотипе
            # Обучение (методом) поиска среднего
            for (component, weight) in item_vector.items():
                cluster_vector[component] = (weight * max_similarity + cluster_vector[component]) / 2

        self._item_cluster[item_id] = similarity_cluster.get_cluster_id()
        return similarity_cluster

    def get_similarity_cluster(self, vector):
        """
        Вернет ближайший кластер

        :param vector:
        :type vector: dict
        :return: similarity_cluster, max_similarity
        :rtype: (ClusterExtractor, int)
        """
        max_similarity = 0
        similarity_cluster = None
        for cluster in self._clusters:
            similarity = self._similarity(vector, cluster.get_cluster_vector())
            if max_similarity <= similarity:
                max_similarity = similarity
                similarity_cluster = cluster
        return similarity_cluster, max_similarity

    def _classify(self, item_id, item_name, item_vector):
        """
        Процесс классификации для обученной сети.

        :param item_id:
        :type item_id: str
        :param item_name:
        :type item_name: str
        :param item_vector:
        :type item_vector: dict
        :return: ClusterExtractor
        :rtype: ClusterExtractor
        """
        # Поиск нейрона-победителя
        max_net = 0
        winner_cluster = None
        for cluster in self._clusters:
            cluster_vector = cluster.get_cluster_vector()
            current_net = sum([cluster_vector[component] * item_vector[component] for component in item_vector.keys()])
            if max_net <= current_net:
                max_net = current_net
                winner_cluster = cluster

        # Коррекция весов для победившего нейрона
        cluster_vector = winner_cluster.get_cluster_vector()
        for (component, weight) in item_vector.items():
            cluster_vector[component] += self._alpha_learning * (weight - cluster_vector[component])

        # Понижение коэффициента скорости обучения
        self._alpha_learning -= 0.001 if self._alpha_learning > 0.1 else 0

        return winner_cluster


class GrossbergMulti():
    """
    Сеть Гроссберга по модели зависимой от слоя Кохонена

    """
    _beta_vector = None
    _beta_learning = None
    _start_beta_learning = None
    _minus_beta = None
    _components = None

    @property
    def beta_vector(self):
        return self._beta_vector

    def __init__(self, components=None, count_items=None, start_beta_learning=None):
        """

        :param components:
        :type components: list[str]
        :param count_items:
        :type count_items: int
        :param start_beta_learning:
        :type start_beta_learning: float
        :return:
        """
        print("Инициализация сети Гроссберга")
        self._components = components if components is not None else top250
        self._beta_vector = {}
        self._beta_learning = {}
        # Определение степени понижения обучения слоя Гроссберга
        self._start_beta_learning = start_beta_learning if start_beta_learning is not None else 0.8
        self._minus_beta = self._start_beta_learning / count_items if count_items > 0 else 0.0001

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
        print("Обучение слоя Гроссберга")
        item_vector = item.get_item_vector()
        cluster_vector = cluster.get_cluster_vector()
        cluster_id = cluster.get_cluster_id()

        # С целью повысить динамику у необученных векторов (и снизить динамику обучения у переученных) устанавливается,
        # что коэффициенты обучения для разных кластеров сети Кохонена будут своими
        if cluster_id not in self._beta_learning:
            self._beta_learning[cluster_id] = self._start_beta_learning
        # В случае если в сети Гроссберга нейрон Кохонена не был определен, для него создаются веса по умолчанию
        if cluster_id not in self._beta_vector:
            self._beta_vector[cluster_id] = {component: 0.6 for component in self._components}

        # Корректировка весов
        cluster_beta_vector = self._beta_vector[cluster_id]
        for component in self._components:
            item_component = item_vector[component] if component in item_vector else 0
            cluster_beta_vector[component] += self._beta_learning[cluster_id] * (item_component - cluster_beta_vector[component]) * cluster_vector[component]

        # Понижение коэффициента обучения
        self._beta_learning[cluster_id] -= self._minus_beta

        item.set_item_recommendation(cluster_beta_vector.copy())
        return cluster_beta_vector


class GrossbergSingle():
    """
    Сеть Гроссберга по модели частично зависимой от слоя Кохонена

    """
    _ideal_vector = None
    _beta_learning = None
    _start_beta_learning = None
    _minus_beta = None
    _components = None

    def __init__(self, components=None, count_items=None, start_beta_learning=None):
        self._components = components if components is not None else top250
        self._ideal_vector = {component: 0.6 for component in self._components}
        self._beta_learning = {}
        self._start_beta_learning = start_beta_learning if start_beta_learning is not None else 0.8
        self._minus_beta = self._start_beta_learning / count_items if count_items > 0 else 0.0001

    def learning(self, item, cluster):
        item_vector = item.get_item_vector()
        cluster_vector = cluster.get_cluster_vector()
        cluster_id = cluster.get_cluster_id()
        if cluster_id not in self._beta_learning:
            self._beta_learning[cluster_id] = self._start_beta_learning
        for component in self._components:
            item_component = item_vector[component] if component in item_vector else 0
            self._ideal_vector[component] += self._beta_learning[cluster_id] * (item_component - self._ideal_vector[component]) * \
                                             cluster_vector[component]
        self._beta_learning[cluster_id] -= self._minus_beta

        item.set_item_recommendation(self._ideal_vector.copy())
        return self._ideal_vector


class CPN():
    """
    Counterpropagation network
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

    def run(self, source=None, clustering=True):
        """

        :param source:
        :param start_alpha_learning:
        :param clustering:
        :return:
        """
        self.net_kohonen.learning(source=source,
                                  clustering=clustering,
                                  # Возбуждение нейронов Гроссберга, срабатывает после того как слой Кохонена сформирует ответ
                                  callback_after_learn_item=self.net_grossberg.learning)


############################################################################################################################################

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

from motorengine import Document, StringField, BaseField


class ClusterDocument(Document):
    __collection__ = "kohonenCluster"

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


if __name__ == "__main__":
    print("Демонстрация сети Кохонена")

    cl1 = KohonenClusterExtractor()
    cl2 = KohonenClusterExtractor()
    cl3 = KohonenClusterExtractor()
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
        cluster = None

        def get_item_id(self):
            return self.id

        def get_item_name(self):
            return self.name

        def get_item_vector(self):
            return self.vector

        def associate_cluster(self, cluster_name):
            self.cluster = cluster_name

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
    net_kohonen = Kohonen(
        # list_cluster=list_clusters,
        similarity=Kohonen.euclid,
        allowable_similarity=0.8,
        acceptable_similarity=0.9,
        # similarity=Kohonen.manhattan,
        # allowable_similarity=0.15,
        # acceptable_similarity=0.9,
        components=top250,
        cluster_class=KohonenClusterExtractor
    )
    net_kohonen.learning(source=list_user)
    net_kohonen.get_result_clustering()
    print(net_kohonen.clusters)
    print(net_kohonen.classify_item(u5))

    net_grossberg = GrossbergSingle(
        components=top250,
        count_items=len(list_user)
    )

    net_cpn = CPN(
        net_kohonen=net_kohonen,
        net_grossberg=net_grossberg,
    )

    net_cpn.run(
        source=list_user,
        clustering=True
    )

    # print(net_kohonen.clusters[0])
    l = net_grossberg.learning(u1, net_kohonen.clusters[0])
    print({top250[0]: l[top250[0]], top250[1]: l[top250[1]], top250[2]: l[top250[2]], top250[3]: l[top250[3]], top250[4]: l[top250[4]]})
    print(u1.get_item_vector())

    print('Завершено')
