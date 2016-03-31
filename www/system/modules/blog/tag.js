/**
 * Метки для постов.
 */

chimera.system.tag = angular.module("tag", ["ngResource", "ngSanitize"]);

/**
 * TagItemHandler
 */
chimera.system.tag.controller("TagItemHandler", ["$scope", "$state", "tagItemService",
    function ($scope, $state, tagItemService) {
        $scope.main.blogContentLoad = true;
        tagItemService.get({tagAlias: $state.params.tagAlias, page: $state.params.page}, function(response) {
            $scope.tag = response.content;
            //$scope.posts = response.content.posts;
            //$scope.paging = response.content.pageData;
            $scope.main.blogContentLoad = false;
        });
    }
]);

/**
 * TagListHandler
 */
chimera.system.tag.controller("TagListMainController", ["$scope", "$state", "tagListService",
    function ($scope, $state, tagListService) {
        tagListService.get({}, function(response) {
            $scope.tags = response.content.tags;
        });
    }
]);

chimera.system.tag.factory("tagItemService", ["$resource",
    function ($resource) {
        return $resource("/tag/:tagAlias/:page", {page: "1"}, {
            save: {method: "POST", params: {tagAlias: null, page: null}}
        });
    }
]);

chimera.system.tag.factory("tagListService", ["$resource",
    function ($resource) {
        return $resource("/tags");
    }
]);