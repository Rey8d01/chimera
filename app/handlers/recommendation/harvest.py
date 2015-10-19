"""Обработка запросов для сохранения информации, которая в дальнейшем будет использоваться для анализа.

На данном этапе преполагается сохранение этой информации в рамках документа пользователя и только в рамках одного списка объектов оценок.

"""
import system.utils.exceptions
from tornado.gen import coroutine
from system.handler import BaseHandler
from documents.recommendation.critic import CriticDocument


class HarvestHandler(BaseHandler):
    """Сборщик информации для анализа.

    GET - список оценок уже проставленных пользователем.
    POST - изменение оценок пользователя.

    """

    @coroutine
    def get(self):
        """Вернет список данных критики по пользователяю."""
        # Тут проще воспользоваться функцией которая получает данные пользователей для системы.
        document_user = yield self.get_data_current_user()
        # У документа пользователя должно быть соответствующее свойство которое отвечает за сохранность информации с оценками
        critic = document_user.critic if hasattr(document_user, "critic") else {}
        raise system.utils.exceptions.Result(content={"critic": critic})

    @coroutine
    def post(self):
        """Сохранение данных критики."""
        document_user = yield self.get_data_current_user()
        # Начальный парсинг приходящих данных с ангулара через пост - потому что это не параметры формы а request payload.
        data_critic = self.escape.json_decode(self.request.body)
        imdb = data_critic[CriticDocument.imdb.name]
        rate = data_critic[CriticDocument.rate.name]

        if len(document_user.critic) == 0:
            # Создание новой записи в случае если вообще никаких данных небыло до этого (вдруг там не dict).
            document_user.critic = {imdb: int(rate)}
        else:
            # Измнение (создание) критики по имдб.
            document_user.critic[imdb] = int(rate)

        yield document_user.save()
        raise system.utils.exceptions.Result(content={CriticDocument.imdb.name: imdb, CriticDocument.rate.name: rate})
