__author__ = 'rey'

from system.base.model import BaseModel


class NavigatorModel(BaseModel):

    def get_structure(self):
        return {
            'title': None,
            'url': None
        }

    def get_name_collection(self):
        return 'navigator'
