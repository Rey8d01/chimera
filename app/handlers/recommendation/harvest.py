"""Обработка запросов для сохранения информации, которая в дальнейшем будет использоваться для анализа.

На данном этапе преполагается сохранение этой информации в рамках документа пользователя и только в рамках одного списка объектов оценок.
В качестве источника данных используется вложенный документ пользователя - критик.
Состоит из набора информации связи объект критики (фильм) - субъект (пользователь) - оценка, а так же служебной информации.

"""
import system.utils.exceptions
from system.handler import BaseHandler


class HarvestHandler(BaseHandler):
    """Сборщик информации для анализа.

    GET - список оценок уже проставленных пользователем.
    POST - изменение оценок пользователя.

    """

    async def get(self):
        """Вернет список данных критики по пользователяю."""
        # Тут проще воспользоваться функцией которая получает данные пользователей для системы.
        document_user = await self.get_data_current_user()
        """ :type: documents.user.UserDocument """
        # У документа пользователя должно быть соответствующее свойство которое отвечает за сохранность информации с оценками.
        raise system.utils.exceptions.Result(content={document_user.critic.name: document_user.critic})

    async def post(self):
        """Сохранение данных критики."""
        document_user = await self.get_data_current_user()
        """ :type: documents.user.UserDocument """
        # Начальный парсинг приходящих данных с ангулара через пост - потому что это не параметры формы а request payload.
        data_critic = self.escape.json_decode(self.request.body)
        imdb = data_critic["imdb"]
        rate = data_critic["rate"]

        if len(document_user.critic) == 0:
            # Создание новой записи в случае если вообще никаких данных небыло до этого (вдруг там не dict).
            document_user.critic = {imdb: int(rate)}
        else:
            # Измнение (создание) критики по имдб.
            document_user.critic[imdb] = int(rate)

        await document_user.save()
        raise system.utils.exceptions.Result(content={"imdb": imdb, "rate": rate})
