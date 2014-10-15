from system.base.handler import BaseHandler
from models.navigator import NavigatorModel
import tornado.web
from tornado import gen


class NavigatorHandler(BaseHandler):
    def get(self):

        # print(self.request.body_arguments)
        navigator = NavigatorModel()
        cursor = navigator.find().sort([('_id', -1)])
        while (yield cursor.fetch_next):
            message = cursor.next_object()
            self.write('<li>%s</li>' % message['msg'])

        # Iteration complete
        self.write('</ul>')
        self.finish()

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        navigator = NavigatorModel().load_post(self)
        result = yield navigator.save()
        self.write(result)