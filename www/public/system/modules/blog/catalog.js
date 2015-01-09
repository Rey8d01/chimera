/**
 * Основной контент это список из постов относящихся к каталогу
 */

chimera.system.catalog = angular.module("catalog", ["ngResource", "ngSanitize"]);

chimera.system.catalog.controller("CatalogPostsController", ["$scope", "$state", "catalogService",
    function ($scope, $state, catalogService) {
        catalogService.get({aliasCatalog: $state.params.aliasCatalog, page: $state.params.page}, function(response) {
            $scope.catalog = response.content;
            $scope.paging = response.content.pageData;
            $scope.catalog.progress = false;
        });
    }
]);

chimera.system.main.controller("CatalogLatestController", ["$scope", "$state", "catalogService",
    function ($scope, $state, catalogService) {

        if(!$state.params.aliasCatalog) {
            $state.params.aliasCatalog = "latest";
        }            

        catalogService.get({}, function(response) {
            $scope.catalog = response.content;
            $scope.paging = response.content.pageData;
            $scope.catalog.progress = false;  
        }, function(response) {
            $scope.catalog.progress = false;
        });
    }
]);

chimera.system.catalog.factory("catalogService", ["$resource",
    function ($resource) {
        return $resource(chimera.config.baseUrl + "/catalog/:aliasCatalog/:page", {aliasCatalog: "latest", page: "1"});
    }
]);
