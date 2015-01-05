/**
 * Модуль управления постами.
 * Отображает посты в виде миниатюр и целиком загруженных материалов.
 */

chimera.system.post = angular.module("post", ["ngResource", "ngSanitize"]);

// Контроллеры
chimera.system.post.controller("PostController", ["$scope", "$state", "postLoader",
    function ($scope, $state, postLoader) {
        postLoader.get({aliasPost: $state.params.aliasPost}, function(response) {
            $scope.post = response.content;
        });
    }
]);

// Сервис
chimera.system.post.factory("postLoader", ["$resource",
    function ($resource) {
        return $resource(chimera.config.baseUrl + "/post/:aliasPost");
    }]);
