/**
 * Модуль управления постами.
 * Отображает посты в виде миниатюр и целиком загруженных материалов.
 */

chimera.system.collection = angular.module("collection", ["ngResource", "ngSanitize"]);

// Контроллеры
chimera.system.collection.controller("CollectionPostsController", ["$scope", "$state", "collectionLoader",
    function ($scope, $state, collectionLoader) {
        collectionLoader.get({aliasCollection: $state.params.aliasCollection, page: $state.params.page}, function(response) {
            $scope.collection = response.content;
            $scope.paging = response.content.pageData;
            $scope.collection.progress = false;
        });
    }
]);

chimera.system.collection.controller("CollectionListController", ["$scope", "$state", "collectionLoader",
    function ($scope, $state, collectionLoader) {
        // pass
    }
]);

// Сервис
chimera.system.collection.factory("collectionLoader", ["$resource",
    function ($resource) {
        return $resource(chimera.config.baseUrl + "/collection/:aliasCollection/:page", {aliasCollection: "latest", page: "1"}, {
            // getPost: {method: "GET", params: {source: "post"}}
        });
    }]);
