__author__ = 'rey'

import json

from system.handlers import BaseHandler


class MainerHandler(BaseHandler):
    def get(self):
        self.write(json.dumps({"hello": "world"}))
