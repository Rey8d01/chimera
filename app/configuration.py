"""Файл конфигурации системы.

Содержит настройки подключения к внешним ресурсам, роутинг и настройки работы системы.

todo реализовать проверки по наличию соединений с базой, кешем и др.

"""
import json
import ssl

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

try:
    f = open("./local/settings.json")
    settings = json.load(f)
except Exception:
    # В случае проблем с чтением настроек из файла, оставим пустые настройки.
    settings = {}

# Базовые настройки запуска системы
define("port", default=settings["system_port"], help="run on the given port", type=int)

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

    (r"/_/post-edit", handlers.blog.post.PostEditHandler),
    (r"/_/post-edit/([\w-]+)", handlers.blog.post.PostEditHandler),
    (r"/_/post/([\w-]+)", handlers.blog.post.PostHandler),

    (r"/_/tag-item/([\w\-]+)/([\d+]+)", handlers.blog.tag.TagItemHandler),
    (r"/_/tag-list", handlers.blog.tag.TagListHandler),

    (r"/_/catalog-edit", handlers.blog.catalog.CatalogEditHandler),
    (r"/_/catalog-edit/([\w-]+)", handlers.blog.catalog.CatalogEditHandler),
    (r"/_/catalog-item/([\w-]+)/([\d+]+)", handlers.blog.catalog.CatalogItemHandler),
    (r"/_/catalog-list-main", handlers.blog.catalog.CatalogListMainHandler),
    (r"/_/catalog-list-children/([\w-]+)", handlers.blog.catalog.CatalogListChildrenHandler),

    # Recommendation
    (r"/_/recommendation/harvest", handlers.recommendation.harvest.HarvestHandler),
    (r"/_/recommendation/harvest/list-rated-items/([\d+]+)", handlers.recommendation.harvest.ListRatedItemsHandler),
    (r"/_/recommendation/harvest/list-users/([\d+]+)", handlers.recommendation.harvest.ListUsersHandler),

    (r"/_/recommendation/metrics/([\w\-]+)/([\w\-]+)", handlers.recommendation.process.MetricsHandler),

    (r"/_/recommendation/stat-users/([\w\-]+)/([\w\-]+)", handlers.recommendation.process.StatisticForUserHandler),
    (r"/_/recommendation/stat-items/([\w\-]+)/([\w\-]+)", handlers.recommendation.process.StatisticForItemsHandler),
    (r"/_/recommendation/stat-utils", handlers.recommendation.process.UtilsStatisticHandler),

    (r"/_/recommendation/cpn-user", handlers.recommendation.process.UserCPNHandler),
    (r"/_/recommendation/cpn-utils", handlers.recommendation.process.UtilsCPNHandler),

    (r"/_/recommendation/fake/statistic", handlers.recommendation.fake.statistic.FakeStatisticHandler),
    (r"/_/recommendation/fake/cpn", handlers.recommendation.fake.cpn.FakeCPNHandler),
]

# Настройки подключения к базе данных MongoDB
motorengine.connect(db=settings["db"]["name"], host=settings["db"]["host"], port=settings["db"]["port"])

# Настройки подключения к Redis
redis = tredis.RedisClient(host=settings["redis"]["host"], port=settings["redis"]["port"])

# Настройки SSL
try:
    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_ctx.load_cert_chain(settings["ssl"]["certificates"][0], settings["ssl"]["certificates"][1])
except KeyError:
    ssl_ctx = None

# Настройки приложения - доступны внутри хендлеров через self.settings
system_settings = {
    # Для тестирования можно подключиться к MongoDB через Motor напрямую
    # "db": motor.MotorClient(host=DB_HOST, port=DB_PORT)[DB_NAME]
    # "db": motorengine.connect(db=DB_NAME, host=DB_HOST, port=DB_PORT)
    "redis": redis,
}

settings.update(system_settings)
