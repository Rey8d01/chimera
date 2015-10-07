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

chimera.system.post.controller("AddNewPostController", ["$scope", "$state", "postService", "catalogsService",
    function ($scope, $state, postService, catalogsService) {

        var $input = $('.typeahead');

        // Инициализация автокомплита для категорий
        $input.typeahead({
            source: function (s, cb) {

                catalogsService.get({}, function(response) {
                    $scope.catalogs = response.content.catalogs;

                    console.log($scope.catalogs);
                });


                //var matches = [];
                //$('.typeahead').parent().removeClass("has-error");
                //
                //omdbapiService.search({s:s}, function (response) {
                //    if(response.Error) {
                //        $('.typeahead').parent().addClass("has-error");
                //    } else {
                //        for(var item in response.Search) {
                //            matches.push({
                //                imdb: response.Search[item].imdbID,
                //                year: response.Search[item].Year,
                //                title: response.Search[item].Title,
                //                name: response.Search[item].Title
                //            });
                //        }
                //    }
                //
                //    cb(matches);
                //});

            },
            afterSelect: function (item) {
                $scope.selectItem.imdb = item.imdb;
                $scope.selectItem.year = item.year;
                $scope.selectItem.title = item.title;
            },
            autoSelect: true
        });

        $scope.addNewPost = function () {
            var title = $(".blog-post-title").html(),
                text = $(".blog-post-text").html(),
                tags = $(".blog-post-tags").text(),
                alias = $(".blog-post-alias").text(),
                aliasCatalog = $(".blog-post-aliasCatalog").text();

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
        return $resource(chimera.config.baseUrl + "/post/:aliasPost");
    }
]);
