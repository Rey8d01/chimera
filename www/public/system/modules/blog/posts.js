/**
 * Основной контент это текст поста
 */

chimera.system.post = angular.module("post", ["ngResource", "ngSanitize"]);

chimera.system.post.controller("PostController", ["$scope", "$state", "postService",
    function ($scope, $state, postService) {
        postService.get({aliasPost: $state.params.aliasPost}, function(response) {
            $scope.post = response.content;
        });
    }
]);

chimera.system.post.factory("postService", ["$resource",
    function ($resource) {
        return $resource(chimera.config.baseUrl + "/post/:aliasPost");
    }
]);
