"""Укомлпектованный набор классов для работы различных конфигураций сети встречного распространения и статистики.

StatisticForUserHandler реализует подсчет статистики для пользователя.
StatisticForMovieHandler реализует подсчет статистики по данным оценкам к фильму.

"""
import random
import system.utils.exceptions
from system.handler import BaseHandler
# from documents.user import UserDocument
from documents.recommendation.cpn import KohonenClusterExtractor, GrossbergOutStarExtractor  # , UserItemExtractor
from documents.recommendation.fake import FakeUserItemExtractor as UserItemExtractor, FakeUserDocument as UserDocument
from system.components.recommendations.cpn import Kohonen, GrossbergOutStar, CPN, top250
from system.components.recommendations.statistic import Recommendations, Similarity
from bson.objectid import ObjectId

"""
# todo
user1 = "5501eec480a9e10c639d60e0"
user2 = "5501eec480a9e10c639d60e4"
movie = "tt0407887"
# todo
"""


class StatisticForUserHandler(BaseHandler):
    """Класс для работы статистических методов над пользовательскими данными и персональным результатом для них."""

    async def get(self):
        """Запрос данных по пользователям (случайные 10)."""
        collection_user = await UserDocument().objects.find_all()
        # Перемешивание втупую и срез 10 пользователей.
        random.shuffle(collection_user)
        user_list = {str(document_user._id): document_user.get_user_name() for document_user in collection_user[:10]}

        raise system.utils.exceptions.Result(content={"userList": user_list})

    async def post(self):
        """Расчет статистики.

        В качестве параметров передавать список необходимых данных: двоих пользователей.

        * euclid - Евклидово расстояние.
        * pearson - Корреляця Пирсона.
        * jaccard - Коэффициент Жаккара.
        * manhattan - Манхэттенское расстояние.
        * matches - Ранжированный список критиков.
        * recommendations - Выработка рекомендации.

        """
        user1 = self.get_argument("user1")
        user2 = self.get_argument("user2")

        collection_user = await UserDocument().objects.limit(100).find_all()
        # Формирование массива данных для анализа - массив данных имеет вид [ид_пользователя => [ид_объекта => оценка,],... ]
        list_critic = {str(document_user._id): document_user.critic for document_user in collection_user}

        recommendations = Recommendations(list_critic)
        result = {
            "euclid": recommendations.euclid(recommendations.source[user1], recommendations.source[user2]),
            "pearson": recommendations.pearson(recommendations.source[user1], recommendations.source[user2]),
            "jaccard": recommendations.jaccard(recommendations.source[user1], recommendations.source[user2]),
            "manhattan": recommendations.manhattan(recommendations.source[user1], recommendations.source[user2]),
            "matches": recommendations.top_matches(user1, 2, recommendations.TYPE_SOURCE, recommendations.pearson),
            "recommendations": recommendations.get_recommendations(user1),
        }
        raise system.utils.exceptions.Result(content=result)


class StatisticForMovieHandler(BaseHandler):
    """Класс для работы статистических методов над пользовательскими данными и результатом для тех образцов, которые они оценили."""

    async def post(self):
        """Расчет статистики.

        В качестве параметров передавать список необходимых данных: пользователя и фильм.

        * pearson - Корреляця Пирсона.
        * matches - Ранжированный список критиков.
        * recommendations - Выработка рекомендации.

        """
        user = self.get_argument("user")
        movie = self.get_argument("movie")

        collection_user = await UserDocument().objects.limit(100).find_all()
        # Формирование массива данных для анализа - массив данных имеет вид [ид_пользователя => [ид_объекта => оценка,],... ]
        list_critic = {str(document_critic._id): document_critic.critic for document_critic in collection_user}

        recommendations = Recommendations(list_critic)
        result = {
            # Фильмы похожие на movie.
            "matches": recommendations.top_matches(movie, 3, recommendations.TYPE_TRANSFORMS, recommendations.pearson),
            # Кто еще не смотрел фильм movie.
            "recommendations": recommendations.get_recommendations_transforms(movie),
            # Похожие фильмы на movie.
            # "similarItems": recommendations.similar_items,
            # Выработка рекомендации по образцам.
            "pearson": recommendations.get_recommendations_items(user),
        }
        raise system.utils.exceptions.Result(content=result)


class UserCPNHandler(BaseHandler):
    """Класс отработки запросов для сети встречного распространения."""

    async def get(self):
        """Запрос персональной пользовательской информации которая связана с данными рекомендаций."""
        user = self.get_argument("user")

        collection_user = await UserDocument().objects.filter({"_id": ObjectId(user)}).find_all()
        if not collection_user:
            raise system.utils.exceptions.NotFound(error="Пользователь не найден")
        document_user = collection_user[-1]
        raise system.utils.exceptions.Result(content={"": document_user.get_user_name()})

    async def post(self):
        """Выработка персональных рекомендаций.

        Происходит в несколько этапов:
        1. Запрос необходмых для сети данных:
            - данные указанного пользователя;
            - данные звезды Гроссберга;
            - данные карт Кохонена;
        2. Запуск сети для одного пользователя.
        3. Исходя из работы сети, получим наиболее похожего пользователя.
        4. Извлечение результатов работы сети и их парсинг

        """
        user = self.get_argument("user")

        # Этап 1.
        collection_user = await UserItemExtractor().objects.filter({"_id": ObjectId(user)}).find_all()
        if not collection_user:
            raise system.utils.exceptions.NotFound(error="Пользователь не найден")
        document_user = collection_user[-1]
        """ :type: UserItemExtractor """

        collection_out_star = await GrossbergOutStarExtractor().objects.find_all()
        out_star = collection_out_star[-1]
        """ :type: GrossbergOutStarExtractor """

        collection_cluster = await KohonenClusterExtractor().objects.find_all()
        """ :type: list[KohonenClusterExtractor] """

        # Этап 2.
        net_kohonen = Kohonen(list_cluster=collection_cluster, cluster_class=KohonenClusterExtractor)
        net_grossberg = GrossbergOutStar(out_star=out_star, count_items=1)
        net_cpn = CPN(net_kohonen=net_kohonen, net_grossberg=net_grossberg)

        cluster_for_user = net_cpn.run_for_item(document_user)
        # Получаем ид кластера к которому лучше всего соответствует указанный пользователь.
        cluster_id_for_user = cluster_for_user.get_cluster_id()

        # Этап 3.
        # Выборка среди тех людей которые входят в тот же кластер.
        collection_user_in_cluster = await UserItemExtractor().objects.filter({UserItemExtractor.cluster.name:
                                                                                   cluster_id_for_user}).find_all()
        # Случайным образом выбираем одного из пользователей кластера (можно предложить на выбор друзей пользователя).
        random.shuffle(collection_user_in_cluster)
        document_other_user = collection_user_in_cluster[-1]
        """ :type: UserItemExtractor """

        # Отфильтруем в списке фильмов те, что не были просмотрены ни одним из двух людей.
        top250_filtered = set(top250).difference(document_other_user.get_item_vector().keys(), document_user.get_item_vector().keys())
        if len(top250_filtered) == 0:
            # Если суммарно оба человека смотрели увже все фильмы - предложим из тех что не смотрел только один из них.
            top250_filtered = set(top250).difference(document_user.get_item_vector().keys())

        # todo ref
        # Фильтрация вектора звезды.
        out_star_vector_filtered = {imdb: weight for (imdb, weight) in out_star.get_out_star_vector().items() if imdb in top250_filtered}
        # Сортировка по убыванию в отфильтрованном векторе звезды.
        sort_out_star_vector_filtered = dict(sorted(out_star_vector_filtered.items(), key=lambda x: x[1], reverse=True))
        # Тоже самое но с вектором кластера
        cluster_vector_filtered = {imdb: weight for (imdb, weight) in cluster_for_user.get_cluster_vector().items() if
                                   imdb in top250_filtered}
        sort_cluster_vector_filtered = dict(sorted(cluster_vector_filtered.items(), key=lambda x: x[1], reverse=True))
        # Для персональных рекомендаций из НС будем использовать восстановленный вектор оценок кластера
        # Для общего привлечения внимания к отдельным фильмам будем использовать данные звезды
        neuro_recommendations = Similarity.recovery_vector(sort_cluster_vector_filtered, document_user.get_item_vector())

        # Для статистического анализа подготовим данные
        data_cluster_user = {document_cluster_user.get_item_id(): document_cluster_user.get_item_vector() for document_cluster_user in
                             collection_user_in_cluster}
        # К данным для статистики добаляется новый пользователь кластера (или его данные актуализируются)
        data_cluster_user[document_user.get_item_id()] = document_user.get_item_vector()
        # После локализации выборки пользователей можно использовать статистические методы для выработки рекомендаций
        # Формируется класс стистики
        user_stat = Recommendations(data_cluster_user)
        # Выработка рекомендаций через статистику
        stat_recommendations = dict(user_stat.get_recommendations(document_user.get_item_id(), 250))

        # Сбор общей информации по кластерам
        count_users = await UserDocument().objects.count()
        pipeline = [
            {"$group": {"_id": "$cluster", "count": {"$sum": 1}}},
            {"$project": {"percentage": {"$multiply": ["$count", 100 / count_users]}}}
        ]
        aggregation_cluster_user = await UserDocument().objects.aggregate.raw(pipeline).fetch()
        result_aggregation = {info_cluster_user["_id"]: info_cluster_user["percentage"] for info_cluster_user in aggregation_cluster_user}

        # Вывод результатов
        result = {
            "cluster": cluster_id_for_user,
            "otherUser": document_other_user.get_item_name(),  # Более быстрая рекомендация с усредненными значениями
            "neuroRecommendations": neuro_recommendations,  # Более быстрая рекомендация с усредненными значениями
            "statRecommendations": stat_recommendations,  # Более точная в оценке рекомендация
            "outStarRecommendations": sort_out_star_vector_filtered,
            "infoClusters": result_aggregation,
        }
        raise system.utils.exceptions.Result(content=result)


class ResetCPNHandler(BaseHandler):
    """Специальный класс для выполнения административных действий с сетью встречного распространения."""

    async def post(self):
        """Запуск перестройки всей сети."""
        # Готовая звезда
        collection_out_star = await GrossbergOutStarExtractor().objects.find_all()
        if len(collection_out_star) > 0:
            out_star = collection_out_star[0]
        else:
            out_star = GrossbergOutStarExtractor()
            out_star.vector = {}
            out_star.learning = {}

        # Готовые кластеры
        collection_cluster = await KohonenClusterExtractor().objects.find_all()

        print("Kohonen")
        net_kohonen = Kohonen(
            list_cluster=collection_cluster,
            allowable_similarity=0.67,
            acceptable_similarity=0.95,
            cluster_class=KohonenClusterExtractor
        )

        # Образцы
        collection_user = await UserItemExtractor().objects.limit(1000).find_all()
        random.shuffle(collection_user)
        print("Kohonen learning 50")
        net_kohonen.learning(source=collection_user[:50])
        # net_kohonen.get_result_clustering()
        print("GrossbergOutStar")

        net_grossberg = GrossbergOutStar(
            out_star=out_star,
            components=top250,
            count_items=len(collection_user)
        )
        print("CPN")
        net_cpn = CPN(
            net_kohonen=net_kohonen,
            net_grossberg=net_grossberg
        )
        print("Запуск сети")
        net_cpn.run(source=collection_user)

        print("Сохранение результатов")
        # Очистка всей коллекции с кластерами.
        await KohonenClusterExtractor().objects.delete()
        # Сохранение тех документов которые образовались в процессе кластеризации.
        print("Сохранение кластеров")
        await KohonenClusterExtractor().objects.bulk_insert(net_kohonen.clusters)
        print("Сохранение звезды")
        await out_star.save()
        print("Сохранение пользователей")  # (у них изменилась принадлежность к кластеру)
        for document_user in collection_user:
            await UserItemExtractor().objects.filter({"_id": ObjectId(document_user._id)}).update(
                {UserItemExtractor.cluster.name: document_user.cluster})
        print("Завершено")
