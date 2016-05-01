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
        baseUrl: "https://chimera.rey/_",
        baseWWWUrl: "https://chimera.rey",
        // baseUrl: "/system/responses/",
        auth: ["manual", "twitter", "github"],
        debug: true,
        test: ""
    },
    system: {},
    helpers: {
        sleep: function(ms) {
            ms += new Date().getTime();
            while (new Date() < ms) {
            }
        },
        log: function() {
            if (chimera.config.debug) {
                console.log(arguments)
            }
        },
        debug: function() {
            if (chimera.config.debug) {
                console.debug(arguments)
            }
        }
    }
};


chimera.system.main = angular.module("main", [
    "ui.router",

    "user",
    "blog",
//    "recommendation",
]);

/**
 * Перехват входящих/исходящих запросов.
 */
chimera.system.main.factory("sessionRecover", ["$q", "$location", function($q, $location) {
    chimera.helpers.debug("sessionRecover");

    // Общая обработка ошибок.
    var parseError = function (error) {
        switch (error.code) {
            case 11:
                $.notify(error.message, "error");
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
        $httpProvider.defaults.headers.post = {"Content-Type": "application/x-www-form-urlencoded"};
//        $httpProvider.defaults.headers.post = {"Content-Type": "multipart/form-data"};
        // html5Mode - без # в урле
        $locationProvider.html5Mode({
            enabled: true,
            requireBase: false
        });

        // Дефолтный роутинг
        // Главная блога
        $urlRouterProvider.when("/blog", "/blog/home");

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
                        templateUrl: "/app/user/login.html",
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
                        templateUrl: "/app/main.html",
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
                        templateUrl: "/app/blog/blog.html",
                        //controller: "CatalogLatestController"
                    },
                    "tags@main.blog": {
                        templateUrl: "/app/blog/side/tag-list.html",
                        controller: "TagListController"
                    },
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
                        templateUrl: "/app/blog/content/post-list.html",
                        controller: "PostListController"
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
                        templateUrl: "/app/blog/content/author.html",
                        controller: "AuthorController"
                    },
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
                        templateUrl: "/app/blog/content/tag-item.html",
                        controller: "TagItemController"
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
                        templateUrl: "/app/blog/content/post-item.html",
                        controller: "PostItemController"
                    }
                }
            })
            /**
             * Редактирование поста.
             */
            .state("main.blog.postEdit", {
                url: "/post",
                params: {
                    "postAlias": null
                },
                views: {
                    "content": {
                        templateUrl: "/app/blog/content/post-edit.html",
                        controller: "PostEditController"
                    }
                }
            })
            /**
             * Главная рекомендаций.
             */
            //.state("main.recommendation", {
            //    url: "/recommendation",
            //    views: {
            //        "container": {
            //            templateUrl: "/system/templates/recommendation/index.html",
            //            controller: "RecommendationController"
            //        }
            //    }
            //})
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
