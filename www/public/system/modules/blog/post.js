/**
 * Основной контент это текст поста.
 */

chimera.system.post = angular.module("post", ["ngResource", "ngSanitize"]);

/**
 * PostHandler
 */
chimera.system.post.controller("PostController", ["$scope", "$state", "postService",
    function ($scope, $state, postService) {
        // Запрос определенного поста
        postService.get({aliasPost: $state.params.aliasPost}, function (response) {
            $scope.post = response.content;
        });
    }
]);

/**
 * PostEditHandler
 */
chimera.system.post.controller("PostEditController", ["$scope", "$state", "postService", "catalogListService",
    function ($scope, $state, postService, catalogListService) {
        var $typeahead = $('.post-edit__catalog-alias_view.typeahead');

        // Инициализация автокомплита для категорий.
        $typeahead.typeahead({
            /**
             * Источником данных для выпадающего списка будет результат отправки запроса на получение всех каталогов.
             */
            source: function (s, cb) {
                $('.post-edit__catalog-alias_view.typeahead').parent().removeClass("has-error");

                // todo передавать паттерн поиска в запрос и искать на сервере
                catalogListService.get({}, function (response) {
                    var matches = [],
                        catalog = null;
                    for (var item in response.content.catalogs) {
                        catalog = response.content.catalogs[item];
                        catalog.name = catalog.title;
                        matches.push(catalog);
                    }
                    cb(matches);
                });
            },
            /**
             * При выборе каталога запоминаем его псевдоним.
             */
            afterSelect: function (item) {
                $scope.postEdit.catalogAlias = item.alias
            },
            autoSelect: true
        });

        /**
         * Отправка запроса на создание поста.
         */
        $scope.sendPostEdit = function () {
            postService.save($scope.postEdit).$promise.then(function (response) {
                if (response.error.code == 0) {
                    $state.go("main.blog.post", {"aliasPost":$scope.postEdit.alias})
                }
            });
        };
    }
]);

chimera.system.post.factory("postService", ["$resource",
    function ($resource) {
        return $resource("/post/:aliasPost");
    }
]);
