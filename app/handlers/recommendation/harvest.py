__author__ = 'rey'

from system.handlers import BaseHandler
from documents.critic import CriticDocument
from documents.user import UserDocument

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
        critic = document_user.critic if hasattr(document_user, "critic") else {}
        self.result.update_content({"critic": critic})
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

        # collection_critic = yield CriticDocument().objects.filter({
        #     # Фильтрация в motorengine по внешним полям идет через _id
        #     CriticDocument.user.name: document_user._id,
        #     CriticDocument.imdb.name: data_critic[CriticDocument.imdb.name],
        # }).find_all()

        imdb = data_critic[CriticDocument.imdb.name]
        rate = data_critic[CriticDocument.rate.name]

        if len(document_user.critic) == 0:
            document_user.critic = {imdb: int(rate)}
        else:
            # if data_critic[CriticDocument.imdb.name] in document_user.critic:
            document_user.critic[imdb] = int(rate)

        yield document_user.save()

        self.result.update_content({
            CriticDocument.imdb.name: imdb,
            CriticDocument.rate.name: rate
        })
        self.write(self.result.get_message())