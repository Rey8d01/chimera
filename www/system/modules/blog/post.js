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

        $scope.editPost = function () {
            $state.go("main.blog.postEdit", {postAlias: $state.params.postAlias})
        }

        $scope.deletePost = function () {
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
chimera.system.post.controller("PostEditController", ["$scope", "$state", "postService", "postEditService", "tagListService",
    function ($scope, $state, postService, postEditService, tagListService) {
        var $typeaheadCatalogAlias = $('.post-edit__catalog-alias_view.typeahead'),
            $typeaheadTags = $('.post-edit__tags.typeahead'),
            tags = [];

        if ($state.params.postAlias) {
            postService.get({postAlias: $state.params.postAlias}, function (response) {
                $scope.postEdit = response.content;
            });
        } else {
            $scope.postEdit = {};
            $scope.postEdit.title = "";
            $scope.postEdit.text = "";
            $scope.postEdit.alias = "";
            $scope.postEdit.catalogAlias = "";
            $scope.postEdit.tags = [];
        }

        /**
         * Источником данных для выпадающего списка будет результат отправки запроса на получение всех тегов.
         *
         * todo вывести в source для удаленного поиска
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
            source: function (request, response) {
                var resultSearch = [];
                for (var tag in tags) {
                    if (tags[tag].title.toLowerCase().search(request.trim().toLowerCase()) + 1) {
                        resultSearch.push({
                            "alias": tags[tag].alias,
                            "name": tags[tag].title,
                            "title": tags[tag].title
                        });
                    }
                }

                // Добавление нового тега
                if (_.isEmpty(resultSearch)) {
                    resultSearch.push({
                        "alias": "",
                        "name": "Новый тег: " + request,
                        "title": request
                    });
                }
                response(resultSearch);
            },
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
            postEditService.save($scope.postEdit).$promise.then(function (response) {
                if (response.error.code == 0) {
                    $state.go("main.blog.post", {"postAlias": $scope.postEdit.alias})
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

chimera.system.post.factory("postEditService", ["$resource",
    function ($resource) {
        return $resource("/post-edit/:postAlias", {postAlias: null}, {
            save: {method: "POST", params: {postAlias: null}}
        });
    }
]);
