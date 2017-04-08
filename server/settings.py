"""Файл конфигурации системы.

Содержит настройки подключения к внешним ресурсам, роутинг и настройки работы системы.

todo реализовать проверки по наличию соединений с базой, кешем и др.

"""

import json
try:
    f = open("./local/settings.json")
    settings = json.load(f)
except Exception:
    # В случае проблем с чтением настроек из файла, оставим пустые настройки.
    settings = {}

# Базовые настройки запуска системы

from tornado.options import define
define("port", default=settings["system_port"], help="run on the given port", type=int)

# Настройки подключения к базе данных MongoDB
from motor.motor_tornado import MotorClient
database = motor_client = None
settings_db = settings.get("db", {})
for connection_name, setting_db in settings_db.items():
    # database = motorengine.connect(db=setting_db["name"], host=setting_db["host"], port=setting_db["port"], alias=connection_name)
    database = motor_client = MotorClient(setting_db["host"], setting_db["port"])[setting_db["name"]]

# Настройки подключения к Redis
import tredis
redis = tredis.RedisClient(host=settings["redis"]["host"], port=settings["redis"]["port"])

# Настройки SSL
import ssl
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
    "db": database,
    "redis": redis,
}

settings.update(system_settings)
