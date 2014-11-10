__author__ = 'rey'

from system.base.handler import BaseHandler

import json


class MainHandler(BaseHandler):
    def get(self):
        self.write(json.dumps({"hello": "world"}))
