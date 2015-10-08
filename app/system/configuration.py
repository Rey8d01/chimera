"""
Файл конфигурации системы.
Содержит настройки подключения к внешним ресурсам, роутинг и настройки работы системы.
"""

from tornado.options import define

import system.handlers

import handlers.test
import handlers.blog.catalogs
import handlers.blog.catalog
import handlers.blog.post

import handlers.recommendation.harvest
import handlers.recommendation.process
import handlers.recommendation.fake.cpn
import handlers.recommendation.fake.statistic

handlers = [
    # (r"/_/auth", system.handlers.AuthHandler),
    (r"/_/introduce", system.handlers.IntroduceHandler),
    (r"/_/private", system.handlers.PrivateIntroduceHandler),
    (r"/_/logout", system.handlers.LogoutHandler),

    (r"/_/test", handlers.test.TestHandler),

    # Blog
    (r"/_/catalog/([\w-]+)/([\d+]+)", handlers.blog.catalog.CatalogHandler),
    (r"/_/catalogs", handlers.blog.catalogs.CatalogsHandler),
    (r"/_/post/([\w-]+)", handlers.blog.post.PostHandler),
    (r"/_/post", handlers.blog.post.PostHandler),

    # Recommendation
    (r"/_/recommendation/harvest", handlers.recommendation.harvest.HarvestHandler),
    (r"/_/recommendation/process/([\w-]+)", handlers.recommendation.process.ProcessHandler),

    (r"/_/recommendation/fake/statistic", handlers.recommendation.fake.statistic.FakeStatisticHandler),
    (r"/_/recommendation/fake/cpn", handlers.recommendation.fake.cpn.FakeCPNHandler),
]

DB_HOST = "melchior"
DB_PORT = 27111
DB_NAME = "chimera"

# import motor
# import motorengine
# motorengine.connect(db=DB_NAME, host=DB_HOST, port=DB_PORT)

settings = {
    "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    "login_url": "/login/",

    # "db": motor.MotorClient(host=DB_HOST, port=DB_PORT)[DB_NAME]
    # "db": motorengine.connect(db=DB_NAME, host=DB_HOST, port=DB_PORT)
}

SYSTEM_PORT = 8888

define("port", default=SYSTEM_PORT, help="run on the given port", type=int)

