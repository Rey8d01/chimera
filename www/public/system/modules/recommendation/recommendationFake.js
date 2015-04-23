/**
 * recommendationFakeService
 */

chimera.system.recommendationFake = angular.module("recommendationFake", ["ngResource", "ngSanitize"]);

chimera.system.recommendationFake.controller("RecommendationFakeController", ["$scope", "$state", "recommendationFakeService", "omdbapiService",
    function ($scope, $state, recommendationFakeService, omdbapiService) {
        $scope.selectItem = {
            imdb: null,
            rate: null,
            year: null,
            title: null
        };
        $scope.criticList = {};
        $scope.infoItems = {};

        // Данные по фейковым юзерам
        recommendationFakeService.get({}, function (response) {
            $scope.fakeUserList = response.content.fakeUserList;
        });
    }
]);

chimera.system.recommendationFake.factory("recommendationFakeService", ["$resource",
    function ($resource) {
        return $resource(chimera.config.baseUrl + "/recommendation/fake");
    }
]);

chimera.system.recommendationFake.factory("omdbapiService", ["$resource",
    function ($resource) {
        var urlApi = "//www.omdbapi.com";
        return $resource(urlApi, {}, {
            "search": {'method': "GET", isArray: false, url: urlApi + "/?s=:s", params: {s:''}},
            "findByImdb": {'method': "GET", isArray: false, url: urlApi + "/?i=:i", params: {i:''}}
        });
    }
]);
