__author__ = 'rey'

from system.handlers import BaseHandler
from documents.critic import CriticDocument

import tornado.web
from tornado import gen


class HarvestHandler(BaseHandler):

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        """
        Вернет список данных критики по пользователяю

        :return:
        """
        document_user = yield self.get_data_current_user()
        collection_critic = yield CriticDocument().objects.filter({
            # Фильтрация в motorengine по внешним полям идет через _id
            CriticDocument.user.name: document_user._id,
        }).find_all()

        list_critic = []
        if collection_critic:
            for document_critic in collection_critic:
                list_critic.append({
                    CriticDocument.imdb.name: document_critic.imdb,
                    CriticDocument.rate.name: document_critic.rate,
                    CriticDocument.year.name: document_critic.year,
                    CriticDocument.title.name: document_critic.title
                })

            self.result.update_content({"critics": list_critic})

        self.write(self.result.get_message())

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        """
        Сохранение данных критики

        :return:
        """
        document_user = yield self.get_data_current_user()
        data_critic = self.escape.json_decode(self.request.body)

        collection_critic = yield CriticDocument().objects.filter({
            # Фильтрация в motorengine по внешним полям идет через _id
            CriticDocument.user.name: document_user._id,
            CriticDocument.imdb.name: data_critic[CriticDocument.imdb.name],
        }).find_all()

        if len(collection_critic) == 0:
            document_critic = CriticDocument()
            document_critic.user = document_user
            document_critic.imdb = data_critic[CriticDocument.imdb.name]
        else:
            document_critic = collection_critic[0]

        document_critic.rate = int(data_critic[CriticDocument.rate.name])
        document_critic.year = int(data_critic[CriticDocument.year.name])
        document_critic.title = data_critic[CriticDocument.title.name]

        yield document_critic.save()

        self.result.update_content({
            CriticDocument.imdb.name: document_critic.imdb,
            CriticDocument.rate.name: document_critic.rate,
            CriticDocument.year.name: document_critic.year,
            CriticDocument.title.name: document_critic.title
        })
        self.write(self.result.get_message())