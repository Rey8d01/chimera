"""Обработка запросов для сохранения информации, которая в дальнейшем будет использоваться для анализа.

На данном этапе предполагается сохранение этой информации в рамках документа пользователя и только в рамках одного списка объектов оценок.
В качестве источника данных используется вложенный документ пользователя - критик.
Состоит из набора информации связи объект критики (фильм) - субъект (пользователь) - оценка, а так же служебной информации.

"""
import random
import system.utils.exceptions
from system.handler import BaseHandler
from documents.user import UserDocument


class ListRatedItemsHandler(BaseHandler):
    """Список сохраненной пользовательской информации для анализа.

    GET - список оценок уже проставленных пользователем.

    """

    async def get(self, count: int=5):
        """Вернет список данных критики по текущему авторизованному пользователю.

        У документа пользователя должно быть соответствующее свойство которое отвечает за сохранность информации с оценками.

        :param count:
        """
        count = int(count)
        document_user = await self.get_data_current_user()
        # Выборка указанного количества фильмов (по последним).
        result = []
        if document_user.critic is not None:
            result = dict(list(document_user.critic.items())[-count:])

        raise system.utils.exceptions.Result(content=result)


class ListRatedUsersHandler(BaseHandler):
    """Список пользователей с оценками (для списков с которыми можно осуществлять сравнение).

    GET - вернет список пользователей.

    """

    async def get(self):
        """Запрос данных по пользователям (случайные 10)."""
        collection_user = await UserDocument().objects.find_all()
        # Перемешивание втупую и срез 10 пользователей.
        random.shuffle(collection_user)
        user_list = {str(document_user._id): document_user.get_user_name() for document_user in collection_user[:10]}

        raise system.utils.exceptions.Result(content={"userList": user_list})


class HarvestHandler(BaseHandler):
    """Сборщик информации для анализа.

    POST - изменение оценок пользователя.

    """

    async def post(self):
        """Сохранение данных критики."""
        imdb = self.get_bytes_body_argument("imdb")
        rate = int(self.get_bytes_body_argument("rate"))
        document_user = await self.get_data_current_user()
        if document_user.critic is None:
            # Создание новой записи в случае если вообще никаких данных не было до этого (вдруг там не dict).
            document_user.critic = {imdb: int(rate)}
        else:
            # Изменение (создание) критики по имдб.
            document_user.critic[imdb] = int(rate)

        await document_user.save()
        raise system.utils.exceptions.Result(content={"imdb": imdb, "rate": rate})
