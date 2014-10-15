__author__ = 'rey'

from system.base.handler import BaseHandler
from models.collection import CollectionModel
import tornado.web
from tornado import gen
from system.utils.exceptions import ChimeraHTTPError

class CollectionHandler(BaseHandler):

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, id_collection):
        collection = CollectionModel()
        document_collection = yield collection.one({'slug': id_collection})
        if not document_collection:
            raise ChimeraHTTPError(404, error_message=u"Нихрена")
        collection.fill_by_data(document_collection)
        self.write(collection.get_json())

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        # Загрузка в
        collection = CollectionModel().load_post(self)
        result = yield collection.save()
        self.write(result)