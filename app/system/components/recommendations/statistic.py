"""Набор утилитарных классов и методов для обеспечения математических расчетов по готовым алгоритмам."""
from scipy.spatial import distance
from scipy import stats
import math


class Similarity:
    """Методы для расчета коэффициентов сходства и другие утилитарные методы."""

    @staticmethod
    def normalize_vector(source_vector: dict) -> dict:
        """Нормализация вектора.

        :param source_vector:
        :return: dict
        """
        vector = source_vector.copy()

        sum_sqrt = pow(sum([pow(i, 2) for i in list(vector.values())]), 1 / 2)
        for (id, weight) in vector.items():
            vector[id] = weight / sum_sqrt
        return vector

    @staticmethod
    def recovery_vector(normalize_vector: dict, source_vector: dict) -> dict:
        """Восстановлние нормализованного вектора по данным исходного вектора.

        :param normalize_vector:
        :param source_vector:
        :return: dict
        """
        normalize_vector = normalize_vector.copy()
        vector = source_vector.copy()

        sum_sqrt = pow(sum([pow(i, 2) for i in list(vector.values())]), 1 / 2)
        return {id: weight * sum_sqrt for (id, weight) in normalize_vector.items()}

    @staticmethod
    def _get_lists(vector_x: dict, vector_y: dict) -> tuple:
        """Метод преобразует словари в списки значений по совпадающим ключам в обоих словарях.

        Решение использует set и map как наиболее быстрый способ (по сравнению с перебором элементов в цикле)
        для генерации списков значений по совпадающим ключам.

        :param vector_x:
        :param vector_y:
        :return: (list, list)
        """
        if (type(vector_x) is list) and (type(vector_y) is list):
            return vector_x, vector_y

        # Список одинаковых ключей.
        intersection = set(vector_x.keys()) & set(vector_y.keys())
        # Списки значений по совпадающим ключам векторов.
        items_vector_x = list(map(vector_x.get, intersection))
        items_vector_y = list(map(vector_y.get, intersection))

        return items_vector_x, items_vector_y

    @staticmethod
    def euclid(vector_x: dict, vector_y: dict) -> float:
        """Оценка подобия на основе Евклидова расстояния.

        :param vector_x:
        :param vector_y:
        :return: [0;+1]
        """
        items_vector_x, items_vector_y = Similarity._get_lists(vector_x, vector_y)
        d = distance.euclidean(items_vector_x, items_vector_y)
        return 1 / (1 + d)

    @staticmethod
    def pearson(vector_x: dict, vector_y: dict) -> float:
        """Коэффициент корреляции Пирсона.

        :param vector_x:
        :param vector_y:
        :return: [-1;+1]
        """
        items_vector_x, items_vector_y = Similarity._get_lists(vector_x, vector_y)
        pearson = stats.pearsonr(items_vector_x, items_vector_y)[0]
        return 0 if math.isnan(pearson) else pearson

    @staticmethod
    def manhattan(vector_x: dict, vector_y: dict) -> float:
        """Расстояние городских кварталов (манхэттенское расстояние).

        :param vector_x:
        :param vector_y:
        :return: [0;+1]
        """
        items_vector_x, items_vector_y = Similarity._get_lists(vector_x, vector_y)
        return distance.cityblock(items_vector_x, items_vector_y)

    @staticmethod
    def jaccard(vector_x: dict, vector_y: dict) -> float:
        """Коэффициент Жаккара. Используется для оценки схожести двух образцов.

        :param vector_x:
        :param vector_y:
        :return: [0;+1]
        """
        items_vector_x, items_vector_y = Similarity._get_lists(vector_x, vector_y)
        return distance.jaccard(items_vector_x, items_vector_y)

    @staticmethod
    def tanimoto(vector_x: dict, vector_y: dict) -> float:
        """Коэффициент Танимото. Используется для оценки схожести двух образцов.

        :param vector_x:
        :param vector_y:
        :return: [0;+1]
        """
        items_vector_x, items_vector_y = Similarity._get_lists(vector_x, vector_y)
        return distance.rogerstanimoto(items_vector_x, items_vector_y)


class Statistic(Similarity):
    """
    source - набор данных с людьми и их оценками к фильмам
    person - конкретный человек для которого определяется наилучший критик (человек с похожими оценками) и выработка рекомендации
    n - количество данных в результате
    similarity_class - класс функции сходимости
    """

    TYPE_SOURCE = 'source'
    TYPE_TRANSFORMS = 'transforms'
    TYPE_SIMILARITY_ITEMS = 'similarity_items'

    def __init__(self, source):
        self.source = source
        self.transforms = self.calculate_source_transforms()

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value

    @property
    def transforms(self):
        if hasattr(self, '_transforms') is False:
            self.transforms = self.calculate_source_transforms()
        return self._transforms

    @transforms.setter
    def transforms(self, value):
        self._transforms = value

    @property
    def similar_items(self):

        # try:
        #     f = open('item_sim.data')
        #     j = json.JSONDecoder()
        #     item_sim = j.decode(f.read())
        #     print('old calculate_similar_items')
        # except Exception as e:
        #     f = open('item_sim.data', 'w')
        #     item_sim = Statistic.calculate_similar_items(critics)
        #     j = json.JSONEncoder()
        #     f.write(j.encode(item_sim))
        #     print('new calculate_similar_items')

        if hasattr(self, '_similar_items') is False:
            self.similar_items = self.calculate_similar_items()
        return self._similar_items

    @similar_items.setter
    def similar_items(self, value):
        self._similar_items = value

    def calculate_source_transforms(self):
        """
        Преобразование людей в товары

        :return:
        """
        result = {}
        for person in self.source:
            for item in self.source[person]:
                result.setdefault(item, {})

                # Обменять местами человека и предмет
                result[item][person] = self.source[person][item]

        return result

    def calculate_similar_items(self, n=10):
        """
        Построение набора данных для сравнения образцов

        :param n:
        :return:
        """
        # Создать словарь, содержащий для каждого образца те образцы, которые больше всего похожи на него
        result = {}

        # Обратить матрицу предпочтений, чтобы строки соответствовали образцам
        item_source = self.calculate_source_transforms()
        c = 0

        for item in item_source:
            # Обновление состояния для больших наборов данных
            c += 1
            # if c % 100 == 0:
            #     print("%d / %d" % (c, len(item_source)))
            # Найти образцы, максимально похожий на данный
            scores = self.top_matches(item, n=n, source=item_source, similarity=self.euclid)
            result[item] = scores
        return result

    def top_matches(self, person: str, n: int = 5, source: str = TYPE_SOURCE, similarity: callable = None):
        """Возвращает список наилучших соответствий для человека из словаря source.

        Наиболее похожего человека мнением которого будем в последствии оперировать для выработки рекомендации.
        Количество результатов в списке и функция подобия - необязательные параметры.

        :param person:
        :param n:
        :param source:
        :param similarity:
        :return:
        """

        source = source if isinstance(source, dict) else getattr(self, source, self.source)
        similarity = similarity or self.pearson

        # Сравнение person со всеми остальными (критиками) по одной из определенных метрик
        scores = [(similarity(source[person], source[other]), other)
                  for other in source if other != person]
        # Отсортировать список по убыванию оценок
        scores.sort()
        scores.reverse()

        return scores[0:n]


class Recommendations(Statistic):
    def get_recommendations(self, person: str, n: int = 5, source: str = Statistic.TYPE_SOURCE, get_similarity: callable = None) -> list:
        """Получить рекомендации для заданного человека, пользуясь взвешенным средним оценок, данных всеми остальными пользователями.

        :param person:
        :param n:
        :param source:
        :param get_similarity:
        :return:
        """
        source = source if isinstance(source, dict) else getattr(self, source, self.source)
        get_similarity = self.pearson if get_similarity is None else get_similarity

        totals = {}
        sum_similarity = {}
        source_person = source[person]

        # Сравнение каждого пользователя с person.
        for other in source:
            # Сравнивать пользователя с собой же не нужно.
            if other == person:
                continue
            # Получение результата функции близости оценок person и other.
            similarity = get_similarity(source_person, source[other])
            # Игнорировать нулевые и отрицательные оценки.
            if similarity <= 0:
                continue

            # Построение списка рекомендаций для person исходя из его близости к other.
            for item in source[other]:
                # Оценивать только те объекты, которых нет среди оценок person.
                if item not in source_person or source_person[item] == 0:
                    # Совокупная оценка для объекта item = коэффициент подобия между person и other * оценку other.
                    # Считаем что влияние other будет незначительным благодаря низкому коэффициенту близости (и наоборот).
                    totals.setdefault(item, 0)
                    totals[item] += source[other][item] * similarity
                    # Сумма коэффициентов подобия для данного оцениваемого объекта.
                    sum_similarity.setdefault(item, 0)
                    sum_similarity[item] += similarity

        # Нормализованный список рекомендаций.
        # Оценка по каждому объекту = совокупная оценка от всех критиков / сумму коэффициентов близости всех критиков.
        rankings = {item: total / sum_similarity[item] for item, total in totals.items()}

        # Возврат отсортированного списка рекомендаций.
        return sorted(rankings.items(), key=lambda x: x[1], reverse=True)[:n]

    def get_recommendations_transforms(self, person, n=5, similarity=None):
        return self.get_recommendations(person, n, Statistic.TYPE_TRANSFORMS, similarity)

    def get_recommendations_items(self, user):
        """Выдача рекомендаций на основе сравнения образцов.

        Для выработки рекомендации по образцам набор данных можно строить заранее и использовать его при необходимости,
        в отличие от способа фильтрации по пользователям, который нужно пересчитывать постоянно при рекомендации.
        В больших массивах данных вкусы людей будут перекрываться очень слабо,
        поэтому предпочтительно сравнивать схожесть образцов
        (которая существенно меняется реже при больших объемах) и выдавать рекомендацию основываясь на ней.

        :param user:
        :return:
        """
        source = self.source
        item_match = self.similar_items

        user_ratings = source[user]
        scores = {}
        total_sim = {}

        # Цикл по образцам, оцененным данным пользователем
        for (item, rating) in user_ratings.items():

            # Цикл по образцам похожий на данный
            for (similarity, item2) in item_match[item]:

                # Пропускаем если пользователь оценил данный образец
                if item2 in user_ratings:
                    continue

                # Взвешенная суммы оценок, умноженных на коэффициент подобия
                scores.setdefault(item2, 0)
                scores[item2] += similarity * rating

                # Сумма всех коэффициентов подобия
                total_sim.setdefault(item2, 0)
                total_sim[item2] += similarity

        # Делим каждую итоговую оценку на взвешенную сумму, чтобы вычислить среднее
        rankings = [(score / total_sim[item], item) for item, score in scores.items()]

        # Вовзвращает список rankings, отсортированный по убыванию
        rankings.sort()
        rankings.reverse()
        return rankings


if __name__ == "__main__":
    # Словарь кинокитиков и выставленных ими оценок для небольшого набора данных о фильмах
    critics = {
        "Lisa Rose": {
            "Lady in the Water": 2.5,
            "Snakes on a Plane": 3.5,
            "Just My Luck": 3.0,
            "Superman Returns": 3.5,
            "You, Me, and Dupree": 2.5,
            "The Night Listener": 3.0},
        "Gene Seymour": {
            "Lady in the Water": 3.0,
            "Snakes on a Plane": 3.5,
            "Just My Luck": 1.5,
            "Superman Returns": 5.0,
            "The Night Listener": 3.0,
            "You, Me, and Dupree": 3.5},
        "Michael Phillips": {
            "Lady in the Water": 2.5,
            "Snakes on a Plane": 3.0,
            "Superman Returns": 3.5,
            "The Night Listener": 4.0},
        "Claudia Puig": {
            "Snakes on a Plane": 3.5,
            "Just My Luck": 3.0,
            "The Night Listener": 4.5,
            "Superman Returns": 4.0,
            "You, Me, and Dupree": 2.5},
        "Mick LaSalle": {
            "Lady in the Water": 3.0,
            "Snakes on a Plane": 4.0,
            "Just My Luck": 2.0,
            "Superman Returns": 3.0,
            "The Night Listener": 3.0,
            "You, Me, and Dupree": 2.0},
        "Jack Matthews": {
            "Lady in the Water": 3.0,
            "Snakes on a Plane": 4.0,
            "The Night Listener": 3.0,
            "Superman Returns": 5.0,
            "You, Me, and Dupree": 3.5},
        "Toby": {
            "Snakes on a Plane": 4.5,
            "You, Me, and Dupree": 1.0,
            "Superman Returns": 4.0}
    }

    # Тестовый прогон
    # Lisa Rose
    # Gene Seymour
    # Michael Phillips
    # Claudia Puig
    # Mick LaSalle
    # Jack Matthews
    # Toby
    test1 = 'Toby'
    test2 = 'Gene Seymour'

    movie = 'You, Me, and Dupree'

    my_stat = Recommendations(critics)

    print(
        'Люди:', test1, 'и', test2, '\n',
        'Евклидово расстояние		', my_stat.euclid(my_stat.source[test1], my_stat.source[test2]), '\n',
        'Корреляця Пирсона			', my_stat.pearson(my_stat.source[test1], my_stat.source[test2]), '\n',
        'Манхэттенское расстояние	', my_stat.manhattan(my_stat.source[test1], my_stat.source[test2]), '\n',
        '\n',
        'Ранжирование критиков		', my_stat.top_matches(test1, 2, my_stat.TYPE_SOURCE, my_stat.pearson), '\n',
        'Выработка рекомендации		', my_stat.get_recommendations(test1), '\n',
        '\n',
        'Фильмы похожие на 			', movie, my_stat.top_matches(movie, 3, my_stat.TYPE_TRANSFORMS, my_stat.pearson), '\n',
        'Кто еще не смотрел фильм	', movie, my_stat.get_recommendations_transforms(movie), '\n',
        'AAAAAAAAAA	', my_stat.transforms, '\n',
        '\n',
        'Похожие фильмы	\n			', my_stat.similar_items, '\n',
        'Выработка рекомендации	по образцам	', my_stat.get_recommendations_items(test1), '\n',
    )
