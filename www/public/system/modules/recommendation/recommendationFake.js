/**
 * recommendationFakeService
 */

chimera.system.recommendationFake = angular.module("recommendationFake", ["ngResource", "ngSanitize"]);

chimera.system.recommendationFake.controller("RecommendationFakeController", ["$scope", "$state", "recommendationFakeService",
    function ($scope, $state, recommendationFakeService) {
        // Данные по фейковым юзерам
        recommendationFakeService.get({}, function (response) {
            $scope.fakeUserList = response.content.fakeUserList;
        });

        // Начальный набор данных для отображения рекомендаций
        $scope.recommendation = {
            "progress": true,
            "fakeUserId": false,
            "fakeUserName": false,
            "fakeOtherUserName": false,
            "neuroRecommendations": false,
            "statRecommendations": false,
            "outStarRecommendations": false
        };
        // Запрос данных рекомендации по указанному пользователю
        $scope.getRecommendation = function(fakeUserId) {
            $scope.recommendation.fakeUserId = fakeUserId;
            recommendationFakeService.getRecommendation($.param({"user": fakeUserId}), function (response) {
                $scope.recommendation.progress = false;
                console.warn(response);
            });
        }
    }
]);

chimera.system.recommendationFake.factory("recommendationFakeService", ["$resource",
    function ($resource) {
        return $resource(chimera.config.baseUrl + "/recommendation/fake/cpn", {}, {
            "getRecommendation" : {method: "POST"}
        });
    }
]);

chimera.system.recommendationFake.factory("omdbapiService", ["$resource",
    function ($resource) {
        var urlApi = "//www.omdbapi.com";
        return $resource(urlApi, {}, {
            "search": {method: "GET", isArray: false, url: urlApi + "/?s=:s", params: {s:''}},
            "findByImdb": {method: "GET", isArray: false, url: urlApi + "/?i=:i", params: {i:''}}
        });
    }
]);
