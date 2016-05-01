chimera.system.blog.controller("PostEditController", ["$scope", "$state", "postItemService", "tagListService",
    function ($scope, $state, postItemService, tagListService) {
        if ($state.params.postAlias) {
            postItemService.get({postAlias: $state.params.postAlias}, function (response) {
                $scope.postEdit = response.content;
            });
        } else {
            $scope.postEdit = {};
            $scope.postEdit.title = "";
            $scope.postEdit.text = "";
            $scope.postEdit.alias = "";
        }

        /**
         * Отправка запроса на создание поста.
         */
        $scope.sendPostEdit = function () {
            postItemService.save($scope.postEdit).$promise.then(function (response) {
                if (response.error.code == 0) {
                    $state.go("main.blog.post", {"postAlias": $scope.postEdit.alias})
                }
            });
        };
    }
]);
