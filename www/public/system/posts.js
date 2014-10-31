/**
 * Модуль управления постами.
 * Отображает посты в виде миниатюр и целиком загруженных материалов.
 */

chimera.system.posts = angular.module("posts", ["ngResource", "ngSanitize"]);

// Контроллеры
chimera.system.posts.controller("LatestPostsController", ["$scope", "loaderPosts",
    function ($scope, loaderPosts) {
        console.log(loaderPosts.getPostsInCollection());
        $scope.collection = loaderPosts.getPostsInCollection();
    }
]);

chimera.system.posts.controller("PostsInCollectionController", ["$scope", "$state", "loaderPosts",
    function ($scope, $state, loaderPosts) {
        $scope.collection = loaderPosts.getPostsInCollection({slug: $state.params.slug_collection});
    }
]);

chimera.system.posts.controller("PostController", ["$scope", "$state", "loaderPosts",
    function ($scope, $state, loaderPosts) {
        $scope.post = loaderPosts.getPost({slug: $state.params.slug_post});
    }
]);

// Сервис
chimera.system.posts.factory("loaderPosts", ["$resource",
    function ($resource) {
        return $resource("/system/responses/:source/:slug.json", {source: "collection", slug: "latest"}, {
            getPostsInCollection: {method: "GET"},
            getPost: {method: "GET", params: {source: "post"}}
        });
    }]);
