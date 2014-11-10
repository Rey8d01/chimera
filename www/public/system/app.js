/**
 *  App Module
 *
 *  Основной модуль - с конфигурациями и настройками
 */

/**
 * Общая переменная агрегирующая всем необходимым для системы
 *
 * @type {{system: {}, helpers: {}}}
 */
var chimera = {
    config: {
        baseUrl: "http://api.chimera.rey/",
        // baseUrl: "/system/responses/",
        test: ""
    },
    system: {},
    helpers: {}
};

chimera.system.main = angular.module('main', [
    'ui.router',
    'navigator',
    'collection'
//    'blogServices'
]);

chimera.system.main.config(['$stateProvider', '$urlRouterProvider', '$locationProvider',
    function ($stateProvider, $urlRouterProvider, $locationProvider) {
        // без # в урле
        $locationProvider.html5Mode(true);

        // Роутинг
        // Главная
        $urlRouterProvider.when('/home', '/main/home/');
        // Посты
        $urlRouterProvider.when('/post/:slug_post', '/main/post/:slug_post');
        // Коллекции
        $urlRouterProvider.when('/:collection/:slug_collection', '/main/:collection/:slug_collection');

        // Любые неопределенные url перенаправлять на /
        $urlRouterProvider.otherwise("/main/home/");
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
                    "quote@main": {templateUrl: "/system/templates/quote.html"},
                    "archives@main": {templateUrl: "/system/templates/archives.html"},
                    "links@main": {templateUrl: "/system/templates/links.html"}
                }
            })
            .state("main.home", {
                url: "/home/",
                views: {
                    "content": {
                        templateUrl: "/system/templates/collection.html",
                        controller: "CollectionLatestController",
                    }
                }
            })
            .state("main.post", {
                url: "/post/:slug_post",
                views: {
                    "content": {
                        templateUrl: "/system/templates/post.html",
                        controller: 'CollectionPostController'
                    }
                }
            })
            .state("main.collection", {
                url: "/collection/:slug_collection",
                views: {
                    "content": {
                        templateUrl: "/system/templates/collection.html",
                        controller: "CollectionPostsController"
                    }
                }
            })
        ;

    }
]);

chimera.system.main.controller('MainController', ['$scope',
    function ($scope) {
        $scope.main = {
            "title": "The Rey's-ysetm main blog",
            "read_more": "ReadMe...",
            "foo": 'BAAAAAR'
        };
    }
]);


