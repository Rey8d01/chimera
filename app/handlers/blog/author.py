"""Обработчики информации по блогу связанную с пользователем.

Осуществляют вывод информации по пользователям.

"""
import re
import system.handler
import system.utils.exceptions
from bson.objectid import ObjectId
from documents.blog.post import PostDocument, PostMetaDocument
from system.utils.pagination import Pagination
from documents.user import UserDocument


class AuthorHandler(system.handler.BaseHandler):
    """Обработчик запросов для указанного каталога.

    GET - Запрос списка постов по заданному id автора.

    """

    async def get(self, user_id: str, current_page: int):
        """Запрос на получение информации по постам от определенного автора.

        :param user_id: id пользователя в базе;
        :param current_page: Номер страницы в списке постов;
        """
        current_page = int(current_page)

        # Запрос информации по пользователю.
        collection_users = await UserDocument().objects.filter({"_id": ObjectId(user_id)}).find_all()
        if not collection_users:
            raise system.utils.exceptions.NotFound(error_message="Пользователь не найден")
        document_user = collection_users[0]

        count_post = await PostDocument().objects.filter({PostDocument.meta.name + "." + PostMetaDocument.user.name: user_id}).count()
        pagination = Pagination(count_post, current_page, 5)

        collection_post = await PostDocument() \
            .objects \
            .filter({PostDocument.meta.name + "." + PostMetaDocument.user.name: user_id}) \
            .sort(PostDocument.meta.name + "." + PostMetaDocument.dateCreate.name, direction=-1) \
            .limit(pagination.count_items_on_page) \
            .skip(pagination.skip_items) \
            .find_all()

        list_items_post = []
        if collection_post:
            for document_post in collection_post:
                # Обрезание текста для превью.
                pattern = re.compile(r'<.*?>')
                clear_text = pattern.sub('', document_post.text)
                clipped_text = re.split('\s+', clear_text)[:10]

                document_post.text = " ".join(clipped_text)

                list_items_post.append(document_post.to_son())

        result = {
            "userName": document_user.get_user_name(),
            "userId": user_id,
            "posts": list_items_post,
            "pageData": {
                "currentPage": pagination.current_page,
                "pageSize": pagination.count_items_on_page,
                "total": pagination.count_all_items,
            }
        }

        raise system.utils.exceptions.Result(content=result)
