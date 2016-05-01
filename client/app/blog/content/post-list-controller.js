chimera.system.blog.controller("PostListController", ["$scope", "$state", "postListService",
    function ($scope, $state, postItemService) {
        $scope.blog.contentLoad = true;
        postListService.get({catalogAlias: $state.params.catalogAlias, page: $state.params.page}, function (response) {
            $scope.catalog = response.content;
            //$scope.posts = response.content.posts;
            //$scope.paging = response.content.pageData;
            $scope.blog.contentLoad = false;
        });
    }
]);
