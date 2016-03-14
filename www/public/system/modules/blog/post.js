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
        postService.get({postAlias: $state.params.postAlias}, function (response) {
            $scope.post = response.content;
        });

        $scope.deletePost = function() {
            postService.delete({postAlias: $state.params.postAlias}).$promise.then(function (response) {
                if (response.error.code == 0) {
                    $state.go("main.blog.home")
                }
            });
        }
    }
]);

/**
 * PostEditHandler
 */
chimera.system.post.controller("PostEditController", ["$scope", "$state", "postService", "catalogListService", "tagListService",
    function ($scope, $state, postService, catalogListService, tagListService) {
        var $typeaheadCatalogAlias = $('.post-edit__catalog-alias_view.typeahead'),
            $typeaheadTags = $('.post-edit__tags.typeahead'),
            tags = [];

        $scope.postEdit = {};
        $scope.postEdit.title = "";
        $scope.postEdit.text = "";
        $scope.postEdit.alias = "";
        $scope.postEdit.catalogAlias = "";
        $scope.postEdit.tags = [];

        // Инициализация автокомплита для категорий.
        $typeaheadCatalogAlias.typeahead({
            /**
             * Источником данных для выпадающего списка будет результат отправки запроса на получение всех каталогов.
             */
            source: function (s, cb) {
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
            minLength: 3,
            /**
             * При выборе каталога запоминаем его псевдоним.
             */
            afterSelect: function (item) {
                $scope.postEdit.catalogAlias = item.alias;
            },
            autoSelect: true
        });

        /**
         * Источником данных для выпадающего списка будет результат отправки запроса на получение всех тегов.
         */
        tagListService.get({}, function (response) {
            for (var item in response.content.tags) {
                tag = response.content.tags[item];
                tag.name = tag.title;
                tags.push(tag);
            }
        });
        // Инициализация автокомплита для тегов.
        $typeaheadTags.typeahead({
            source: tags,
            minLength: 2,
            /**
             * При выборе тега он помещается в скоп для отображения и последующей отправки.
             */
            afterSelect: function (item) {
                if ($scope.postEdit.tags.indexOf(item) == -1) {
                    $scope.postEdit.tags.push(item);
                    $scope.$apply();
                }
                $typeaheadTags.val('');
            },
            autoSelect: true
        });

        /**
         * Удаление определенного тега.
         */
        $scope.deleteTag = function (tag) {
            $scope.postEdit.tags = _.without($scope.postEdit.tags, tag);
        };

        /**
         * Отправка запроса на создание поста.
         */
        $scope.sendPostEdit = function () {
            postService.save($scope.postEdit).$promise.then(function (response) {
                if (response.error.code == 0) {
                    $state.go("main.blog.post", {"postAlias":$scope.postEdit.alias})
                }
            });
        };
    }
]);

chimera.system.post.factory("postService", ["$resource",
    function ($resource) {
        return $resource("/post/:postAlias");
    }
]);
