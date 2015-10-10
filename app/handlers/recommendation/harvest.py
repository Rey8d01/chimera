from system.handler import BaseHandler
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
        # Начальный парсинг приходящих с ангулара через пост данных -
        # потому что это не параметры формы а request payload
        document_user = yield self.get_data_current_user()
        data_critic = self.escape.json_decode(self.request.body)
        imdb = data_critic[CriticDocument.imdb.name]
        rate = data_critic[CriticDocument.rate.name]

        if len(document_user.critic) == 0:
            # Создание новой записи в случае если вообще никаких данных небыло до этого (вдруг там не dict)
            document_user.critic = {imdb: int(rate)}
        else:
            # Измнение (создание) критики по имдб
            document_user.critic[imdb] = int(rate)

        yield document_user.save()

        self.result.update_content({
            CriticDocument.imdb.name: imdb,
            CriticDocument.rate.name: rate
        })
        self.write(self.result.get_message())