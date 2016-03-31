/**
 * Информация по авторам.
 */

chimera.system.author = angular.module("author", ["ngResource", "ngSanitize"]);

/**
 * AuthorItemHandler
 */
chimera.system.author.controller("AuthorHandler", ["$scope", "$state", "authorItemService",
    function ($scope, $state, authorItemService) {
        $scope.main.blogContentLoad = true;
        authorItemService.get({userId: $state.params.userId, page: $state.params.page}, function(response) {
            $scope.author = response.content;
            //$scope.posts = response.content.posts;
            //$scope.paging = response.content.pageData;
            $scope.main.blogContentLoad = false;
        });
    }
]);

chimera.system.author.factory("authorItemService", ["$resource",
    function ($resource) {
        return $resource("/author/:userId/:page", {page: "1"}, {
            save: {method: "POST", params: {userId: null, page: null}}
        });
    }
]);
