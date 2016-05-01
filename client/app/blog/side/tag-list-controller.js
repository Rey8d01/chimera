chimera.system.blog.controller("TagListController", ["$scope", "$state", "tagListService",
    function ($scope, $state, tagListService) {
        tagListService.get({}, function(response) {
            $scope.tags = response.content.tags;
        });
    }
]);
