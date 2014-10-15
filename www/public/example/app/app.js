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

chimera.system.blog = angular.module('blog', [
    'ui.router',
    'navigator',
    'posts'
//    'blogServices'
]);

chimera.system.blog.config(['$stateProvider', '$urlRouterProvider', '$locationProvider',
    function ($stateProvider, $urlRouterProvider, $locationProvider) {
        // без #
        $locationProvider.html5Mode(true);

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
                        templateUrl: "/example/app/templates/main.html",
                        controller: "MainController"
                    },
                    "nav@main": {
                        templateUrl: "/example/app/templates/nav.html",
                        controller: "NavigatorController"
                    },
                    "quote@main": {templateUrl: "/example/app/templates/quote.html"},
                    "archives@main": {templateUrl: "/example/app/templates/archives.html"},
                    "links@main": {templateUrl: "/example/app/templates/links.html"}
                }
            })
            .state("main.home", {
                url: "/home/",
                views: {
                    "content": {
                        templateUrl: "/example/app/templates/collection.html",
                        controller: "LatestPostsController"
                    }
                }
            })
            .state("main.post", {
                url: "/post/:id",
                views: {
                    "content": {
                        templateUrl: "/example/app/templates/post.html",
                        controller: 'PostController'
                    }
                }
            })
            .state("main.collection", {
                url: "/collection/:slug",
                views: {
                    "content": {
                        templateUrl: "/example/app/templates/collection.html",
                        controller: "PostsInCollectionController"
                    }
                }
            })
        ;

    }
]);

chimera.system.blog.controller('MainController', ['$scope',
    function ($scope) {
        $scope.blog = {
            'title': "The Rey's-ysetm Blog",
            "readMore": "ReadMe...",
            'foo': 'BAAAAAR'
        };
    }
]);