__author__ = 'rey'

import tornado.web
from tornado import gen

import system.handlers
from documents.catalog import CatalogDocument
from documents.post import PostDocument
from system.utils.exceptions import ChimeraHTTPError


class CatalogsHandler(system.handlers.MainHandler):

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        """

        :param alias:
        :return:
        """
        collection_catalog = yield CatalogDocument().objects.find_all()

        list_catalogs = []
        for document_catalog in collection_catalog:
            count_posts = yield PostDocument().objects.filter({"aliasCatalog": document_catalog.alias}).count()
            result = document_catalog.to_son()
            result["countPosts"] = count_posts
            list_catalogs.append(result)

        self.result.update_content({"catalogs": list_catalogs})
        self.write(self.result.get_message())

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        """

        :return:
        """
        pass