"""Обработка запросов пользователей по собственной информации."""
import system.handler
import system.utils.exceptions


class MeHandler(system.handler.MainHandler):
    """Обработчик запросов для авторизованного пользователя.

    GET - Запрос собственных данных из базы.

    """

    async def get(self):
        """Получение данных текущего пользователя, который представился системе."""
        document_user = self.current_user

        result = {
            "id": str(document_user._id)
        }

        raise system.utils.exceptions.Result(content=result)
