/**
 * Модуль рекомендаций для пользователей на примере работы с фильмами. Основная задача собирать данные оценок пользователей к фильмам,
 * а значит и запрашивать информацию по ним. Используется сторонний сервис для забора базы по фильмам www.omdbapi.com
 * где id к фильму будет его номер в системе imdb и он будет использоваться для идентификации фильма при просмотре оценок.
 */

chimera.system.recommendation = angular.module("recommendation", ["ngResource", "ngSanitize"]);

/**
 * Harvest
 */
chimera.system.recommendation.controller("RecommendationController", ["$scope", "$state", "recommendationService", "recommendationFakeService", "omdbapiService",
    function ($scope, $state, recommendationService, recommendationFakeService, omdbapiService) {
        /**
         * Основной контроллер системы рекомендаций загружает информацию по уже оцененным фильмам авторизованного пользователя и
         * подгружает их названия из стороннего сервиса.
         */
        $scope.selectItem = {
            imdb: null,
            rate: null,
            year: null,
            title: null
        };
        $scope.criticList = {};
        $scope.infoItems = {};

        // Инициализация автокомплита для поиска фильмов.
        var $inputSetRate = $('.typeahead');
        $inputSetRate.typeahead({
            delay: 300,
            /**
             * Источником данных для автокомлпита будет внешний сервис www.omdbapi.com
             */
            source: function (s, cb) {
                var matches = [];
                $inputSetRate.parent().removeClass("has-error");

                omdbapiService.search({s:s}, function (response) {
                    if(response.Error) {
                        $inputSetRate.parent().addClass("has-error");
                    } else {
                        for(var item in response.Search) {
                            matches.push({
                                imdb: response.Search[item].imdbID,
                                year: response.Search[item].Year,
                                title: response.Search[item].Title,
                                name: response.Search[item].Title
                            });
                        }
                    }

                    cb(matches);
                });
            },
            /**
             * По выбору фильма из автокомплита данные будут помещены в скоп для последующей отправки на сохранение оценки.
             */
            afterSelect: function (item) {
                $scope.selectItem.imdb = item.imdb;
                $scope.selectItem.year = item.year;
                $scope.selectItem.title = item.title;
            },
            autoSelect: true
        });

        /**
         * Установка оценки.
         *
         * @param {Number} rate
         */
        $scope.setRate = function(rate) {
            $scope.selectItem.rate = rate;
            if ($scope.selectItem.imdb) {
                recommendationService.save($scope.selectItem, function (response) {
                    // @todo в рамках одной сессии - могут быть повторы при изменении оценки
                    $scope.criticList[response.content.imdb] = response.content.rate;
                    // getInfoItem(response.content.imdb);

                    $scope.criticList[$scope.selectItem.imdb] = {
                        // imdb: response.Search[item].imdbID,
                        year: $scope.selectItem.year,
                        title: $scope.selectItem.title,
                        rate: rate
                    };

                });
            }
        };

        /**
         * Начальная выборка нескольких последних оцененных фильмов.
         */
        recommendationService.get({}, function (response) {
            var criticList = response.content;
            if (criticList) {
                for (var imdb in criticList) {
                    // Сбор инфы по фильмам на основе имдб.
                    omdbapiService.findByImdb({i:imdb}, function(response) {
                        $scope.criticList[response.imdbID] = {
                            imdb: response.imdbID,
                            year: response.Year,
                            title: response.Title,
                            rate: criticList[response.imdbID]
                        };
                    });
                }
            }
        });

        // Демонстрационные данные пользователей.
        $scope.fakeUserList = [];
        //recommendationFakeService.get({}, function (response) {
        //    $scope.fakeUserList = response.content.fakeUserList;
        //});
    }
]);

chimera.system.recommendation.factory("recommendationService", ["$resource",
    function ($resource) {
        return $resource("/recommendation/harvest/:count", {count: 5}, {
            save: {method: "POST", params: {count: null}}
        });
    }
]);

/**
 *
 */
chimera.system.recommendation.controller("RecommendationDemoController", ["$scope", "$state", "recommendationFakeService", "omdbapiService",
    function ($scope, $state, recommendationFakeService, omdbapiService) {
        $scope.progress = true;

        // Данные по фейковым юзерам
        recommendationFakeService.get({}, function (response) {
            $scope.fakeUserList = response.content.fakeUserList;
            $scope.progress = false;
        });

        // Начальный набор данных для отображения рекомендаций
        $scope.recommendation = {
            "fakeUserId": false,
            "fakeUserName": false
        };

        // Запрос данных рекомендации по указанному пользователю
        $scope.getRecommendation = function(fakeUserId, fakeUserName) {
            $scope.recommendation.fakeUserId = fakeUserId;
            $scope.recommendation.fakeUserName = fakeUserName;
            $scope.progress = true;

            recommendationFakeService.getRecommendation($.param({"user": fakeUserId}), function (response) {
                $scope.recommendation.clusterName = response.content.cluster;
                $scope.recommendation.fakeOtherUserName = response.content.otherUser;
                $scope.recommendation.neuroRecommendations = $scope.showRecommendation(response.content.neuroRecommendations);
                $scope.recommendation.statRecommendations = $scope.showRecommendation(response.content.statRecommendations);
                $scope.recommendation.outStarRecommendations = $scope.showRecommendation(response.content.outStarRecommendations);
                $scope.recommendation.infoClusters = response.content.infoClusters;
                $scope.progress = false;
            });
        };

        $scope.showRecommendation = function(sourceObject, length, desc) {
            desc = desc != undefined ? desc : true;
            length = length != undefined ? length : 5;

            var sortable = [];
            for (var id in sourceObject) {
                sortable.push([id, sourceObject[id]]);
            }

            if (desc) {
                sortable.sort(function(a, b) {return b[1] - a[1]});
            } else {
                sortable.sort(function(a, b) {return a[1] - b[1]});
            }

            return sortable.slice(0, length)
        };

        $scope.movies = {};
        $scope.getMovieByImdb = function(imdb) {
            if (!$scope.movies.hasOwnProperty(imdb)) {
                $scope.movies[imdb] = {
                    imdb: '',
                    year: '',
                    title: '',
                    rate: ''
                };
                omdbapiService.findByImdb({i:imdb}, function(response) {
                    $scope.movies[imdb] = {
                        imdb: response.imdbID,
                        year: response.Year,
                        title: response.Title
                    };
                });
            }
            return $scope.movies[imdb];
        };
    }
]);

chimera.system.recommendation.factory("recommendationFakeService", ["$resource",
    function ($resource) {
        return $resource("/recommendation/fake/cpn", {}, {
            "getRecommendation" : {method: "POST"}
        });
    }
]);

chimera.system.recommendation.factory("recommendationFakeService", ["$resource",
    function ($resource) {
        return $resource("/recommendation/fake");
    }
]);

chimera.system.recommendation.factory("omdbapiService", ["$resource",
    function ($resource) {
        var urlApi = "//www.omdbapi.com";
        return $resource(urlApi, {}, {
            "search": {'method': "GET", isArray: false, url: urlApi + "/?s=:s", params: {s:''}},
            "findByImdb": {'method': "GET", isArray: false, url: urlApi + "/?i=:i", params: {i:''}}
        });
    }
]);
