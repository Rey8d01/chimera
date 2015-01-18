__author__ = 'rey'

from system.handlers import BaseHandler
from documents.critic import CriticDocument

import tornado.web
from tornado import gen


class HarvestHandler(BaseHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        """
        Сохранение данных критики

        :return:
        """
        document_user = yield self.get_data_current_user()
        data_critic = self.escape.json_decode(self.request.body)

        document_critic = yield CriticDocument().objects.filter({
            CriticDocument.user.name: document_user,
            CriticDocument.imdb.name: data_critic[CriticDocument.imdb.name],
        }).find_all()

        if len(document_critic) == 0:
            document_critic = CriticDocument()
            document_critic.user = document_user
            document_critic.imdb = data_critic[CriticDocument.imdb.name]
        else:
            document_critic = document_critic[0]

        document_critic.rate = int(data_critic[CriticDocument.rate.name])
        document_critic.year = int(data_critic[CriticDocument.year.name])
        document_critic.title = data_critic[CriticDocument.title.name]


        print(document_critic)
        # yield document_critic.save()


        # self.result.update_content({
        #     CriticDocument.imdb.name: data_critic.imdb,
        #     CriticDocument.rate.name: data_critic.rate,
        #     CriticDocument.year.name: data_critic.year,
        #     CriticDocument.title.name: data_critic.title
        # })
        # self.write(self.result.get_message())