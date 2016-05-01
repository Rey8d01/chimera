chimera.system.blog.controller("AuthorController", ["$scope", "$state", "authorService",
    function ($scope, $state, authorService) {
        $scope.main.blogContentLoad = true;
        authorService.get({userId: $state.params.userId, page: $state.params.page}, function(response) {
            $scope.author = response.content;
            //$scope.posts = response.content.posts;
            //$scope.paging = response.content.pageData;
            $scope.main.blogContentLoad = false;
        });
    }
]);
