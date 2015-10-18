import random

from tornado.gen import coroutine

from system.handler import BaseHandler
from documents.fake import UserDocument
from system.components.recommendations.statistic import Recommendations


class FakeHandler(BaseHandler):

    @coroutine
    def get(self):
        """
        Запрос данных по пользователям (случайные 10)
        :return:
        """
        collection_critic = yield UserDocument().objects.find_all()

        # Перемешивание втупую и срез 10 пользователей
        random.shuffle(collection_critic)
        fake_user_list = {}
        for document_critic in collection_critic[:10]:
            fake_user_list[str(document_critic._id)] = document_critic.info.name

        self.result.update_content({"fakeUserList": fake_user_list})
        self.write(self.result.get_message())

    @coroutine
    def put(self):
        from system.components.recommendations.cpn import Kohonen, ItemExtractor, top250
        from documents.recommendation.cpn import KohonenClusterExtractor

        class UserItemExtractor(UserDocument, ItemExtractor):
            """
            Внутренний класс для определения ключевых позиций необходимых для кластеризации
            """
            __collection__ = UserDocument.__collection__

            def get_item_id(self):
                return self._id

            def get_item_name(self):
                return self.info.name

            def get_item_vector(self):
                return self.critic.copy()

        # Готовые кластеры
        collection_cluster = yield KohonenClusterExtractor().objects.find_all()
        # Образцы
        list_user = yield UserItemExtractor().objects.limit(10).find_all()
        random.shuffle(list_user)

        net = Kohonen(
            list_cluster=[],
            similarity=Kohonen.euclid,
            allowable_similarity=0.7,
            acceptable_similarity=0.9,
            # similarity=Kohonen.manhattan,
            # allowable_similarity=0.15,
            # acceptable_similarity=0.9,
            components=top250,
            cluster_class=KohonenClusterExtractor
        )
        net.learning(source=list_user[:50])
        net.get_result_clustering()
        net.save()


    @coroutine
    def post(self):
        """
        Расчет статистики

        В качестве параметров передавать список необходимых данных: двоих пользователей или фильм
        Возвращать данные расщитанные данные
        :return:
        """
        # 5501eec480a9e10c639d60e0 5501eec480a9e10c639d60e4
        user1 = self.get_argument("user1", "")
        user2 = self.get_argument("user2", "")
        movie = self.get_argument("movie", "")

        # todo
        user1 = "5501eec480a9e10c639d60e0"
        user2 = "5501eec480a9e10c639d60e4"
        movie = "tt0407887"
        # todo
        collection_critic = yield UserDocument().objects.limit(100).find_all()

        # Формирование массива данных для анализа
        list_critic = {}
        for document_critic in collection_critic:
            # Массив данных имеет вид [ид пользователя => [ид объекта => оценка,] ]
            list_critic[str(document_critic._id)] = document_critic.critic
        # print(list_critic)

        # Recommendations
        instance_recommendations = Recommendations(list_critic)

        if movie != "":
            # Для проверки объектов
            self.result.update_content({
                # Фильмы похожие на
                "matches": instance_recommendations.top_matches(movie, 3, instance_recommendations.TYPE_TRANSFORMS,
                                                                instance_recommendations.pearson),
                # Кто еще не смотрел фильм
                "recommendations": instance_recommendations.get_recommendations_transforms(movie),
                # Похожие фильмы
                #"similarItems": instance_recommendations.similar_items,
                # Выработка рекомендации по образцам
                "pearson": instance_recommendations.get_recommendations_items(user1),
            })
        elif (user1 != "") and (user2 != ""):
            # Для сравнения пользователей
            self.result.update_content({
                # Евклидово расстояние
                "euclid": instance_recommendations.euclid(instance_recommendations.source[user1],
                                                          instance_recommendations.source[user2]),
                # Корреляця Пирсона
                "pearson": instance_recommendations.pearson(instance_recommendations.source[user1],
                                                            instance_recommendations.source[user2]),
                # Коэффициент Жаккара
                "jaccard": instance_recommendations.jaccard(instance_recommendations.source[user1],
                                                            instance_recommendations.source[user2]),
                # Манхэттенское расстояние
                "manhattan": instance_recommendations.manhattan(instance_recommendations.source[user1],
                                                                instance_recommendations.source[user2]),
                # Ранжирование критиков
                "matches": instance_recommendations.top_matches(user1, 2, instance_recommendations.TYPE_SOURCE,
                                                                instance_recommendations.pearson),
                # Выработка рекомендации
                "recommendations": instance_recommendations.get_recommendations(user1),
            })
        else:
            # self.result.update_content({})
            pass

        self.write(self.result.get_message())

        # print(
        #     'Люди:', user1, 'и', user2, '\n',
        #     'Евклидово расстояние		', instance_recommendations.euclid(instance_recommendations.source, user1, user2), '\n',
        #     'Корреляця Пирсона			', instance_recommendations.pearson(instance_recommendations.source, user1, user2), '\n',
        #     'Коэффициент Жаккара		', instance_recommendations.jaccard(instance_recommendations.source, user1, user2), '\n',
        #     'Манхэттенское расстояние	', instance_recommendations.manhattan(instance_recommendations.source, user1, user2), '\n',
        #     '\n',
        #     'Ранжирование критиков		', instance_recommendations.top_matches(user1, 2, instance_recommendations.TYPE_SOURCE, instance_recommendations.pearson), '\n',
        #     'Выработка рекомендации		', instance_recommendations.get_recommendations(user1), '\n',
        #     '\n',
        #     'Фильмы похожие на 			', movie, instance_recommendations.top_matches(movie, 3, instance_recommendations.TYPE_TRANSFORMS, instance_recommendations.pearson), '\n',
        #     'Кто еще не смотрел фильм	', movie, instance_recommendations.get_recommendations_transforms(movie), '\n',
        #     # 'AAAAAAAAAA	', instance_recommendations.transforms, '\n',
        #     # '\n',
        #     # 'Похожие фильмы	\n			', instance_recommendations.similar_items, '\n',
        #     # 'Выработка рекомендации по образцам', instance_recommendations.get_recommendations_items(user1), '\n',
        # )