__author__ = 'rey'

import system.handlers

import handlers.main
import handlers.navigator
import handlers.blog.catalogs
import handlers.blog.catalog
import handlers.blog.post

import handlers.recommendation.harvest
import handlers.recommendation.process
import handlers.recommendation.result
import handlers.recommendation.fake

DB_HOST = "localhost"
DB_PORT = 27017
DB_NAME = "chimera"

handlers = [
    # (r"/_/auth", system.handlers.AuthHandler),
    (r"/_/introduce", system.handlers.IntroduceHandler),
    (r"/_/logout", system.handlers.LogoutHandler),

    (r"/_/index", handlers.main.MainerHandler),
    # (r"/_/navigator", handlers.navigator.NavigatorHandler),

    # Blog
    (r"/_/catalog/([\w-]+)/([\d+]+)", handlers.blog.catalog.CatalogHandler),
    (r"/_/catalogs", handlers.blog.catalogs.CatalogsHandler),
    (r"/_/post/([\w-]+)", handlers.blog.post.PostHandler),

    # Recommendation
    (r"/_/recommendation/harvest", handlers.recommendation.harvest.HarvestHandler),
    (r"/_/recommendation/process/([\w-]+)", handlers.recommendation.process.ProcessHandler),
    (r"/_/recommendation/result/([\w-]+)", handlers.recommendation.result.ResultHandler),
    (r"/_/recommendation/fake", handlers.recommendation.fake.FakeHandler),
]

settings = {
    "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    "login_url": "/login/",

    "twitter_consumer_key": "54HALYb2DrpC3VmdDN5jM9HZB",
    "twitter_consumer_secret": "RtkuUQPhKkk3uk1HclggzCPJk1L3jLfc6P7L6Hz6mZ5Lsadhqt",

    "google_oauth": {
        "key": "484611128919-82v2ugod9iam9v1ipvmo61bfsvhj3c6q.apps.googleusercontent.com",
        "secret": "_ITW0YImv3pfxjJN1UVYoPdU"
    }
}
