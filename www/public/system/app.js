/**
 *  App Module
 *
 *  Основной модуль - с конфигурациями и настройками
 * 
 * Основные скопы моделей, которые лучше не использовать в модулях формирующих контент
 * $scope.
 *        main - модель с основным для системы содержимым
 *        user - модель с пользовательскими данными
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
    "post",
    "tag",

    "recommendation",
    "recommendationFake"
]);

/**
 * Перехват входящих/исходящих запросов.
 */
chimera.system.main.factory("sessionRecover", ["$q", "$location", function($q, $location) {
    console.debug("sessionRecover");

    // Общая обработка ошибок.
    var parseError = function(error) {
        switch(error.code) {
            case 11:                
                $location.path("/login").replace();
                break;
            default:
                $.notify(error.message, "error");
                break;
        }
    };

    return {
        /**
         * Роутинг запросов по статике и к системе.
         *
         * @param config
         * @returns {*}
         */
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
        /**
         * Разбор ответов для определения соответствующей реакции на случай возникновения ошибок.
         *
         * @param response
         * @returns {*}
         */
        response: function(response) {
            console.debug("response", response);
            var data = response.data;

            if (data && data.error && data.error.code) {
                parseError(data.error);
            }
            
            return response;
        },
        //requestError: function(rejection) {
        //    console.debug("requestError", rejection);
        //    return $q.reject(rejection);
        //},
        responseError: function(rejection) {
            console.debug("responseError", rejection);
            var data = rejection.data;

            if (data && data.error && data.error.code) {
                parseError(data.error);
            }

            return $q.reject(rejection);
        }
    };
}]);

chimera.system.main.config(["$stateProvider", "$urlRouterProvider", "$locationProvider", "$httpProvider",
    function ($stateProvider, $urlRouterProvider, $locationProvider, $httpProvider) {
        // Перехват всех http запросов для определения ошибок и реакции на них.
        $httpProvider.interceptors.push("sessionRecover");
        // Отправка POST запросов в едином виде.
        //$httpProvider.defaults.headers.post = {"Content-Type": "application/x-www-form-urlencoded"};
        $httpProvider.defaults.headers.post = {"Content-Type": "multipart/form-data"};
        // html5Mode - без # в урле
        $locationProvider.html5Mode({
            enabled: true,
            requireBase: false
        });

        // Дефолтный роутинг
        // Главная блога
        $urlRouterProvider.when("/blog", "/blog/home");
        //// Посты
        //$urlRouterProvider.when("/post/:aliasPost", "/blog/post/:aliasPost");
        //// Каталоги
        //$urlRouterProvider.when("/catalog/:catalogAlias", "/blog/catalog/:catalogAlias");
        //$urlRouterProvider.when("/catalog/:catalogAlias/:page", "/blog/catalog/:catalogAlias/:page");

        // Любые неопределенные url перенаправлять на страницу авторизации (при успешной авторизации произойдет редирект на блог).
        $urlRouterProvider.otherwise("/login");

        // Определение состояний для всего приложения.
        $stateProvider
            /**
             * Форма входа.
             */
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
             * главное меню и основную контентную область.
             */
            .state("main", {
                abstract: true,
                url: "",
                views: {
                    "": {
                        templateUrl: "/system/templates/main.html",
                        controller: "AuthController"
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
                        //controller: "CatalogLatestController"
                    },
                    "catalogs@main.blog": {
                        templateUrl: "/system/templates/blog/catalogs.html",
                        controller: "CatalogListMainController"
                    },
                    "tags@main.blog": {
                        templateUrl: "/system/templates/blog/tags.html",
                        controller: "TagListMainController"
                    },
                    "links@main.blog": {templateUrl: "/system/templates/blog/links.html"}
                }
            })
            /**
             * Главная блога.
             */
            .state("main.blog.home", {
                url: "/home",
                views: {
                    "content": {
                        templateUrl: "/system/templates/blog/catalog.html",
                        controller: "CatalogLatestController"
                    }
                }
            })
            /**
             * Посты в каталоге.
             */
            .state("main.blog.catalog", {
                url: "/catalog/:catalogAlias/:page",
                params: {
                    "catalogAlias": "latest",
                    "page": "1"
                },
                views: {
                    "content": {
                        templateUrl: "/system/templates/blog/catalog.html",
                        controller: "CatalogItemHandler"
                    }
                }
            })
            /**
             * Редактирование поста.
             */
            .state("main.blog.catalogEdit", {
                url: "/catalog",
                views: {
                    "content": {
                        templateUrl: "/system/templates/blog/catalogEdit.html",
                        controller: "CatalogEditController"
                    }
                }
            })
            /**
             * Посты по определенному тегу.
             */
            .state("main.blog.tag", {
                url: "/tag/:tagAlias/:page",
                params: {
                    "page": "1"
                },
                views: {
                    "content": {
                        templateUrl: "/system/templates/blog/tag.html",
                        controller: "TagItemHandler"
                    }
                }
            })
            /**
             * Просмотр поста.
             */
            .state("main.blog.post", {
                url: "/post/:aliasPost",
                views: {
                    "content": {
                        templateUrl: "/system/templates/blog/post.html",
                        controller: "PostController"
                    }
                }
            })
            /**
             * Редактирование поста.
             */
            .state("main.blog.postEdit", {
                url: "/post",
                views: {
                    "content": {
                        templateUrl: "/system/templates/blog/postEdit.html",
                        controller: "PostEditController"
                    }
                }
            })
            /**
             * Главная рекомендаций.
             */
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
