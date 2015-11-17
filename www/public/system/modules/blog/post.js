/**
 * Основной контент это текст поста
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
            source: function (s, cb) {
                $('.post-edit__catalog-alias_view.typeahead').parent().removeClass("has-error");

                //omdbapiService.search({s:s}, function (response) {
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
            afterSelect: function (item) {
                $('.post-edit__catalog-alias_hide').val(item.alias);
            },
            autoSelect: true
        });

        // Отправка запроса на создание поста.
        $scope.postEdit = function () {
            var title = $(".post-edit__title").text(),
                text = $(".post-edit__text").html(),
                alias = $(".post-edit__alias").text(),
                tags = $(".post-edit__tags").text(),
                catalogAlias = $(".post-edit__catalog-alias_hide").val(),
                data;

            data = {
                "title": title,
                "text": text,
                "alias": alias,
                "catalogAlias": catalogAlias,
            };

            // console.info(data);

            postService.save(data);
        };
    }
]);

chimera.system.post.factory("postService", ["$resource",
    function ($resource) {
        return $resource("/post/:aliasPost");
    }
]);
