from system.base.handler import BaseHandler
from models.navigator import NavigatorModel
import tornado.web
from tornado import gen
from system.utils.exceptions import ChimeraHTTPError


class NavigatorHandler(BaseHandler):

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        """

        :return:
        """
        navigator = NavigatorModel()
        documents_navigator = navigator.find().sort([('_id', -1)])

        if not documents_navigator:
            raise ChimeraHTTPError(404, error_message=u"Навигационные элементы отсутствуют")

        list_items_navigator = []
        while (yield documents_navigator.fetch_next):
            document_navigator = documents_navigator.next_object()
            navigator.fill_by_data(document_navigator)
            list_items_navigator.append(navigator.get_data())
        self.result.update_content({"navigator": list_items_navigator})

        self.write(self.result.get_message())

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        """

        :return:
        """
        navigator = NavigatorModel().load_post(self)
        result = yield navigator.save()
        self.write(result)