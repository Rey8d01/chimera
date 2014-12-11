__author__ = 'rey'

from system.model import BaseModel


class UserModel(BaseModel):
    def get_structure(self):
        return {
            "info": None,
            "oauth": [
                {
                    "type": None,  # twitter
                    "id": None,  # 1234
                    "name": None,  # John Doe
                    "firstName": None,  # John
                    "lastName": None,  # Doe
                    "alias": None,  # john87
                    "email": None,  # john@doe.com
                    "dateBirth": {
                        "day": None,  # 27
                        "month": None,  # 11
                        "year": None,  # 1987
                    },
                    "raw": None
                }
            ],
            "meta": {
                "dateRegistration": None,
                "dateLastActivity": None,
            },
        }

    def get_name_collection(self):
        return 'user'

    def references(self):
        return {}
