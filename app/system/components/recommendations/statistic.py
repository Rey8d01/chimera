__author__ = 'rey'

# Используем JSON для преобразования объекта словаря в текст и обратно
import json
from math import sqrt, fabs, floor
# from similarity import SimilarityDistance, SimilarityPearson, SimilarityJaccard, SimilarityManhattan


class Similarity:
    """ Методы для расчета коэффициентов сходства """

    @staticmethod
    def normalize_vector(vector):
        """
        Нормализация вектора

        :param vector:
        :return:
        """
        values_item_vector = list(vector.values())
        sum_sqrt = pow(sum([pow(i, 2) for i in values_item_vector]), 1/2)
        for (id, weight) in vector.items():
            vector[id] = weight/sum_sqrt
        return vector

    @staticmethod
    def normalize_weight(weight, vector):
        """
        Нормализация значения в векторе

        :param weight:
        :param vector:
        :return:
        """
        return weight/pow(sum([pow(i, 2) for i in vector]), 1/2)

    @staticmethod
    def euclid(vector1, vector2):
        """
        Оценка подобия на основе Евклидова расстояния
        [0;+1]

        :type vector1: dict
        :type vector2: dict
        :return:
        """
        # Получить список предметов, оцененных обоими
        si = {}
        for item in vector1:
            if item in vector2:
                si[item] = 1

        # Если нет ни одной общей оценки вернуть 0
        # если нет ни одного предмета который оценили бы оба
        if len(si) == 0: return 0

        # Сложить квадраты разностей
        sum_of_squares = sum([pow(vector1[item] - vector2[item], 2) for item in vector1 if item in vector2])

        return round(1 / (1 + sum_of_squares), 3)

    @staticmethod
    def pearson(vector1, vector2):
        """
        Коэффициент корреляции Пирсона
        [-1;+1]

        :type vector1: dict
        :type vector2: dict
        :return: double
        """
        # Получить список предметов оцененных обоими
        si = {}
        for item in vector1:
            if item in vector2:
                si[item] = 1

        # Найти число элементов
        n = len(si)

        # Если нет ни одной общей оценки, вернуть 0
        if n == 0:
            return 0

        # Вычислить сумму всех предпочтений
        sum1 = sum([vector1[it] for it in si])
        sum2 = sum([vector2[it] for it in si])

        # Вычислить сумму квадратов
        sum1sq = sum([pow(vector1[it], 2) for it in si])
        sum2sq = sum([pow(vector2[it], 2) for it in si])

        # Вычислить сумму произведений
        psum = sum([vector1[it] * vector2[it] for it in si])

        # Вычислить коэффициент Пирсона
        num = psum - (sum1 * sum2 / n)
        den = sqrt((sum1sq - pow(sum1, 2) / n) * (sum2sq - pow(sum2, 2) / n))
        if den == 0:
            return 0

        return round(num / den, 3)

    @staticmethod
    def jaccard(vector1, vector2):
        """
        Коэффициент Жаккара (Танимото)
        Используется для оценки схожести двух образцов
        [0;+1]

        :type vector1: dict
        :type vector2: dict
        :return:
        """
        # Получить количество предметов оцененных обоими
        si = 0
        for item in vector1:
            if item in vector2:
                si = si + 1

        return round(si / (len(vector1) + len(vector2) - si), 3)

    @staticmethod
    def tanimoto(vector1, vector2):
        return Similarity.jaccard(vector1, vector2)

    @staticmethod
    def manhattan(vector1, vector2):
        """
        Расстояние городских кварталов (манхэттенское расстояние)
        [0;+1]

        :type vector1: dict
        :type vector2: dict
        :return:
        """
        # Получить список предметов, оцененных обоими
        si = {}
        for item in vector1:
            if item in vector2:
                si[item] = 1

        # Если нет ни одной общей оценки вернуть 0
        if len(si) == 0: return 0

        # Сложить модули разностей
        sum_of_abs = sum([fabs(vector1[item] - vector2[item])
                          for item in vector1 if item in vector2])

        return round(1 / (1 + sum_of_abs), 3)


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

    def top_matches(self, person, n=5, source=TYPE_SOURCE, similarity=None):
        """
        Возвращает список наилучших соответствий для человека из словаря source
        - наиболее похожего человека мнением которого будем в последствии оперировать для выработки рекомендации
        Количество результатов в списке и функция подобия - необязательные параметры

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

    def get_recommendations(self, person, n=5, source=Statistic.TYPE_SOURCE, similarity=None):
        """
        Получить рекомендации для заданного человека, пользуясь взвешенным средним оценок,
        данных всеми остальными пользователями

        :param source:
        :param person:
        :param n:
        :param similarity:
        :return:
        """

        source = source if isinstance(source, dict) else getattr(self, source, self.source)
        similarity = self.pearson if similarity is None else similarity

        totals = {}
        sim_sums = {}

        for other in source:
            # Сравнивать пользователя с собой же не нужно
            if other == person:
                continue
            sim = similarity(source[person], source[other])

            # Игнорировать нулевые и отрицательные оценки
            if sim <= 0:
                continue

            for item in source[other]:
                # Оценивать только то что нет среди оценок пользователя person
                if item not in source[person] or source[person][item] == 0:
                    # Коэффициент подибия * Оценка
                    totals.setdefault(item, 0)
                    totals[item] += source[other][item] * sim
                    # Сумма коэффициентов подобия
                    sim_sums.setdefault(item, 0)
                    sim_sums[item] += sim

        # Создать нормализованный список
        rankings = [(round(total / sim_sums[item], 3), item) for item, total in totals.items()]

        # Вернуть отсортированный список
        rankings.sort()
        rankings.reverse()

        return rankings[0:n]

    def get_recommendations_transforms(self, person, n=5, similarity=None):
        return self.get_recommendations(person, n, Statistic.TYPE_TRANSFORMS, similarity)

    # def get_recommendations_items(self, source, item_match, user):
    def get_recommendations_items(self, user):
        """
        Выдача рекомендаций на основе сравнения образцов

        Для выработки рекомендации по образцам набор данных можно строить заранее и использовать его при необходимости,
        в отличие от способа фильтрации по пользователям, который нужно пересчитывать постоянно при рекомендации.
        В больших массивах данных вкусы людей будут перекрываться очень слабо,
        поэтому предпочтительно сравнивать схожесть образцов
        (которая существенно меняется реже при больших объемах) и выдавать рекомендацию основываясь на ней

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
        'Коэффициент Жаккара		', my_stat.jaccard(my_stat.source[test1], my_stat.source[test2]), '\n',
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