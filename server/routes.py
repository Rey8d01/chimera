import handlers.test
import modules.blog.handlers.author
import modules.blog.handlers.post
import modules.blog.handlers.tag
import modules.blogql.handler
import utils.handler

# Роутинг
routes = [
    # Index
    # (r"/_/auth", system._old.AuthHandler),
    (r"/_/introduce", utils.handler.IntroduceHandler),
    (r"/_/private", utils.handler.PrivateIntroduceHandler),
    (r"/_/logout", utils.handler.LogoutHandler),

    (r"/_/me", handlers.user.MeHandler),
    (r"/_/test-rest", handlers.test.TestRestHandler),
    (r"/_/test-graphql", handlers.test.TestGraphQLHandler),

    # Blog
    (r"/_/author/([\w-]+)/([\d+]+)", modules.blog.handlers.author.AuthorHandler),

    (r"/_/post-item/([\w-]+)", modules.blog.handlers.post.PostItemHandler),
    (r"/_/post-item", modules.blog.handlers.post.PostItemHandler),
    (r"/_/post-list/([\w-]+)/([\d+]+)", modules.blog.handlers.post.PostListHandler),

    (r"/_/tag-item/([\w\-]+)/([\d+]+)", modules.blog.handlers.tag.TagItemHandler),
    (r"/_/tag-list", modules.blog.handlers.tag.TagListHandler),

    (r"/_/blogql", modules.blogql.handler.BlogHandler),
    # Recommendation
    # (r"/_/recommendation/harvest", modules.recommendation._old.harvest.HarvestHandler),
    # (r"/_/recommendation/harvest/list-rated-items/([\d+]+)", modules.recommendation._old.harvest.ListRatedItemsHandler),
    # (r"/_/recommendation/harvest/list-users/([\d+]+)", modules.recommendation._old.harvest.ListUsersHandler),
    #
    # (r"/_/recommendation/metrics/([\w\-]+)/([\w\-]+)", modules.recommendation._old.process.MetricsHandler),
    #
    # (r"/_/recommendation/stat-users/([\w\-]+)/([\w\-]+)", modules.recommendation._old.process.StatisticForUserHandler),
    # (r"/_/recommendation/stat-items/([\w\-]+)/([\w\-]+)", modules.recommendation._old.process.StatisticForItemsHandler),
    # (r"/_/recommendation/stat-utils", modules.recommendation._old.process.UtilsStatisticHandler),
    #
    # (r"/_/recommendation/cpn-user", modules.recommendation._old.process.UserCPNHandler),
    # (r"/_/recommendation/cpn-utils", modules.recommendation._old.process.UtilsCPNHandler),
    #
    # (r"/_/recommendation/fake/statistic", modules.recommendation._old.fake.statistic.FakeStatisticHandler),
    # (r"/_/recommendation/fake/cpn", modules.recommendation._old.fake.cpn.FakeCPNHandler),
]
