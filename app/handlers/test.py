"""
Тестовый обработчик основных запросов.
"""

import json
from system.handlers import BaseHandler


class TestHandler(BaseHandler):

    def data_received(self, chunk):
        print("data_received")
        pass

    def get(self):
        print("get")
        self.write(json.dumps({"hello": "world"}))

    def head(self):
        print("head")
        self.write(json.dumps({"hello": "world"}))

    def post(self):
        print("post")
        self.write(json.dumps({"hello": "world"}))

    def delete(self):
        print("delete")
        self.write(json.dumps({"hello": "world"}))

    def patch(self):
        print("patch")
        self.write(json.dumps({"hello": "world"}))

    def put(self):
        print("put")
        self.write(json.dumps({"hello": "world"}))

    def options(self):
        print("options")
        self.write(json.dumps({"hello": "world"}))
