"""Файл конфигурации системы.

Содержит настройки подключения к внешним ресурсам, роутинг и настройки работы системы.

todo реализовать проверки по наличию соединений с базой, кешем и др.

"""

from tornado.options import define

# import motor
import motorengine

import tredis

import system.handler

import handlers.test
import handlers.user
import handlers.blog.catalog
import handlers.blog.post
import handlers.blog.tag
import handlers.blog.author

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

    (r"/_/me", handlers.user.MeHandler),
    (r"/_/test", handlers.test.TestHandler),

    # Blog
    (r"/_/author/([\w-]+)/([\d+]+)", handlers.blog.author.AuthorHandler),

    (r"/_/catalog", handlers.blog.catalog.CatalogEditHandler),
    (r"/_/catalog/([\w-]+)/([\d+]+)", handlers.blog.catalog.CatalogItemHandler),
    (r"/_/catalogs", handlers.blog.catalog.CatalogListMainHandler),
    (r"/_/catalogs/([\w-]+)", handlers.blog.catalog.CatalogListChildrenHandler),

    (r"/_/tag/([\w\-]+)/([\d+]+)", handlers.blog.tag.TagItemHandler),
    (r"/_/tags", handlers.blog.tag.TagListHandler),

    (r"/_/post", handlers.blog.post.PostEditHandler),
    (r"/_/post/([\w-]+)", handlers.blog.post.PostHandler),

    # Recommendation
    (r"/_/recommendation/harvest/([\d+]+)", handlers.recommendation.harvest.ListRatedItemsHandler),
    (r"/_/recommendation/harvest", handlers.recommendation.harvest.HarvestHandler),
    (r"/_/recommendation/stat-users/([\w\-]+)/([\w\-]+)", handlers.recommendation.process.StatisticForUserHandler),
    (r"/_/recommendation/stat-items/([\w\-]+)/([\w\-]+)", handlers.recommendation.process.StatisticForItemsHandler),
    (r"/_/recommendation/cpn-user", handlers.recommendation.process.UserCPNHandler),
    (r"/_/recommendation/cpn-utils", handlers.recommendation.process.UtilsCPNHandler),

    (r"/_/recommendation/fake/statistic", handlers.recommendation.fake.statistic.FakeStatisticHandler),
    (r"/_/recommendation/fake/cpn", handlers.recommendation.fake.cpn.FakeCPNHandler),
]

# Настройки подключения к базе данных MongoDB
DB_HOST = "melchior"
DB_PORT = 27111
DB_NAME = "chimera"

motorengine.connect(db=DB_NAME, host=DB_HOST, port=DB_PORT)

# Настройки подключения к Redis
REDIS_HOST = "localhost"
REDIS_PORT = 6379

redis = tredis.RedisClient(host=REDIS_HOST, port=REDIS_PORT)

# Настройки приложения - доступны внутри хендлеров через self.settings
settings = {
    "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    "login_url": "/login/",

    # Для тестирования можно подключиться к MongoDB через Motor напрямую
    # "db": motor.MotorClient(host=DB_HOST, port=DB_PORT)[DB_NAME]
    # "db": motorengine.connect(db=DB_NAME, host=DB_HOST, port=DB_PORT)

    "redis": redis,
}
