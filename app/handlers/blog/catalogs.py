from tornado.gen import coroutine

import system.handlers
from documents.blog.catalog import CatalogDocument
from documents.blog.post import PostDocument


class CatalogsHandler(system.handlers.BaseHandler):
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
            count_posts = yield PostDocument().objects.filter({PostDocument.aliasCatalog.name: document_catalog.alias}).count()
            result = document_catalog.to_son()
            result["countPosts"] = count_posts
            list_catalogs.append(result)

        self.result.update_content({"catalogs": list_catalogs})
        self.write(self.result.get_message())

    @coroutine
    def post(self):
        """
        Редактирование критериев отображения списка каталогов

        :return:
        """
        pass
