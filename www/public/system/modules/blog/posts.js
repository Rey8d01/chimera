/**
 * Основной контент это текст поста
 */

chimera.system.post = angular.module("post", ["ngResource", "ngSanitize"]);

chimera.system.post.controller("PostController", ["$scope", "$state", "postService",
    function ($scope, $state, postService) {
        // Запрос определенного поста
        postService.get({aliasPost: $state.params.aliasPost}, function (response) {
            $scope.post = response.content;
        });
    }
]);

chimera.system.post.controller("NewPostController", ["$scope", "$state", "postService", "catalogsService",
    function ($scope, $state, postService, catalogsService) {
        var $typeahead = $('.new-post__catalog-alias.typeahead');

        // Инициализация автокомплита для категорий.
        $typeahead.typeahead({
            source: function (s, cb) {
                $('.new-post__catalog-alias.typeahead').parent().removeClass("has-error");

                //omdbapiService.search({s:s}, function (response) {
                catalogsService.get({}, function (response) {
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
            //afterSelect: function (item) {
            //    $scope.selectItem.imdb = item.imdb;
            //    $scope.selectItem.year = item.year;
            //    $scope.selectItem.title = item.title;
            //},
            autoSelect: true
        });

        $scope.newPost = function () {
            var title = $(".blog-post-title").html(),
                text = $(".blog-post-text").html(),
                tags = $(".blog-post-tags").text(),
                alias = $(".blog-post-alias").text(),
                catalogAlias = $(".blog-post-catalogAlias").text();

            postService.save({
                "title": title,
                "text": text,
                "alias": alias
            });
        };
    }
]);

chimera.system.post.factory("postService", ["$resource",
    function ($resource) {
        return $resource("/post/:aliasPost");
    }
]);
