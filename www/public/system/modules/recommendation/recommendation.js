/**
 * recommendationService
 */

chimera.system.recommendation = angular.module("recommendation", ["ngResource", "ngSanitize"]);

chimera.system.recommendation.controller("RecommendationController", ["$scope", "$state", "recommendationService", "omdbapiService",
    function ($scope, $state, recommendationService, omdbapiService) {
        console.log("RecommendationController");

        var $input = $('.typeahead');

        $scope.selectItem = {
            imdb: null,
            rate: null,
            year: null,
            title: null
        };
        //Title: "Re-cycle"Type: "movie"Year: "2006"imdbID: "tt0498311"

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
                    console.log(response);
                });
            }
        }

    }
]);

chimera.system.recommendation.factory("recommendationService", ["$resource",
    function ($resource) {
        return $resource(chimera.config.baseUrl + "/recommendation/harvest");
    }
]);

chimera.system.recommendation.factory("omdbapiService", ["$resource",
    function ($resource) {
        var urlApi = "//www.omdbapi.com";
        return $resource(urlApi, {}, {
            "search": {'method': "GET", isArray: false, url: urlApi + "/?s=:s", params: {s:''}}
        });
    }
]);
