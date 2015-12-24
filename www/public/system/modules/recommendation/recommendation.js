/**
 * recommendationService
 */

chimera.system.recommendation = angular.module("recommendation", ["ngResource", "ngSanitize"]);

chimera.system.recommendation.controller("RecommendationController", ["$scope", "$state", "recommendationService", "recommendationFakeService", "omdbapiService",
    function ($scope, $state, recommendationService, recommendationFakeService, omdbapiService) {
        chimera.helpers.log(42);
        var $input = $('.typeahead');

        $scope.selectItem = {
            imdb: null,
            rate: null,
            year: null,
            title: null
        };
        $scope.criticList = {};
        $scope.infoItems = {};

        // Инициализация автокомплита
        $input.typeahead({
            source: function (s, cb) {
                var matches = [];
                $('.typeahead').parent().removeClass("has-error");

                omdbapiService.search({s:s}, function (response) {
                    if(response.Error) {
                        $('.typeahead').parent().addClass("has-error");
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
            afterSelect: function (item) {
                $scope.selectItem.imdb = item.imdb;
                $scope.selectItem.year = item.year;
                $scope.selectItem.title = item.title;
            },
            autoSelect: true
        });

        // Установка оценки
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

        // Начальные данные критики
        recommendationService.get({}, function (response) {
            var criticList = response.content.critic;
            if (criticList) {
                for (var imdb in criticList) {
                    // Сбор инфы по фильмам на основе имдб
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

        // Данные по фейковым юзерам
        recommendationFakeService.get({}, function (response) {
            $scope.fakeUserList = response.content.fakeUserList;
        });
    }
]);

chimera.system.recommendation.factory("recommendationService", ["$resource",
    function ($resource) {
        return $resource("/recommendation/harvest");
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
