__author__ = 'rey'

from system.base.model import BaseModel
import models.collection


class PostModel(BaseModel):

    def get_structure(self):
        return {
            'title': None,
            'id_collection': None,
            'text': None,
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
        }

    def get_name_collection(self):
        return 'post'

    def references(self):
        return {
            'id_collection': models.collection.CollectionModel
        }