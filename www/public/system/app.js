/**
 *  App Module
 *
 *  Основной модуль - с конфигурациями и настройками
 * 
 * Основные скопы моделей, которые лучше не использовать в модулях формирующих контент
 * $scope.
 *        main - модель с основным для системы содержимым
 *        user - модель с пользовательскими данными
 * 
 * 
 */

/**
 * Общая переменная агрегирующая всем необходимым для системы
 *
 * @type {{system: {}, helpers: {}}}
 */
var chimera = {
    config: {
        baseUrl: "http://www.chimera.rey/_",
        // baseUrl: "http://api.chimera.rey",
        // baseUrl: "/system/responses/",
        auth: ["twitter", "github"],
        test: ""
    },
    system: {},
    helpers: {}
};


chimera.system.main = angular.module("main", [
    "ui.router",
    
    // "twitterApp.services",
    "auth",
    "navigator",

    "catalog",
    "post"
]);

chimera.system.main.factory("sessionRecoverer", ["$q", "$location", function($q, $location) {
    var sessionRecoverer = {
        responseError: function(rejection) {
            console.log("responseError");
            console.log(rejection);

            $location.path("/login");
            $location.replace();

            return $q.reject(rejection);
        },
    };
    return sessionRecoverer;
}]);

chimera.system.main.config(["$stateProvider", "$urlRouterProvider", "$locationProvider", "$httpProvider",
    function ($stateProvider, $urlRouterProvider, $locationProvider, $httpProvider) {
        $httpProvider.interceptors.push("sessionRecoverer");

        // без # в урле
        $locationProvider.html5Mode(true);

        // Роутинг
        // Главная
        $urlRouterProvider.when("/home", "/main/home");
        // Посты
        $urlRouterProvider.when("/post/:aliasPost", "/main/post/:aliasPost");
        // Каталоги
        $urlRouterProvider.when("/catalog/:aliasCatalog", "/main/catalog/:aliasCatalog");
        $urlRouterProvider.when("/catalog/:aliasCatalog/:page", "/main/catalog/:aliasCatalog/:page");

        // Любые неопределенные url перенаправлять на /
        $urlRouterProvider.otherwise("/login");
        // Теперь определим состояния
        $stateProvider
            .state("main", {
                abstract: true,
                url: "/main",

                views: {
                    "": {
                        templateUrl: "/system/templates/main.html",
                        controller: "MainController"
                    },
                    "nav@main": {
                        templateUrl: "/system/templates/nav.html",
                        controller: "NavigatorController"
                    },
                    "catalogs@main": {templateUrl: "/system/templates/catalogs.html"},
                    "tags@main": {templateUrl: "/system/templates/tags.html"},
                    "links@main": {templateUrl: "/system/templates/links.html"}
                }
            })
            // .state("main.home", {
            //     url: "/home/",
            //     views: {
            //         "content": {
            //             templateUrl: "/system/templates/catalog.html",
            //             controller: "CatalogLatestController",
            //         }
            //     }
            // })
            .state("login", {
                url: "/login",
                views: {
                    "": {
                        templateUrl: "/system/templates/login.html",
                        controller: "MainLoginController",
                    }
                }
            })
            .state("main.home", {
                url: "/home",
                views: {
                    "content": {
                        templateUrl: "/system/templates/catalog.html",
                        controller: "MainContentController",
                    }
                }
            })
            .state("main.catalog", {
                url: "/catalog/:aliasCatalog/:page",// {aliasCatalog:([\w-]+)}/{page:([\d+])}
                params: {
                    "aliasCatalog": "latest",
                    "page": "1"
                },
                views: {
                    "content": {
                        templateUrl: "/system/templates/catalog.html",
                        controller: "CatalogPostsController"
                    }
                }
            })
            .state("main.post", {
                url: "/post/:aliasPost", // {alias_post:([\w-]+)}
                views: {
                    "content": {
                        templateUrl: "/system/templates/post.html",
                        controller: "PostController"
                    }
                }
            })

            // NeuronStar - cinema
            // .state("main", {
            //     abstract: true,
            //     url: "/main",

            //     views: {
            //         "": {
            //             templateUrl: "/system/templates/main.html",
            //             controller: "MainController"
            //         },
            //         "nav@main": {
            //             templateUrl: "/system/templates/nav.html",
            //             controller: "NavigatorController"
            //         },
            //         "quote@main": {templateUrl: "/system/templates/quote.html"},
            //         "archives@main": {templateUrl: "/system/templates/archives.html"},
            //         "links@main": {templateUrl: "/system/templates/links.html"}
            //     }
            // })
            // .state("main.home", {
            //     url: "/home",
            //     views: {
            //         "content": {
            //             templateUrl: "/system/templates/catalog.html",
            //             controller: "CatalogLatestController",
            //         }
            //     }
            // })
            // .state("main.catalog", {
            //     url: "/catalog/{aliasCatalog:([\w-]+)}/{page:([\d+])}",
            //     views: {
            //         "content": {
            //             templateUrl: "/system/templates/catalog.html",
            //             controller: "CatalogPostsController"
            //         }
            //     }
            // })
            // .state("main.post", {
            //     url: "/post/:alias_post", // {alias_post:([\w-]+)}
            //     views: {
            //         "content": {
            //             templateUrl: "/system/templates/post.html",
            //             controller: "CatalogPostController"
            //         }
            //     }
            // })

            // MultiCriteria - processor
        ;

    }
]);

chimera.system.main.controller("MainController", ["$scope",
    function ($scope) {
        console.log('MainController');
        $scope.main = {
            "title": "Rey's-ysetm",
            "readMore": "ReadMe...",
            "foo": "BAAAAAR"
        };
    }
]);

chimera.system.main.controller("MainLoginController", ["$scope",
    function ($scope) {
        console.log("MainLoginController");
        $scope.main = {
            "title": "Rey's-ysetm",
            "readMore": "ReadMe...",
            "foo": "BAAAAAR"
        };
    }
]);


chimera.system.main.controller("MainContentController", ["$scope", "$state", "catalogLoader",
    function ($scope, $state, catalogLoader) {

        if(!$state.params.aliasCatalog) {
            $state.params.aliasCatalog = "latest";
        }            

        catalogLoader.get({}, function(response) {
            $scope.catalog = response.content;
            $scope.paging = response.content.pageData;
            $scope.catalog.progress = false;  
        }, function(response) {
            $scope.catalog.progress = false;
        });
    }
]);
