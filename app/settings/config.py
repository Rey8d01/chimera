__author__ = 'rey'

import os.path
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

# config for tornado
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "template/static"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "xsrf_cookies": True,
}

# config for my app
config = {
    "db" : {
        "host" : "qaz",
        "user" : "qaz",
        "pass" : "qaz"
    }
}