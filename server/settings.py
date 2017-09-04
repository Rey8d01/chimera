"""Файл конфигурации системы.

Содержит настройки подключения к внешним ресурсам, роутинг и настройки работы системы.

"""

import json
import ssl

import tredis
from motor.motor_tornado import MotorClient
from tornado.options import define

try:
    f = open("./local/settings.json")
    settings = json.load(f)
except Exception:
    # В случае проблем с чтением настроек из файла, оставим пустые настройки.
    settings = {}

# Базовые настройки запуска системы
define("port", default=settings["system_port"], help="run on the given port", type=int)

# Настройки подключения к базе данных MongoDB
client_motor = db_motor = None
settings_db = settings.get("db", {})
for connection_name, setting_db in settings_db.items():
    client_motor = MotorClient(setting_db["host"], setting_db["port"])
    # todo Разрулить с доступами к базам
    db_motor = client_motor[setting_db["name"]]

# Настройки подключения к Redis
client_redis = tredis.RedisClient(host=settings["redis"]["host"], port=settings["redis"]["port"])

# Настройки SSL
try:
    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_ctx.load_cert_chain(settings["ssl"]["certificates"][0], settings["ssl"]["certificates"][1])
except KeyError:
    ssl_ctx = None

# Настройки приложения - доступны внутри хендлеров через self.settings
system_settings = {
    "client_motor": db_motor,
    "client_redis": client_redis,
}

settings.update(system_settings)
