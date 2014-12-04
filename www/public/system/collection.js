/**
 * Модуль управления постами.
 * Отображает посты в виде миниатюр и целиком загруженных материалов.
 */

chimera.system.collection = angular.module("collection", ["ngResource", "ngSanitize"]);

// Контроллеры
chimera.system.collection.controller("CollectionPostsController", ["$scope", "$state", "collectionLoader",
    function ($scope, $state, collectionLoader) {
        collectionLoader.get({slugCollection: $state.params.slugCollection, page: $state.params.page}, function(response) {
            $scope.collection = response.content;
            $scope.paging = response.content.pageData;
            $scope.collection.progress = false;
        });
    }
]);

// chimera.system.collection.controller("CollectionPostController", ["$scope", "$state", "collectionLoader",
//     // Для этого может  стоит сделать отдельный модуль
//     function ($scope, $state, collectionLoader) {
//         collectionLoader.getPost({slugCollection: $state.params.slug_post}, function(response) {
//             $scope.post = response.content
//             // $scope.post.progress = false;
//         });
//     }
// ]);

// Сервис
chimera.system.collection.factory("collectionLoader", ["$resource",
    function ($resource) {
        return $resource(chimera.config.baseUrl + "/collection/:slugCollection/:page", {slugCollection: "latest", page: "1"}, {
            // getPost: {method: "GET", params: {source: "post"}}
        });
    }]);
