__author__ = 'rey'

from tornado.gen import coroutine

from system.handlers import BaseHandler
from documents.fake import UserItemExtractor, UserDocument
from documents.cpn import KohonenClusterExtractor, GrossbergOutStarExtractor
from system.components.recommendations.cpn import Kohonen, GrossbergOutStar, CPN, top250

from bson.objectid import ObjectId
import random
from system.components.recommendations.statistic import Recommendations, Similarity


class FakeCPNHandler(BaseHandler):

    @coroutine
    def put(self):
        """
        Спец метод по запуску перестройке всей сети

        :return:
        """
        # Готовая звезда
        collection_out_star = yield GrossbergOutStarExtractor().objects.find_all()
        if len(collection_out_star) > 0:
            out_star = collection_out_star[0]
        else:
            out_star = GrossbergOutStarExtractor()
            out_star.vector = {}
            out_star.learning = {}

        # Готовые кластеры
        collection_cluster = yield KohonenClusterExtractor().objects.find_all()

        print("Kohonen")
        net_kohonen = Kohonen(
            list_cluster=collection_cluster,
            allowable_similarity=0.67,
            acceptable_similarity=0.95,
            cluster_class=KohonenClusterExtractor
        )

        # Образцы
        collection_user = yield UserItemExtractor().objects.limit(1000).find_all()
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
        # Очистка всей коллекции с кластерами
        yield KohonenClusterExtractor().objects.delete()
        # И сохранение тех документов которые образовались в процессе кластеризации
        print("Сохранение кластеров")
        yield KohonenClusterExtractor().objects.bulk_insert(net_kohonen.clusters)
        print("Сохранение звезды")
        yield out_star.save()
        print("Сохранение пользователей")  # (у них изменилась принадлежность к кластеру)
        for document_user in collection_user:
            yield UserItemExtractor().objects.filter({"_id": ObjectId(document_user._id)}).update({UserItemExtractor.cluster.name: document_user.cluster})
        print("Завершено")

    @coroutine
    def get(self):
        """
        :return:
        """
        user = self.get_argument("user", None)

        if user:
            """ Запрос информации по конкретному пользователю """
            collection_user = yield UserDocument().objects.filter({"_id": ObjectId(user)}).find_all()
            document_user = collection_user[0]
            """ :type: UserItemExtractor """
            self.result.update_content({"": document_user.get_item_name()})
        else:
            """ Запрос данных по пользователям (случайные 10) """
            collection_critic = yield UserDocument().objects.find_all()

            # Перемешивание втупую и срез 10 пользователей
            random.shuffle(collection_critic)
            fake_user_list = {}
            for document_critic in collection_critic[:10]:
                fake_user_list[str(document_critic._id)] = document_critic.info.name

            self.result.update_content({"fakeUserList": fake_user_list})

        self.write(self.result.get_message())

    @coroutine
    def post(self):
        """
        Выработка персональных рекомендаций

        :return:
        """
        user = self.get_argument("user")
        # Запрошенный пользователь
        collection_user = yield UserItemExtractor().objects.filter({"_id": ObjectId(user)}).find_all()
        document_user = collection_user[0]
        """ :type: UserItemExtractor """

        # Готовая звезда
        collection_out_star = yield GrossbergOutStarExtractor().objects.find_all()
        out_star = collection_out_star[0]
        """ :type: GrossbergOutStarExtractor """
        # Готовые кластеры
        collection_cluster = yield KohonenClusterExtractor().objects.find_all()

        # Запуск сети для одного пользователя
        net_kohonen = Kohonen(list_cluster=collection_cluster, cluster_class=KohonenClusterExtractor)
        net_grossberg = GrossbergOutStar(out_star=out_star, count_items=1)
        net_cpn = CPN(net_kohonen=net_kohonen, net_grossberg=net_grossberg)
        cluster_for_user = net_cpn.run_for_item(document_user)
        cluster_id_for_user = cluster_for_user.get_cluster_id()

        # Выборка среди тех людей которые входят в тот же кластер
        collection_user_in_cluster = yield UserItemExtractor().objects.filter({UserItemExtractor.cluster.name:
                                                                              cluster_id_for_user}).find_all()

        # Случайным образом выбираем одно из пользователей кластера (можно предложить на выбор друзей пользователя)
        random.shuffle(collection_user_in_cluster)
        document_other_user = collection_user_in_cluster[0]
        """ :type: UserItemExtractor """
        # Отфильтруем из списка фильмов те что не были просмотрены ни одним из двух людей
        top250_filtered = set(top250).difference(document_other_user.get_item_vector().keys(), document_user.get_item_vector().keys())
        if len(top250_filtered) == 0:
            # Если суммарно оба человека смотрели увже все фильмы - предложим из тех что не смотрел только один из них
            top250_filtered = set(top250).difference(document_user.get_item_vector().keys())

        # if len(top250_filtered) > 0:
        # Фильтрация вектора звезды
        out_star_vector_filtered = {imdb: weight for (imdb, weight) in out_star.get_out_star_vector().items() if imdb in top250_filtered}
        # Сортировка по убыванию в отфильтрованном векторе звезды
        sort_out_star_vector_filtered = dict(sorted(out_star_vector_filtered.items(), key=lambda x: x[1], reverse=True))
        # Тоже самое но с вектором кластера
        cluster_vector_filtered = {imdb: weight for (imdb, weight) in cluster_for_user.get_cluster_vector().items() if imdb in top250_filtered}
        sort_cluster_vector_filtered = dict(sorted(cluster_vector_filtered.items(), key=lambda x: x[1], reverse=True))
        # Для персональных рекомендаций из НС будем использовать восстановленный вектор оценок кластера
        # Для общего привлечения внимания к отдельным фильмам будем использовать данные звезды
        neuro_recommendations = Similarity.recovery_vector(sort_cluster_vector_filtered, document_user.get_item_vector())

        # Для статистического анализа подготовим данные
        data_cluster_user = {}
        for document_cluster_user in collection_user_in_cluster:
            data_cluster_user[document_cluster_user.get_item_id()] = document_cluster_user.get_item_vector()
        # К данным для статистики добаляется новый пользователь кластера (или его данные актуализируются)
        data_cluster_user[document_user.get_item_id()] = document_user.get_item_vector()
        # После локализации выборки пользователей можно использовать статистические методы для выработки рекомендаций
        # Формируется класс стистики
        user_stat = Recommendations(data_cluster_user)
        # Выработка рекомендаций через статистику
        stat_recommendations = dict(user_stat.get_recommendations(document_user.get_item_id(), 250))

        # Сбор общей информации по кластерам
        count_users = yield UserDocument().objects.count()
        pipeline = [
            {"$group": {"_id": "$cluster", "count": {"$sum": 1}}},
            {"$project": {"percentage": {"$multiply": ["$count", 100 / count_users]}}}
        ]
        aggregation_cluster_user = yield UserDocument().objects.aggregate.raw(pipeline).fetch()
        result_aggregation = {info_cluster_user["_id"]: info_cluster_user["percentage"] for info_cluster_user in aggregation_cluster_user}

        # Вывод результатов
        self.result.update_content({
            "cluster": cluster_id_for_user,
            "otherUser": document_other_user.get_item_name(),  # Более быстрая рекомендация с усредненными значениями
            "neuroRecommendations": neuro_recommendations,  # Более быстрая рекомендация с усредненными значениями
            "statRecommendations": stat_recommendations,  # Более точная в оценке рекомендация
            "outStarRecommendations": sort_out_star_vector_filtered,
            "infoClusters": result_aggregation,
        })
        self.write(self.result.get_message())
