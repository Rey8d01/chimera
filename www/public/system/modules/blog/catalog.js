/**
 * Основной контент это список из постов относящихся к каталогу.
 * CatalogListChildrenHandler
 */

chimera.system.catalog = angular.module("catalog", ["ngResource", "ngSanitize"]);

/**
 * CatalogItemHandler
 */
chimera.system.catalog.controller("CatalogItemHandler", ["$scope", "$state", "catalogItemService",
    function ($scope, $state, catalogItemService) {
        catalogItemService.get({catalogAlias: $state.params.catalogAlias, page: $state.params.page}, function(response) {
            $scope.catalog = response.content;
            $scope.paging = response.content.pageData;
            $scope.catalog.progress = false;
        });
    }
]);

/**
 * CatalogItemHandler
 */
chimera.system.main.controller("CatalogLatestController", ["$scope", "$state", "catalogItemService",
    function ($scope, $state, catalogItemService) {

        if(!$state.params.catalogAlias) {
            $state.params.catalogAlias = "latest";
        }            

        catalogItemService.get({}, function(response) {
            $scope.catalog = response.content;
            $scope.paging = response.content.pageData;
            $scope.catalog.progress = false;  
        }, function(response) {
            $scope.catalog.progress = false;
        });
    }
]);

/**
 * CatalogEditHandler
 */
chimera.system.catalog.controller("CatalogEditController", ["$scope", "$state", "catalogItemService", "catalogListService",
    function ($scope, $state, catalogItemService, catalogListService) {
        var $typeahead = $('.catalog-edit__parent-alias_view.typeahead');

        // Инициализация автокомплита для категорий.
        $typeahead.typeahead({
            source: function (s, cb) {
                $('.catalog-edit__parent-alias_view.typeahead').parent().removeClass("has-error");

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
                $('.catalog-edit__parent-alias_hide').val(item.alias);
            },
            autoSelect: true
        });

        // Отправка запроса на создание поста.
        $scope.catalogEdit = function () {
            var title = $(".catalog-edit__title").text(),
                alias = $(".catalog-edit__alias").text(),
                parentAlias = $(".catalog-edit__parent-alias_hide").val();

            catalogItemService.save({
                "title": title,
                "alias": alias,
                "parentAlias": parentAlias
            });
        };
    }
]);

/**
 * CatalogListMainHandler
 */
chimera.system.catalog.controller("CatalogListMainController", ["$scope", "$state", "catalogListService",
    function ($scope, $state, catalogListService) {
        catalogListService.get({}, function(response) {
            $scope.catalogs = response.content.catalogs;
        });
    }
]);

chimera.system.catalog.factory("catalogItemService", ["$resource",
    function ($resource) {
        return $resource("/catalog/:catalogAlias/:page", {catalogAlias: "latest", page: "1"}, {
            save: {method: "POST", params: {catalogAlias: null, page: null}}
        });
    }
]);

chimera.system.catalog.factory("catalogListService", ["$resource",
    function ($resource) {
        return $resource("/catalogs");
    }
]);