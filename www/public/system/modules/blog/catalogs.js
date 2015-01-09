/**
 * Меню из списка каталогов
 */

chimera.system.catalogs = angular.module("catalogs", ["ngResource"]);

chimera.system.catalogs.controller("CatalogsMenuController", ["$scope", "$state", "catalogsService",
    function ($scope, $state, catalogsService) {
        catalogsService.get({}, function(response) {
            $scope.catalogs = response.content.catalogs;
        });
    }
]);

chimera.system.catalogs.factory("catalogsService", ["$resource",
    function ($resource) {
        return $resource(chimera.config.baseUrl + "/catalogs");
    }
]);
