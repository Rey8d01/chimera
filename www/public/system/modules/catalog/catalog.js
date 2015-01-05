/**
 * Модуль управления постами.
 * Отображает посты в виде миниатюр и целиком загруженных материалов.
 */

chimera.system.catalog = angular.module("catalog", ["ngResource", "ngSanitize"]);

// Контроллеры
chimera.system.catalog.controller("CatalogPostsController", ["$scope", "$state", "catalogLoader",
    function ($scope, $state, catalogLoader) {
        catalogLoader.get({aliasCatalog: $state.params.aliasCatalog, page: $state.params.page}, function(response) {
            $scope.catalog = response.content;
            $scope.paging = response.content.pageData;
            $scope.catalog.progress = false;
        });
    }
]);

chimera.system.catalog.controller("CatalogListController", ["$scope", "$state", "catalogLoader",
    function ($scope, $state, catalogLoader) {
        // pass
    }
]);

// Сервис
chimera.system.catalog.factory("catalogLoader", ["$resource",
    function ($resource) {
        return $resource(chimera.config.baseUrl + "/catalog/:aliasCatalog/:page", {aliasCatalog: "latest", page: "1"}, {
            // getPost: {method: "GET", params: {source: "post"}}
        });
    }]);
