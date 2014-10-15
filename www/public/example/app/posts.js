/**
 * Модуль управления постами.
 * Отображает посты в виде миниатюр и целиком загруженных материалов.
 */

chimera.system.posts = angular.module("posts", ["ngResource", "ngSanitize"]);

// Контроллеры
chimera.system.posts.controller("LatestPostsController", ["$scope", "loaderPosts",
    function ($scope, loaderPosts) {
        $scope.collection = loaderPosts.getPostsInCollection();
    }
]);

chimera.system.posts.controller("PostsInCollectionController", ["$scope", "$state", "loaderPosts",
    function ($scope, $state, loaderPosts) {
        $scope.collection = loaderPosts.getPostsInCollection({id: $state.params.slug});
    }
]);

chimera.system.posts.controller("PostController", ["$scope", "$state", "loaderPosts",
    function ($scope, $state, loaderPosts) {
        $scope.post = loaderPosts.getPost({id: $state.params.id});
    }
]);

// Сервис
chimera.system.posts.factory("loaderPosts", ["$resource",
    function ($resource) {
        return $resource("/example/app/responses/:collection/:id.json", {collection: "collection", id: "latest"}, {
            getPostsInCollection: {method: "GET"},
            getPost: {method: "GET", params: {collection: "posts"}}
        });
    }]);
