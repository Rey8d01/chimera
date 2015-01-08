/**
 * Модуль управления постами.
 * Отображает посты в виде миниатюр и целиком загруженных материалов.
 */

chimera.system.post = angular.module("post", ["ngResource", "ngSanitize"]);

// Контроллеры
chimera.system.post.controller("PostController", ["$scope", "$state", "postService",
    function ($scope, $state, postService) {
        postService.get({aliasPost: $state.params.aliasPost}, function(response) {
            $scope.post = response.content;
        });
    }
]);

// Сервис
chimera.system.post.factory("postService", ["$resource",
    function ($resource) {
        return $resource(chimera.config.baseUrl + "/post/:aliasPost");
    }
]);
