"""Роутинг."""
import modules.handler

routes = [
    # GraphQL API
    (r"/_/public", modules.handler.PublicHandler),
    (r"/_/private", modules.handler.PrivateHandler),
]
