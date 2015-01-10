/**
 * recommendationService
 */

chimera.system.recommendation = angular.module("recommendation", ["ngResource", "ngSanitize"]);

chimera.system.recommendation.controller("RecommendationController", ["$scope", "$state", "recommendationService", "omdbapiService",
    function ($scope, $state, recommendationService, omdbapiService) {
        omdbapiService.search({}, function (response) {
            console.log(response);
        });
        //postService.get({aliasPost: $state.params.aliasPost}, function(response) {
        //    $scope.post = response.content;
        //});
    }
]);

chimera.system.recommendation.factory("recommendationService", ["$resource",
    function ($resource) {
        //return $resource(chimera.config.baseUrl + "/post/:aliasPost");
    }
]);

chimera.system.recommendation.factory("omdbapiService", ["$resource",
    function ($resource) {
        var urlApi = "//www.omdbapi.com";
        return $resource(urlApi, {}, {
            "search": {'method': "GET", isArray: false, url: urlApi+"/?s=matrix"}
        });
    }
]);
