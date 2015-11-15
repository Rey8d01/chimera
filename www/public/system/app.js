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
 * Общий объект системы
 */
var chimera = {
    config: {
        baseUrl: "http://api.chimera.rey/_", // baseApiUrl
        baseWWWUrl: "http://www.chimera.rey",
        // baseUrl: "/system/responses/",
        auth: ["manual", "twitter", "github"],
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

    "recommendation",
    "recommendationFake"
]);

chimera.system.main.factory("sessionRecover", ["$q", "$location", function($q, $location) {
    // Перехват запросов
    console.debug("sessionRecover");
    return {
        // Роутинг запросов по статике и к системе
        request: function(config) {
            console.debug("request", config);
            if (/.*\.(js|css|ico|htm|html|json)/.test(config.url)) {
                // Запросы по статик файлам переадресуются на основной домен.
                config.url = chimera.config.baseWWWUrl + config.url;
            } else {
                // Запросы не относящиея к статик файлам идут к основной системе.
                config.url = chimera.config.baseUrl + config.url;
            }
            return config;
        },
        // Разбор ответов для определения соответствующей реакции на случай возникновения ошибок.
        response: function(response) {
            console.debug("response", response);
            var data = response.data;

            if (data && data.error) {
                switch(data.error){
                    case 11:                
                        $location.path("/login").replace();
                        break;
                    default:
                        break;
                }
            }
            
            return response;
        },
        //requestError: function(rejection) {
        //    console.debug("requestError", rejection);
        //    return $q.reject(rejection);
        //},
        responseError: function(rejection) {
            console.debug("responseError", rejection);
            // Для неавторизованного пользователя
            if (rejection.status == 401) {
                $location.path("/login");
                $location.replace();
            }

            return $q.reject(rejection);
        }
    };
}]);

chimera.system.main.config(["$stateProvider", "$urlRouterProvider", "$locationProvider", "$httpProvider",
    function ($stateProvider, $urlRouterProvider, $locationProvider, $httpProvider) {
        // Перехват всех http запросов для определения ошибок и реакции на них.
        $httpProvider.interceptors.push("sessionRecover");
        // Отправка запросов в едином виде
//        $httpProvider.defaults.headers.post = {"Content-Type": "application/x-www-form-urlencoded"};
        $httpProvider.defaults.headers.post = {"Content-Type": "multipart/form-data"};

        // без # в урле
        $locationProvider.html5Mode({
            enabled: true,
            requireBase: false
        });

        // Роутинг
        // Главная блога
        $urlRouterProvider.when("/blog", "/blog/home");
        //// Посты
        //$urlRouterProvider.when("/post/:aliasPost", "/blog/post/:aliasPost");
        //// Каталоги
        //$urlRouterProvider.when("/catalog/:aliasCatalog", "/blog/catalog/:aliasCatalog");
        //$urlRouterProvider.when("/catalog/:aliasCatalog/:page", "/blog/catalog/:aliasCatalog/:page");

        // Любые неопределенные url перенаправлять на страницу авторизации
        // (в рамках которой, при успешной авторизации будет редирект на блог)
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
            /**
             * Главное абстрактное состояние для системы. Включает в себя компоненты авторизованного пользователя,
             * главное меню и основную контентную область
             */
            .state("main", {
                abstract: true,
                url: "",

                views: {
                    "": {
                        templateUrl: "/system/templates/main.html",
                        controller: "CatalogLatestController"
                    }
                }
            })
            /**
             * Абстрактное состояние блога. Наследуется от главного абстрактного состояния
             * и заполняет основную контентную область блоговым контентом.
             */
            .state("main.blog", {
                abstract: true,
                url: "/blog",

                views: {
                    "container@main": {
                        templateUrl: "/system/templates/blog/blog.html",
                        controller: "CatalogLatestController"
                    },
                    "catalogs@main.blog": {
                        templateUrl: "/system/templates/blog/catalogs.html",
                        controller: "CatalogsMenuController"
                    },
                    "tags@main.blog": {templateUrl: "/system/templates/blog/tags.html"},
                    "links@main.blog": {templateUrl: "/system/templates/blog/links.html"}
                }
            })
            // Главная блога
            .state("main.blog.home", {
                url: "/home",
                views: {
                    "content": {
                        templateUrl: "/system/templates/blog/catalog.html",
                        controller: "CatalogLatestController"
                    }
                }
            })
            // Посты в каталоге
            .state("main.blog.catalog", {
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
            .state("main.blog.post", {
                url: "/post/:aliasPost",
                views: {
                    "content": {
                        templateUrl: "/system/templates/blog/post.html",
                        controller: "PostController"
                    }
                }
            })
            // Просмотр поста
            .state("main.blog.addNewPost", {
                url: "/addNewPost",
                views: {
                    "content": {
                        templateUrl: "/system/templates/blog/addNewPost.html",
                        controller: "AddNewPostController"
                    }
                }
            })
            /**
             * Главная рекомендаций
             *
             */
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
            .state("main.recommendationFake", {
                url: "/recommendationFake",
                views: {
                    "content": {
                        templateUrl: "/system/templates/recommendation/fake/index.html",
                        controller: "RecommendationFakeController"
                    }
                }
            })

            // MultiCriteria - processor
        ;

    }
]);

