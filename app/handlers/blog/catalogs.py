
import system.handler
import system.utils.exceptions
from tornado.gen import coroutine
from documents.blog.catalog import CatalogDocument
from documents.blog.post import PostDocument


class CatalogsHandler(system.handler.MainHandler):
    @coroutine
    def get(self):
        """
        Список категорий

        :param alias:
        :return:
        """
        collection_catalog = yield CatalogDocument().objects.find_all()

        list_catalogs = []
        for document_catalog in collection_catalog:
            count_posts = yield PostDocument().objects.filter({PostDocument.catalogAlias.name: document_catalog.alias}).count()
            result = document_catalog.to_son()
            result["countPosts"] = count_posts
            list_catalogs.append(result)

        raise system.utils.exceptions.Result(content={"catalogs": list_catalogs})

    @coroutine
    def post(self):
        """
        Редактирование критериев отображения списка каталогов

        :return:
        """
        pass
