"""Файл конфигурации системы.

Содержит настройки подключения к внешним ресурсам, роутинг и настройки работы системы.

"""

from tornado.options import define

# import motor
import motorengine

import system.handler

import handlers.test
import handlers.blog.catalog
import handlers.blog.post
import handlers.blog.tag

import handlers.recommendation.harvest
import handlers.recommendation.process
import handlers.recommendation.fake.cpn
import handlers.recommendation.fake.statistic

# Базовые настройки запуска системы
SYSTEM_PORT = 8888
define("port", default=SYSTEM_PORT, help="run on the given port", type=int)

# Роутинг
handlers = [
    # Index
    # (r"/_/auth", system.handlers.AuthHandler),
    (r"/_/introduce", system.handler.IntroduceHandler),
    (r"/_/private", system.handler.PrivateIntroduceHandler),
    (r"/_/logout", system.handler.LogoutHandler),

    (r"/_/test", handlers.test.TestHandler),

    # Blog
    (r"/_/catalog", handlers.blog.catalog.CatalogEditHandler),
    (r"/_/catalog/([\w-]+)/([\d+]+)", handlers.blog.catalog.CatalogItemHandler),
    (r"/_/catalogs", handlers.blog.catalog.CatalogListMainHandler),
    (r"/_/catalogs/([\w-]+)", handlers.blog.catalog.CatalogListChildrenHandler),

    (r"/_/tag/([\w\-]+)/([\d+]+)", handlers.blog.tag.TagItemHandler),
    (r"/_/tags", handlers.blog.tag.TagListHandler),

    (r"/_/post", handlers.blog.post.PostEditHandler),
    (r"/_/post/([\w-]+)", handlers.blog.post.PostHandler),

    # Recommendation
    (r"/_/recommendation/harvest", handlers.recommendation.harvest.HarvestHandler),
    (r"/_/recommendation/process/([\w-]+)", handlers.recommendation.process.ProcessHandler),

    (r"/_/recommendation/fake/statistic", handlers.recommendation.fake.statistic.FakeStatisticHandler),
    (r"/_/recommendation/fake/cpn", handlers.recommendation.fake.cpn.FakeCPNHandler),
]

# Настройки подключения к базе данных MongoDB
DB_HOST = "melchior"
DB_PORT = 27111
DB_NAME = "chimera"

motorengine.connect(db=DB_NAME, host=DB_HOST, port=DB_PORT)

# Настройки приложения - доступны внутри хендлеров через self.settings
settings = {
    "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    "login_url": "/login/",

    # Для тестирования можно подключиться к MongoDB через Motor напрямую
    # "db": motor.MotorClient(host=DB_HOST, port=DB_PORT)[DB_NAME]
    # "db": motorengine.connect(db=DB_NAME, host=DB_HOST, port=DB_PORT)
}
