chimera.system.blog.controller("PostListController", ["$scope", "$state", "postListService",
    function ($scope, $state, postListService) {
        $scope.blog.contentLoad = true;
        postListService.get({typeList: $state.params.typeList, page: $state.params.page}, function (response) {
            $scope.latest = response.content;
            $scope.latest.typeList = $state.params.typeList;
            $scope.blog.contentLoad = false;
        });
    }
]);
