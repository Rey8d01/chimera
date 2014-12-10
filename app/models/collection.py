__author__ = 'rey'

from system.base.model import BaseModel


class CollectionModel(BaseModel):

    def get_structure(self):
        return {
            'title': None,
            'alias': None
        }

    def get_name_collection(self):
        return 'collection'