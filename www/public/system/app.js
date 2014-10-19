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
    system: {},
    helpers: {}
};

chimera.system.main = angular.module('main', [
    'ui.router',
    'navigator',
    'posts'
//    'blogServices'
]);

chimera.system.main.config(['$stateProvider', '$urlRouterProvider', '$locationProvider',
    function ($stateProvider, $urlRouterProvider, $locationProvider) {
        // без #
//        $locationProvider.html5Mode(true);

        // Роутинг
        // Главная
        $urlRouterProvider.when('/home', '/main/home/');
        // Посты
        $urlRouterProvider.when('/post/:id', '/main/post/:id');
        // Коллекции
        $urlRouterProvider.when('/:collection/:id', '/main/:collection/:id');

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
                        controller: "LatestPostsController"
                    }
                }
            })
            .state("main.post", {
                url: "/post/:id",
                views: {
                    "content": {
                        templateUrl: "/system/templates/post.html",
                        controller: 'PostController'
                    }
                }
            })
            .state("main.collection", {
                url: "/collection/:slug",
                views: {
                    "content": {
                        templateUrl: "/system/templates/collection.html",
                        controller: "PostsInCollectionController"
                    }
                }
            })
        ;

    }
]);

chimera.system.main.controller('MainController', ['$scope',
    function ($scope) {
        $scope.main = {
            'title': "The Rey's-ysetm main blog",
            "readMore": "ReadMe...",
            'foo': 'BAAAAAR'
        };
    }
]);


