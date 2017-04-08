"""Обработка запросов пользователей по собственной информации."""
import utils.exceptions
import utils.handler


class MeHandler(utils.handler.MainHandler):
    """Обработчик запросов для авторизованного пользователя.

    GET - Запрос собственных данных из базы.

    """

    async def get(self):
        """Получение данных текущего пользователя, который представился системе."""
        document_user = self.current_user

        result = {
            "id": str(document_user._id)
        }

        raise utils.exceptions.Result(content=result)
