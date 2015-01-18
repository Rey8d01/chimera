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
    
    "auth",
    // "navigator",

    "catalog",
    "catalogs",
    "post",

    "recommendation"
]);

chimera.system.main.factory("sessionRecoverer", ["$q", "$location", function($q, $location) {
    var sessionRecoverer = {
        responseError: function(rejection) {
            console.log("responseError");
            console.log(rejection);
            if (rejection.status == 403) {
                $location.path("/login");
                $location.replace();
            }

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
            // Форма входа
            .state("login", {
                url: "/login",
                views: {
                    "": {
                        templateUrl: "/system/templates/login.html",
                        controller: "AuthController"
                    }
                }
            })
            // Главное абстрактное состояние
            .state("main", {
                abstract: true,
                url: "/main",

                views: {
                    "": {
                        templateUrl: "/system/templates/main.html",
                        controller: "AuthController"
                    },
                    "catalogs@main": {
                        templateUrl: "/system/templates/blog/catalogs.html",
                        controller: "CatalogsMenuController"
                    },
                    "tags@main": {templateUrl: "/system/templates/blog/tags.html"},
                    "links@main": {templateUrl: "/system/templates/blog/links.html"}
                }
            })
            // Главная блога
            .state("main.home", {
                url: "/home",
                views: {
                    "content": {
                        templateUrl: "/system/templates/blog/catalog.html",
                        controller: "CatalogLatestController"
                    }
                }
            })
            // Посты в каталоге
            .state("main.catalog", {
                url: "/catalog/:aliasCatalog/:page",
                params: {
                    "aliasCatalog": "latest",
                    "page": "1"
                },
                views: {
                    "content": {
                        templateUrl: "/system/templates/blog/catalog.html",
                        controller: "CatalogPostsController"
                    }
                }
            })
            // Просмотр поста
            .state("main.post", {
                url: "/post/:aliasPost",
                views: {
                    "content": {
                        templateUrl: "/system/templates/blog/post.html",
                        controller: "PostController"
                    }
                }
            })

            // recommendation movies
            .state("main.recommendation", {
                url: "/recommendation",
                views: {
                    "content": {
                        templateUrl: "/system/templates/recommendation/index.html",
                        controller: "RecommendationController"
                    }
                }
            })


            // MultiCriteria - processor
        ;

    }
]);

