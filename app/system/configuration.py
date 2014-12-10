__author__ = 'rey'

import system.handlers

import handlers.main
import handlers.navigator
import handlers.catalog
import handlers.post

handlers = [
    # (r"/auth", system.handlers.AuthHandler),
    (r"/introduce", system.handlers.IntroduceHandler),
    (r"/logout", system.handlers.LogoutHandler),

    (r"/index", handlers.main.MainerHandler),
    (r"/navigator", handlers.navigator.NavigatorHandler),
    (r"/post/([\w-]+)", handlers.post.PostHandler),
    (r"/collection/([\w-]+)/([\d+]+)", handlers.catalog.CatalogHandler),

    # Neuron
    # (r"/cinema/process/([\w-]+)", CollectionHandler),
    # (r"/cinema/harvest/([\w-]+)", CollectionHandler),
    # (r"/cinema/result/([\w-]+)", CollectionHandler),
]

settings = {
    "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    # "login_url": "/login",

    "twitter_consumer_key": "54HALYb2DrpC3VmdDN5jM9HZB",
    "twitter_consumer_secret": "RtkuUQPhKkk3uk1HclggzCPJk1L3jLfc6P7L6Hz6mZ5Lsadhqt",

    "google_oauth": {
        "key": "484611128919-82v2ugod9iam9v1ipvmo61bfsvhj3c6q.apps.googleusercontent.com",
        "secret": "_ITW0YImv3pfxjJN1UVYoPdU"
    }
}


class Configuration():
    DB_HOST = "localhost"
    DB_PORT = 27017
    DB_NAME = "chimera"