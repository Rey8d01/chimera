__author__ = 'rey'

from tornado.web import asynchronous
from tornado.gen import coroutine

from system.handlers import BaseHandler
from documents.fake import UserItemExtractor
from documents.cpn import KohonenClusterExtractor, GrossberOutStarExtractor
from system.components.recommendations.cpn import Kohonen, GrossbergOutStar, CPN, top250

from bson.objectid import ObjectId
import random


class FakeCPNHandler(BaseHandler):

    @asynchronous
    @coroutine
    def put(self):
        """
        Спец метод по запуску перестройки сети

        :return:
        """

        collection_out_star = yield GrossberOutStarExtractor().objects.find_all()
        if len(collection_out_star) > 0:
            out_star = collection_out_star[0]
        else:
            out_star = GrossberOutStarExtractor()
            out_star.vector = {}
            out_star.learning = {}

        # Готовые кластеры
        collection_cluster = yield KohonenClusterExtractor().objects.find_all()
        # Образцы
        collection_user = yield UserItemExtractor().objects.limit(1000).find_all()
        random.shuffle(collection_user)

        print("Kohonen")
        net_kohonen = Kohonen(
            list_cluster=collection_cluster,
            similarity=Kohonen.euclid,
            allowable_similarity=0.7,
            acceptable_similarity=0.9,
            # similarity=Kohonen.manhattan,
            # allowable_similarity=0.15,
            # acceptable_similarity=0.9,
            components=top250,
            cluster_class=KohonenClusterExtractor
        )
        print("Kohonen learning 50")
        net_kohonen.learning(source=collection_user[:50])
        # net_kohonen.learning(source=collection_user, clustering=False)
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

        [document_cluster.save() for document_cluster in collection_cluster]
        out_star.save()

    @asynchronous
    @coroutine
    def get(self):
        """
        Запрос данных по пользователям (случайные 10)
        :return:
        """
        collection_critic = yield UserItemExtractor().objects.find_all()

        # Перемешивание втупую и срез 10 пользователей
        random.shuffle(collection_critic)
        fake_user_list = {}
        for document_critic in collection_critic[:10]:
            fake_user_list[str(document_critic._id)] = document_critic.info.name

        self.result.update_content({"fakeUserList": fake_user_list})
        self.write(self.result.get_message())

    @asynchronous
    @coroutine
    def post(self):
        user = self.get_argument("user")
        collection_critic = yield UserItemExtractor().objects.filter({"_id": ObjectId(user)}).find_all()

        if len(collection_critic) == 0:
            pass
        document_critic = collection_critic[0]

        self.result.update_content({"user": user})
        self.write(self.result.get_message())
        # return True
