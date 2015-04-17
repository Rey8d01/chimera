__author__ = 'rey'

from tornado.web import asynchronous
from tornado.gen import coroutine

from system.handlers import BaseHandler
from documents.fake import UserItemExtractor
from documents.cpn import KohonenClusterExtractor, GrossbergOutStarExtractor
from system.components.recommendations.cpn import Kohonen, GrossbergOutStar, CPN, top250

from bson.objectid import ObjectId
import random


class FakeCPNHandler(BaseHandler):

    @asynchronous
    @coroutine
    def put(self):
        """
        Спец метод по запуску перестройке всей сети

        :return:
        """
        # Образцы
        collection_user = yield UserItemExtractor().objects.limit(10).find_all()
        random.shuffle(collection_user)

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
            cluster_class=KohonenClusterExtractor
        )

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
        print("Сохранение каждого кластера")
        [document_cluster.save() for document_cluster in collection_cluster]
        print("Сохранение звезды")
        yield out_star.save()
        print("Сохранение пользователей")  # (у них изменилась принадлежность к кластеру)
        print(dir(collection_user[0]))
        print(collection_user[0]._id)
        print(collection_user[0].info.name)
        t = yield collection_user[0].save()
        print(t)
        # [document_user.save() for document_user in collection_user]

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
        # collection_critic = UserItemExtractor()
        # collection_critic.fake_id="11111"
        #
        # t = yield collection_critic.save()
        # print(t)
        # return True

        # Запрошенный пользователь
        collection_critic = yield UserItemExtractor().objects.filter({"fake_id": "11111"}).find_all()

        # print(collection_critic[0]._id)
        # print(collection_critic[0].info.name)
        t = yield collection_critic[0].save()
        print(t)
        return True
        """ :type: UserItemExtractor"""
        # Готовая звезда
        collection_out_star = yield GrossbergOutStarExtractor().objects.find_all()
        out_star = collection_out_star[0]
        """ :type: GrossbergOutStarExtractor"""
        # Готовые кластеры
        collection_cluster = yield KohonenClusterExtractor().objects.find_all()

        net_kohonen = Kohonen(list_cluster=collection_cluster, cluster_class=KohonenClusterExtractor)
        net_grossberg = GrossbergOutStar(out_star=out_star, count_items=1)
        net_cpn = CPN(net_kohonen=net_kohonen, net_grossberg=net_grossberg)
        net_cpn.run(source=collection_critic)

        # net_kohonen.get_result_clustering()

        document_critic = collection_critic[0]
        print(document_critic)
        print(document_critic.cluster)
        self.result.update_content({"cluster": document_critic.cluster})
        self.write(self.result.get_message())
        # return True

    @asynchronous
    @coroutine
    def head(self):

        db = self.settings['db']
        print(db)
        # print(db.server_info())
        # print(db.host)
        # print(db.is_mongos)
        # print(db.is_primary)
        collection = db.fakeUser
        print(db.fakeUser)

        old_document = yield collection.find_one({"fake_id": "11111"})
        _id = old_document['_id']
        print(_id)
        result = yield collection.update({"fake_id": "11111"}, {'key': 'value'})
        # print('replaced', result['n'], 'document')
        new_document = yield collection.find_one({'_id': _id})
        print('document is now', new_document)

        return True