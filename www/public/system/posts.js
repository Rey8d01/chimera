/**
 * Модуль управления постами.
 * Отображает посты в виде миниатюр и целиком загруженных материалов.
 */

chimera.system.post = angular.module("post", ["ngResource", "ngSanitize"]);

// Контроллеры
chimera.system.post.controller("PostLatestController", ["$scope", "postLoader",
    function ($scope, postLoader) {

        // $scope.post.title = "Последние новости";
        $scope.post = postLoader.get({}, function() {
            $scope.post.progress = false;
        }, function(response) {
            console.log(response.data);
            $scope.post.progress = false;
            $scope.post = response.data;
        });
    }
]);

chimera.system.post.controller("PostController", ["$scope", "$state", "postLoader",
    function ($scope, $state, postLoader) {
        $scope.post = postLoader.getPost({slug: $state.params.slug_post});
    }
]);

// Сервис
chimera.system.post.factory("postLoader", ["$resource",
    function ($resource) {
        return $resource(chimera.config.baseUrl + ":source/:slug", {source: "post", slug: "latest"}, {
            // getPost: {method: "GET", params: {source: "post"}}
        });
    }]);
