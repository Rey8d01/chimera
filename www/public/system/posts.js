/**
 * Модуль управления постами.
 * Отображает посты в виде миниатюр и целиком загруженных материалов.
 */

chimera.system.collection = angular.module("collection", ["ngResource", "ngSanitize"]);

// Контроллеры
chimera.system.collection.controller("CollectionLatestController", ["$scope", "collectionLoader",
    function ($scope, collectionLoader) {

        // $scope.collection.title = "Последние новости";
        $scope.collection = collectionLoader.get({}, function() {
            $scope.collection.progress = false;
        }, function(response) {
            console.log(response.data);
            $scope.collection.progress = false;
            $scope.collection = response.data;
        });
    }
]);

chimera.system.collection.controller("CollectionPostsController", ["$scope", "$state", "collectionLoader",
    function ($scope, $state, collectionLoader) {
        $scope.collection = collectionLoader.get({slug: $state.params.slug_collection});
    }
]);

chimera.system.collection.controller("CollectionPostController", ["$scope", "$state", "collectionLoader",
    // Для этого может  стоит сделать отдельный модуль
    function ($scope, $state, collectionLoader) {
        $scope.post = collectionLoader.getPost({slug: $state.params.slug_post});
    }
]);

// Сервис
chimera.system.collection.factory("collectionLoader", ["$resource",
    function ($resource) {
        return $resource(chimera.config.baseUrl + ":source/:slug", {source: "collection", slug: "latest"}, {
            getPostsInCollection: {method: "GET"},
            getPost: {method: "GET", params: {source: "post"}}
        });
    }]);
