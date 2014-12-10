__author__ = 'rey'

from system.base.model import BaseModel
import re


class PostModel(BaseModel):

    def get_structure(self):
        return {
            'id': None,
            'alias': None,
            'aliasCollection': None,
            'title': None,
            'tags': [
                {
                    'alias': None,
                    'title': None
                }
            ],
            'meta': {
                'dateCreate': None,
                'dateUpdate': None,
                'author': None
            },
            'text': None,
        }

    def get_name_collection(self):
        return 'post'

    def references(self):
        return {}
