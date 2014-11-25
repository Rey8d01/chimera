/**
 * Модуль управления постами.
 * Отображает посты в виде миниатюр и целиком загруженных материалов.
 */

chimera.system.post = angular.module("post", ["ngResource", "ngSanitize"]);

// Контроллеры
chimera.system.post.controller("PostController", ["$scope", "$state", "postLoader",
    function ($scope, $state, postLoader) {
        $scope.post = postLoader.get({slug: $state.params.slugPost});
    }
]);

// Сервис
chimera.system.post.factory("postLoader", ["$resource",
    function ($resource) {
        return $resource(chimera.config.baseUrl + "/post/:slug", {slug: "latest"}, {
            // getPost: {method: "GET", params: {source: "post"}}
        });
    }]);
