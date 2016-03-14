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
        debug: true,
        test: ""
    },
    system: {},
    helpers: {}
};


chimera.system.main = angular.module("main", [
    "ui.router",
    
    "auth",
    "user",
    // "navigator",

    "author",
    "catalog",
    "post",
    "tag",

    "recommendation",
]);

/**
 * Перехват входящих/исходящих запросов.
 */
chimera.system.main.factory("sessionRecover", ["$q", "$location", function($q, $location) {
    chimera.helpers.debug("sessionRecover");

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
            chimera.helpers.debug("request", config);

            if (!s.startsWith(config.url, "//")) {
                // Внешние запросы остаются без модификаций.
                if (/.*\.(js|css|ico|htm|html|json)/.test(config.url)) {
                    // Запросы по статик файлам переадресуются на основной домен.
                    config.url = chimera.config.baseWWWUrl + config.url;
                } else {
                    // Запросы не относящиея к статик файлам идут к основной системе.
                    config.url = chimera.config.baseUrl + config.url;
                }
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
            chimera.helpers.debug("response", response);
            var data = response.data;

            if (data && data.error && data.error.code) {
                parseError(data.error);
            }
            
            return response;
        },
        responseError: function(rejection) {
            chimera.helpers.debug("responseError", rejection);
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
        //$urlRouterProvider.when("/post/:postAlias", "/blog/post/:postAlias");
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
                        controller: "ChimeraController"
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
                        templateUrl: "/system/templates/blog/index.html",
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
                params: {
                    "catalogAlias": "latest",
                    "page": "1"
                },
                views: {
                    "content": {
                        templateUrl: "/system/templates/blog/content/catalog.html",
                        controller: "CatalogItemHandler"
                    }
                }
            })
            /**
             * Посты в каталоге.
             */
            .state("main.blog.author", {
                url: "/author/:userId/:page",
                params: {
                    "page": "1"
                },
                views: {
                    "content": {
                        templateUrl: "/system/templates/blog/content/author.html",
                        controller: "AuthorHandler"
                    },
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
                        templateUrl: "/system/templates/blog/content/catalog.html",
                        controller: "CatalogItemHandler"
                    },
                }
            })
            /**
             * Редактирование поста.
             */
            .state("main.blog.catalogEdit", {
                url: "/catalog",
                views: {
                    "content": {
                        templateUrl: "/system/templates/blog/content/catalogEdit.html",
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
                        templateUrl: "/system/templates/blog/content/tag.html",
                        controller: "TagItemHandler"
                    }
                },
            })
            /**
             * Просмотр поста.
             */
            .state("main.blog.post", {
                url: "/post/:postAlias",
                views: {
                    "content": {
                        templateUrl: "/system/templates/blog/content/post.html",
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
                        templateUrl: "/system/templates/blog/content/postEdit.html",
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
                    "container": {
                        templateUrl: "/system/templates/recommendation/index.html",
                        controller: "RecommendationController"
                    }
                }
            })
            //.state("main.recommendationFake", {
            //    url: "/recommendationFake",
            //    views: {
            //        "container": {
            //            templateUrl: "/system/templates/recommendation/fake/index.html",
            //            controller: "RecommendationFakeController"
            //        }
            //    }
            //})
            // MultiCriteria - processor
        ;

    }
]);


chimera.system.main.controller("ChimeraController", ["$scope", "$q", "authService", "userMeService",
    function($scope, $q, authService, userMeService) {
        authService.initialize();
        if (!authService.isReady()) {
            chimera.helpers.debug("ChimeraController", 'auth!');
        }

        $scope.main = {
            "title": "Rey's-ysetm",
            "readMore": "ReadMe...",
            "blogContentLoad": false,
            "foo": "BAAAAAR"
        };
        $scope.user = {
            system: null,
            social: null
        };

        // Отложенная запись в скоп всех запрашиваемых данных.
        authService.getMeData().then(function(data) {
            $scope.user.social = data;
        });

        userMeService.get(function(response) {
            $scope.user.system = response.content;
        });

        $scope.signOut = function() {
            authService.disconnect();
            $(".sign-in-button").fadeIn();
            $(".sign-out-button").fadeOut();
        };

    }
]);
