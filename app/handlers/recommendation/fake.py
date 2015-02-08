__author__ = 'rey'

from system.handlers import BaseHandler, MainHandler
from documents.fake import UserDocument
from system.components.recommendations.statistic import Recommendations

import tornado.web
from tornado import gen


class FakeHandler(MainHandler):

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        """
        Запрос чистых данных по пользователям (случайные 10)
        Список фильмов топ250
        :return:
        """

        collection_critic = yield UserDocument().objects.find_all()

        list_criric = {}
        for document_critic in collection_critic:
            # print(document_critic._id)
            # print(document_critic.critic)
            list_criric[str(document_critic._id)] = document_critic.critic

        # Recommendations
        # print(list_criric)
        #
        my_stat = Recommendations(list_criric)
        test1 = '54c92bbc80a9e1252dff9949'
        test2 = '54c92bbc80a9e1252dff9d18'
        movie = 'tt0407887'

        print(
            'Люди:', test1, 'и', test2, '\n',
            'Евклидово расстояние		', my_stat.distance(my_stat.source, test1, test2), '\n',
            'Корреляця Пирсона			', my_stat.pearson(my_stat.source, test1, test2), '\n',
            'Коэффициент Жаккара		', my_stat.jaccard(my_stat.source, test1, test2), '\n',
            'Манхэттенское расстояние	', my_stat.manhattan(my_stat.source, test1, test2), '\n',
            '\n',
            'Ранжирование критиков		', my_stat.top_matches(test1, 2, my_stat.TYPE_SOURCE, my_stat.pearson), '\n',
            'Выработка рекомендации		', my_stat.get_recommendations(test1), '\n',
            '\n',
            'Фильмы похожие на 			', movie, my_stat.top_matches(movie, 3, my_stat.TYPE_TRANSFORMS, my_stat.pearson), '\n',
            'Кто еще не смотрел фильм	', movie, my_stat.get_recommendations_transforms(movie), '\n',
            # 'AAAAAAAAAA	', my_stat.transforms, '\n',
            # '\n',
            # 'Похожие фильмы	\n			', my_stat.similar_items, '\n',
            # 'Выработка рекомендации	по образцам	', my_stat.get_recommendations_items(test1), '\n',
        )
        self.write({"ee":55})

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        """
        Расчет статистики

        В качестве параметров передавать список необходимых данных и расчеты для них
        :return:
        """
        self.write(2)