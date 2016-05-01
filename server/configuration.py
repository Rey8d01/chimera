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

import handlers.user
import handlers.test

import modules.blog.handlers.author
import modules.blog.handlers.post
import modules.blog.handlers.tag

# import modules.recommendation.handlers.fake.cpn
# import modules.recommendation.handlers.fake.statistic

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
    (r"/_/author/([\w-]+)/([\d+]+)", modules.blog.handlers.author.AuthorHandler),

    (r"/_/post-item/([\w-]+)", modules.blog.handlers.post.PostItemHandler),
    (r"/_/post-item", modules.blog.handlers.post.PostItemHandler),
    (r"/_/post-list", modules.blog.handlers.post.PostListHandler),

    (r"/_/tag-item/([\w\-]+)/([\d+]+)", modules.blog.handlers.tag.TagItemHandler),
    (r"/_/tag-list", modules.blog.handlers.tag.TagListHandler),

    # Recommendation
    # (r"/_/recommendation/harvest", modules.recommendation.handlers.harvest.HarvestHandler),
    # (r"/_/recommendation/harvest/list-rated-items/([\d+]+)", modules.recommendation.handlers.harvest.ListRatedItemsHandler),
    # (r"/_/recommendation/harvest/list-users/([\d+]+)", modules.recommendation.handlers.harvest.ListUsersHandler),
    #
    # (r"/_/recommendation/metrics/([\w\-]+)/([\w\-]+)", modules.recommendation.handlers.process.MetricsHandler),
    #
    # (r"/_/recommendation/stat-users/([\w\-]+)/([\w\-]+)", modules.recommendation.handlers.process.StatisticForUserHandler),
    # (r"/_/recommendation/stat-items/([\w\-]+)/([\w\-]+)", modules.recommendation.handlers.process.StatisticForItemsHandler),
    # (r"/_/recommendation/stat-utils", modules.recommendation.handlers.process.UtilsStatisticHandler),
    #
    # (r"/_/recommendation/cpn-user", modules.recommendation.handlers.process.UserCPNHandler),
    # (r"/_/recommendation/cpn-utils", modules.recommendation.handlers.process.UtilsCPNHandler),
    #
    # (r"/_/recommendation/fake/statistic", modules.recommendation.handlers.fake.statistic.FakeStatisticHandler),
    # (r"/_/recommendation/fake/cpn", modules.recommendation.handlers.fake.cpn.FakeCPNHandler),
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
