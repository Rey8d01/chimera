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
        $scope.main.blogContentLoad = true;
        catalogItemService.get({catalogAlias: $state.params.catalogAlias, page: $state.params.page}, function (response) {
            $scope.catalog = response.content;
            //$scope.posts = response.content.posts;
            //$scope.paging = response.content.pageData;
            $scope.main.blogContentLoad = false;
        });
    }
]);

/**
 * CatalogItemHandler
 */
chimera.system.catalog.controller("CatalogLatestController", ["$scope", "$state", "catalogItemService",
    function ($scope, $state, catalogItemService) {
        $scope.main.blogContentLoad = true;

        if (!$state.params.catalogAlias) {
            $state.params.catalogAlias = "latest";
        }

        catalogItemService.get({}, function (response) {
            $scope.catalog = response.content;
            //$scope.paging = response.content.pageData;
            $scope.main.blogContentLoad = false;
        }, function (response) {
            $scope.main.blogContentLoad = false;
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
            /**
             * При выборе каталога запоминаем его псевдоним.
             */
            afterSelect: function (item) {
                $scope.catalogEdit.alias = item.alias;
            },
            autoSelect: true
        });

        // Отправка запроса на создание поста.
        $scope.sendCatalogEdit = function () {
            catalogItemService.save($scope.catalogEdit).$promise.then(function (response) {
                if (response.error.code == 0) {
                    $state.go("main.blog.catalog", {"catalogAlias":$scope.catalogEdit.alias});
                }
            });
        };
    }
]);

/**
 * CatalogListMainHandler
 */
chimera.system.catalog.controller("CatalogListMainController", ["$scope", "$state", "catalogListService",
    function ($scope, $state, catalogListService) {
        catalogListService.get({}, function (response) {
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