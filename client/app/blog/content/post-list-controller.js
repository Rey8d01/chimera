chimera.system.blog.controller("PostListController", ["$scope", "$state", "postListService",
    function ($scope, $state, postItemService) {
        $scope.main.blogContentLoad = true;
        catalogItemService.get({catalogAlias: $state.params.catalogAlias, page: $state.params.page}, function (response) {
            $scope.catalog = response.content;
            //$scope.posts = response.content.posts;
            //$scope.paging = response.content.pageData;
            $scope.main.blogContentLoad = false;
        });
    }
]);
