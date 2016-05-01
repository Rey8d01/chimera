chimera.system.blog.controller("PostItemController", ["$scope", "$state", "postItemService",
    function ($scope, $state, postItemService) {
        // Запрос определенного поста
        postItemService.get({postAlias: $state.params.postAlias}, function (response) {
            $scope.post = response.content;
        });

        $scope.editPost = function () {
            $state.go("main.blog.postEdit", {postAlias: $state.params.postAlias})
        }

        $scope.deletePost = function () {
            postItemService.delete({postAlias: $state.params.postAlias}).$promise.then(function (response) {
                if (response.error.code == 0) {
                    $state.go("main.blog.home")
                }
            });
        }
    }
]);
