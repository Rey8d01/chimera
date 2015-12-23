/**
 * Информация по авторам.
 */

chimera.system.author = angular.module("author", ["ngResource", "ngSanitize"]);

/**
 * AuthorItemHandler
 */
chimera.system.author.controller("AuthorHandler", ["$scope", "$state", "authorItemService",
    function ($scope, $state, authorItemService) {
        authorItemService.get({userId: $state.params.userId, page: $state.params.page}, function(response) {
            $scope.author = response.content;
            $scope.paging = response.content.pageData;
            $scope.author.progress = false;
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
