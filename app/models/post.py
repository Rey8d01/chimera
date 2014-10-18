__author__ = 'rey'

from system.base.model import BaseModel
import models.collection


class PostModel(BaseModel):

    def get_structure(self):
        return {
            'id': None,
            'slug': None,
            'slug_collection': None,
            'title': None,
            'tags': [
                {
                    'slug': None,
                    'title': None
                }
            ],
            'meta': {
                'date_create': None,
                'date_update': None,
                'author': None
            },
            'text': None,
        }

    def get_name_collection(self):
        return 'post'

    def references(self):
        return {
            'id_collection': models.collection.CollectionModel
        }