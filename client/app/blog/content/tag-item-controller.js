chimera.system.blog.controller("TagItemController", ["$scope", "$state", "tagItemService",
    function ($scope, $state, tagItemService) {
        $scope.blog.contentLoad = true;
        tagItemService.get({tagAlias: $state.params.tagAlias, page: $state.params.page}, function(response) {
            $scope.tag = response.content;
            //$scope.posts = response.content.posts;
            //$scope.paging = response.content.pageData;
            $scope.blog.contentLoad = false;
        });
    }
]);
