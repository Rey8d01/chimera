"""Укомплектованный набор классов для работы различных конфигураций сети встречного распространения и статистики.

StatisticForUserHandler реализует подсчет статистики для пользователя.
StatisticForMovieHandler реализует подсчет статистики по данным оценкам к фильму.
UserCPNHandler работа сети встречного распространения на основе пользовательских данных и по пресональным данным одного пользователя.
UtilsCPNHandler утилитарный класс для обслуживания сети.

user_x = "5501eec480a9e10c639d60e0"
user_y = "5501eec480a9e10c639d60e4"
movie = "tt0407887"

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


class MetricsHandler(BaseHandler):
    """Класс для получения результатов вычисления различных метрик расстояний между пользователями."""

    async def get(self, user_x: str, user_y: str):
        """Вернет результат вычислений метрик по двум пользователям.

        * euclid - Евклидово расстояние.
        * pearson - Корреляция Пирсона.

        :param user_x:
        :param user_y:
        :return:
        """
        collection_user = await UserDocument().objects.filter({"_id": ObjectId(user_x)}).find_all()
        document_user_x = collection_user[-1]
        critic_x = document_user_x.critic

        collection_user = await UserDocument().objects.filter({"_id": ObjectId(user_y)}).find_all()
        document_user_y = collection_user[-1]
        critic_y = document_user_y.critic

        result = {
            "euclid": Similarity.euclid(critic_x, critic_y),
            "pearson": Similarity.pearson(critic_x, critic_y),
        }

        raise system.utils.exceptions.Result(content=result)


class StatisticForUserHandler(BaseHandler):
    """Класс для работы статистических методов над пользовательскими данными и персональным результатом для них."""

    async def get(self, user_x: str, user_y: str):
        """Коллаборативная фильтрация по схожести пользователей.

        Долгий расчет поскольку каждый раз выбирается вся база пользователей и их оценки.

        * matches - Ранжированный список критиков.
        * recommendations - Выработка рекомендации.

        :param user_x: id первого пользователя;
        :param user_y: id второго пользователя;
        """
        collection_user = await UserDocument().objects.limit(60).find_all()
        list_critic = UserDocument.get_list_critic(collection_user)

        result = {
            "matches": Recommendations.top_matches(source=list_critic, person=user_x, n=2, get_similarity=Similarity.pearson),
            "recommendations": Recommendations.get_recommendations_by_person_for_person(source=list_critic, person=user_x),
        }

        raise system.utils.exceptions.Result(content=result)


class StatisticForItemsHandler(BaseHandler):
    """Класс для работы статистических методов над пользовательскими данными и результатом для тех образцов, которые они оценили."""

    async def get(self, user: str, item: str):
        """Коллаборативная фильтрация по схожести образцов.

        * matches - Ранжированный список критиков.
        * recommendations - Выработка рекомендации.

        :param user: id пользователя;
        :param item: id образца;
        """
        source_similar_items = await self.redis.get("recommendation_source_similar_items")

        print(source_similar_items)
        return 1
        # self.escape.json_decode(self.escape.to_unicode(tags))

        result = {
            # "matches": Recommendations.top_matches(source=list_items, person=item, n=3, get_similarity=Similarity.pearson),
            "recommendations": Recommendations.get_recommendations_by_items_for_person(person=user,
                                                                                       source_similar_items=source_similar_items),
            # "recommendations_item": Recommendations.get_recommendations_by_items_for_item(transformed_source=list_items, item=item),
        }
        raise system.utils.exceptions.Result(content=result)


class UtilsStatisticHandler(BaseHandler):
    """Класс вызова утилитарных функций для коррекции статистических данных."""

    async def put(self):
        """Обновление (пересчет) массива данных для фильтрации по схожести образцов."""
        collection_user = await UserDocument().objects.find_all()
        list_critic = UserDocument.get_list_critic(collection_user)
        source_similar_items = Recommendations.calculate_source_similar_items(source=list_critic)

        await self.redis.set("recommendation_source_similar_items", source_similar_items)

        raise system.utils.exceptions.Result(content={"result": True})


class UserCPNHandler(BaseHandler):
    """Класс отработки запросов для сети встречного распространения."""

    async def get(self):
        """Запрос персональной пользовательской информации которая связана с данными рекомендаций."""
        user = self.get_argument("user")

        collection_user = await UserDocument().objects.filter({"_id": ObjectId(user)}).find_all()
        if not collection_user:
            raise system.utils.exceptions.NotFound(error_message="Пользователь не найден")
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
        После того как сеть отработала и вернула результат (наиболее подходящую группу единомышлеников), им можно вертеть
        как угодно.
        3. Исходя из работы сети, получим наиболее похожего пользователя.
        На совместных взгялдах похожего пользователя с запрошенным пользователем выявим список непросмотренных фильмов,
         для того чтобы по ограниченной выборке фильмов определить их предполагаемые оценки и отранжировать рекоммендации.
        4. Извлечение результатов работы сети и их парсинг.
        5. Для совокупности примешаем данные результатов статистики.
        6. Запрос агрегации по кластерам и вывод результатов.

        """
        user = self.get_argument("user")

        # Этап 1.
        collection_user = await UserItemExtractor().objects.filter({"_id": ObjectId(user)}).find_all()
        if not collection_user:
            raise system.utils.exceptions.NotFound(error_message="Пользователь не найден")
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
        # Выборка одного человека среди тех людей, которые входят в тот же кластер.
        collection_user_in_cluster = await UserItemExtractor().objects.filter({UserItemExtractor.cluster.name:
                                                                                   cluster_id_for_user}).find_all()
        # Случайным образом выбираем одного из пользователей кластера (можно предложить на выбор друзей пользователя).
        random.shuffle(collection_user_in_cluster)
        document_other_user = collection_user_in_cluster[-1]
        """ :type: UserItemExtractor """

        # Отфильтруем в списке фильмов те, что не были просмотрены ни одним из двух людей.
        top250_filtered = set(top250).difference(document_other_user.get_item_vector().keys(), document_user.get_item_vector().keys())
        if len(top250_filtered) == 0:
            # Если суммарно оба человека смотрели увже все фильмы - предложим из тех что не смотрел только пользователь.
            top250_filtered = set(top250).difference(document_user.get_item_vector().keys())
        # В дальнейшем этот отфильтрованный список фильмов будем использовать для фильтрации результатов работы сети,
        # поскольку все оценки подряд нам получать не интересно.

        # Этап 4.
        # Фильтрация вектора звезды и сортировка по убыванию.
        out_star_vector_filtered = {imdb: weight for (imdb, weight) in out_star.get_out_star_vector().items() if imdb in top250_filtered}
        sort_out_star_vector_filtered = dict(sorted(out_star_vector_filtered.items(), key=lambda x: x[1], reverse=True))
        # Аналогично поступаем с вектором кластера.
        cluster_vector_filtered = {imdb: weight for (imdb, weight) in cluster_for_user.get_cluster_vector().items() if
                                   imdb in top250_filtered}
        sort_cluster_vector_filtered = dict(sorted(cluster_vector_filtered.items(), key=lambda x: x[1], reverse=True))
        # Для персональных рекомендаций из НС будем использовать восстановленный вектор оценок кластера.
        # Для общего привлечения внимания к отдельным фильмам будем использовать данные звезды.
        neuro_recommendations = Similarity.recovery_vector(sort_cluster_vector_filtered, document_user.get_item_vector())

        # Этап 5.
        # Для статистического анализа подготовим данные.
        data_cluster_user = {document_cluster_user.get_item_id(): document_cluster_user.get_item_vector() for document_cluster_user in
                             collection_user_in_cluster}
        # К данным для статистики добаляется новый пользователь кластера (или его данные актуализируются).
        data_cluster_user[document_user.get_item_id()] = document_user.get_item_vector()
        # После локализации выборки пользователей можно использовать статистические методы для выработки рекомендаций.
        user_stat = Recommendations(data_cluster_user)
        # Выработка рекомендаций через статистику.
        stat_recommendations = dict(user_stat.get_recommendations_by_person_for_person(document_user.get_item_id(), 250))

        # Этап 6.
        # Сбор общей информации по кластерам.
        count_users = await UserDocument().objects.count()
        pipeline = [
            {"$group": {"_id": "$cluster", "count": {"$sum": 1}}},
            {"$project": {"percentage": {"$multiply": ["$count", 100 / count_users]}}}
        ]
        aggregation_cluster_user = await UserDocument().objects.aggregate.raw(pipeline).fetch()
        result_aggregation = {info_cluster_user["_id"]: info_cluster_user["percentage"] for info_cluster_user in aggregation_cluster_user}

        result = {
            "cluster": cluster_id_for_user,
            "otherUser": document_other_user.get_item_name(),
            "neuroRecommendations": neuro_recommendations,
            "statRecommendations": stat_recommendations,
            "outStarRecommendations": sort_out_star_vector_filtered,
            "infoClusters": result_aggregation,
        }
        raise system.utils.exceptions.Result(content=result)


class UtilsCPNHandler(BaseHandler):
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
