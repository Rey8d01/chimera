/**
 * recommendationFakeService
 */

chimera.system.recommendationFake = angular.module("recommendationFake", ["ngResource", "ngSanitize"]);

chimera.system.recommendationFake.controller("RecommendationFakeController", ["$scope", "$state", "recommendationFakeService", "omdbapiService",
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

chimera.system.recommendationFake.factory("recommendationFakeService", ["$resource",
    function ($resource) {
        return $resource("/recommendation/fake/cpn", {}, {
            "getRecommendation" : {method: "POST"}
        });
    }
]);
