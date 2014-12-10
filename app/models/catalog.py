__author__ = 'rey'

from system.model import BaseModel


class CatalogModel(BaseModel):

    def get_structure(self):
        return {
            'title': None,
            'alias': None
        }

    def get_name_collection(self):
        return 'catalog'