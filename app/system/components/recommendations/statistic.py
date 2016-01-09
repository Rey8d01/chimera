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


class Recommendations(Similarity):
    """Класс построения рекомендаций на основе статистических методов.

    В методах используются одинаковые термины:
    source - набор данных с людьми и их оценками к объектам;
    transformed_source - преобразованный набор данных в котором оценки фильмов по каждому человеку
    трансформируются в оценки людей  по каждому фильму;
    person - конкретный человек для которого определяется наилучший критик (человек с похожими оценками) и выработка рекомендации;


    """

    @staticmethod
    def calculate_source_transforms(source: dict) -> dict:
        """Трансформация оценщиков в оцениваемых (преобразование людей в товары).

        :param source: Исходный источник данных;
        :return: Словарь объектов с оценками людей;
        """
        result = {}
        for person in source:
            for item in source[person]:
                result.setdefault(item, {})
                # Обменять местами человека и предмет.
                result[item][person] = source[person][item]
        return result

    @staticmethod
    def calculate_similar_items(source: dict = None, transformed_source: dict = None, n=10,
                                get_similarity: callable = Similarity.euclid) -> dict:
        """Вернет список оценщиков, у каждого из которых будет список наиболее похожих на них других оценщиков.

        Построение набора данных для сравнения образцов.
        Для работы необходимо передать transformed_source, но он может быть получен если был передан source.

        :param source: Исходный источник данных;
        :param transformed_source: Трансформированный исходный источник данных с оценками образцов;
        :param n: Количество наилучших соответствий;
        :param get_similarity: Функция сходимости;
        :return: {person: [(int, other_person), ...]}
        """
        # Обратить матрицу предпочтений, чтобы строки соответствовали образцам
        transformed_source = transformed_source or Recommendations.calculate_source_transforms(source=source)
        # Создать словарь, содержащий для каждого образца те образцы, которые больше всего похожи на него
        result = {}
        c = 0

        for person in transformed_source:
            # Обновление состояния для больших наборов данных
            c += 1
            # if c % 100 == 0:
            #     print("%d / %d" % (c, len(item_source)))
            # Найти образцы, максимально похожий на данный
            scores = Recommendations.top_matches(source=transformed_source, person=person, n=n, get_similarity=get_similarity)
            result[person] = scores
        return result

    @staticmethod
    def top_matches(source: dict, person: str, n: int = 5, get_similarity: callable = Similarity.pearson) -> list:
        """Возвращает список наилучших соответствий для человека из словаря source.

        Наиболее похожего человека мнением которого будем в последствии оперировать для выработки рекомендации.
        Количество результатов в списке и функция подобия - необязательные параметры.

        :param source: Исходный источник данных;
        :param person: Имя объекта-оценщика, человек;
        :param n: Количество наилучших соответствий;
        :param get_similarity: Функция сходимости;
        :return: [(int, id_person), ...]
        """
        # Составление списка значений результатов функции сходимости между основным объектом person и всеми остальными.
        scores = [(get_similarity(source[person], source[other_person]), other_person)
                  for other_person in source if other_person != person]
        # Отсортировать список по убыванию оценок.
        scores.sort()
        scores.reverse()

        return scores[0:n]

    @staticmethod
    def get_recommendations_by_person_for_person(source: dict, person: str, source_person: dict = None, n: int = 5,
                                                 get_similarity: callable = Similarity.pearson) -> list:
        """Коллаборативная фильтрация по схожести пользователей.

        :param source: Исходный источник данных;
        :param person: Имя объекта-оценщика, человек;
        :param source_person: Набор данных оценок человека (Если не задано берется из source по person);
        :param n: Количество наилучших соответствий;
        :param get_similarity: Функция сходимости;
        :return:
        """
        source_person = source_person or source[person]
        totals = {}
        sum_similarity = {}

        # Сравнение каждого пользователя с person.
        for other_person in source:
            # Сравнивать пользователя с собой же не нужно.
            if other_person == person:
                continue
            # Получение результата функции близости оценок person и other.
            similarity = get_similarity(source_person, source[other_person])
            # Игнорировать нулевые и отрицательные оценки.
            if similarity <= 0:
                continue

            # Построение списка рекомендаций для person исходя из его близости к other.
            for item in source[other_person]:
                # Оценивать только те объекты, которых нет среди оценок person.
                if item not in source_person or source_person[item] == 0:
                    # Совокупная оценка для объекта item = коэффициент подобия между person и other * оценку other.
                    # Считаем что влияние other будет незначительным благодаря низкому коэффициенту близости (и наоборот).
                    totals.setdefault(item, 0)
                    totals[item] += source[other_person][item] * similarity
                    # Сумма коэффициентов подобия для данного оцениваемого объекта.
                    sum_similarity.setdefault(item, 0)
                    sum_similarity[item] += similarity

        # Нормализованный список рекомендаций.
        # Оценка по каждому объекту = совокупная оценка от всех критиков / сумму коэффициентов близости всех критиков.
        rankings = {item: total / sum_similarity[item] for item, total in totals.items()}

        # Возврат отсортированного списка рекомендаций.
        return sorted(rankings.items(), key=lambda x: x[1], reverse=True)[:n]

    @staticmethod
    def get_recommendations_by_items_for_person(person: str, source: dict = None, source_similar_items: dict = None,
                                                get_similarity: callable = Similarity.euclid) -> list:
        """Коллаборативная фильтрация по схожести образцов.

        Для выработки рекомендации по образцам набор данных можно строить заранее и использовать его при необходимости,
        в отличие от способа фильтрации по пользователям, который нужно пересчитывать постоянно при рекомендации.
        В больших массивах данных вкусы людей будут перекрываться очень слабо,
        поэтому предпочтительно сравнивать схожесть образцов
        (которая существенно меняется реже при больших объемах) и выдавать рекомендацию основываясь на ней.

        Для работы нужно передать источник данных source_similar_items но он может быть получен если передать source.

        :param source: Исходный источник данных оценок пользователей;
        :param source_similar_items: Исходный источник данных оценок образцов;
        :param person: Объект-оценщик, человек;
        :param get_similarity: Функция сходимости;
        :return:
        """
        source_similar_items = source_similar_items or Recommendations.calculate_similar_items(source=source, get_similarity=get_similarity)
        user_ratings = source[person]
        scores = {}
        total_sim = {}

        # Цикл по образцам, оцененным данным пользователем
        for (item, rating) in user_ratings.items():

            # Цикл по образцам похожий на данный
            for (similarity, other_item) in source_similar_items[item]:

                # Пропускаем если пользователь оценил данный образец
                if other_item in user_ratings:
                    continue

                # Взвешенная суммы оценок, умноженных на коэффициент подобия
                scores.setdefault(other_item, 0)
                scores[other_item] += similarity * rating

                # Сумма всех коэффициентов подобия
                total_sim.setdefault(other_item, 0)
                total_sim[other_item] += similarity

        # Делим каждую итоговую оценку на взвешенную сумму, чтобы вычислить среднее
        rankings = [(score / total_sim[item], item) for item, score in scores.items()]

        # Возвращает список rankings, отсортированный по убыванию
        rankings.sort()
        rankings.reverse()
        return rankings

    @staticmethod
    def get_recommendations_by_items_for_item(item: str, source: dict = None, transformed_source: dict = None, n: int = 5,
                                              get_similarity: callable = Similarity.pearson):
        """

        :param source:
        :param transformed_source:
        :param item:
        :param n:
        :param get_similarity:
        :return:
        """
        transformed_source = transformed_source or Recommendations.calculate_source_transforms(source=source)
        return Recommendations.get_recommendations_by_person_for_person(source=transformed_source, person=item, n=n,
                                                                        get_similarity=get_similarity)


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

    items = Recommendations.calculate_source_transforms(source=critics)

    print(
            'Люди:', test1, 'и', test2, '\n',
            'Евклидово расстояние		', Similarity.euclid(critics[test1], critics[test2]), '\n',
            'Корреляця Пирсона			', Similarity.pearson(critics[test1], critics[test2]), '\n',
            'Манхэттенское расстояние	', Similarity.manhattan(critics[test1], critics[test2]), '\n',
            '\n',
            'Ранжирование критиков		', Recommendations.top_matches(source=critics, person=test1, n=2), '\n',
            'Выработка рекомендации		', Recommendations.get_recommendations_by_person_for_person(source=critics, person=test1), '\n',
            '\n',
            'Фильмы похожие на 			', movie, Recommendations.top_matches(source=items, person=movie, n=3), '\n',
            'Кто еще не смотрел фильм	', movie,
            Recommendations.get_recommendations_by_items_for_item(transformed_source=items, item=movie), '\n',
            'AAAAAAAAAA	', items, '\n',
            '\n',
            'Похожие фильмы	\n			', Recommendations.calculate_similar_items(transformed_source=items, n=3), '\n',
            'Выработка рекомендации	по образцам	',
            Recommendations.get_recommendations_by_items_for_person(person=test1, source=critics), '\n',
    )
