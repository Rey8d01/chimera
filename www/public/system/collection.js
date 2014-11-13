/**
 * Модуль управления постами.
 * Отображает посты в виде миниатюр и целиком загруженных материалов.
 */

chimera.system.collection = angular.module("collection", ["ngResource", "ngSanitize"]);

// Контроллеры
chimera.system.collection.controller("CollectionLatestController", ["$scope", "collectionLoader",
    function ($scope, collectionLoader) {

        // $scope.collection.title = "Последние новости";
        collectionLoader.get({}, function(response) {
            $scope.collection = response.content
            $scope.collection.progress = false;
        }, function(response) {
            // $scope.collection = response.content;
            $scope.collection.progress = false;
        });
    }
]);

chimera.system.collection.controller("CollectionPostsController", ["$scope", "$state", "collectionLoader",
    function ($scope, $state, collectionLoader) {
        collectionLoader.get({slug: $state.params.slug_collection}, function(response) {
            $scope.collection = response.content
            $scope.collection.progress = false;
        });
    }
]);

chimera.system.collection.controller("CollectionPostController", ["$scope", "$state", "collectionLoader",
    // Для этого может  стоит сделать отдельный модуль
    function ($scope, $state, collectionLoader) {
        collectionLoader.getPost({slug: $state.params.slug_post}, function(response) {
            $scope.post = response.content
            // $scope.post.progress = false;
        });
    }
]);

// Сервис
chimera.system.collection.factory("collectionLoader", ["$resource",
    function ($resource) {
        return $resource(chimera.config.baseUrl + ":source/:slug", {source: "collection", slug: "latest"}, {
            getPost: {method: "GET", params: {source: "post"}}
        });
    }]);
