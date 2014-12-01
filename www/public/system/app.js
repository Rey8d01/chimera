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
        baseUrl: "http://api.chimera.rey",
        // baseUrl: "/system/responses/",
        test: ""
    },
    system: {},
    helpers: {}
};

chimera.system.main = angular.module('main', [
    'ui.router',
    'navigator',
    'collection',
    'post'
]);

chimera.system.main.config(['$stateProvider', '$urlRouterProvider', '$locationProvider',
    function ($stateProvider, $urlRouterProvider, $locationProvider) {
        // без # в урле
        $locationProvider.html5Mode(true);

        // Роутинг
        // Главная
        $urlRouterProvider.when('/home', '/main/home/');
        // Посты
        $urlRouterProvider.when('/post/:slugPost', '/main/post/:slugPost');
        // Коллекции
        $urlRouterProvider.when('/collection/:slugCollection', '/main/collection/:slug_collection');
        $urlRouterProvider.when('/collection/:slugCollection/:page', '/main/collection/:slug_collection/:page');

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
            // .state("main.home", {
            //     url: "/home/",
            //     views: {
            //         "content": {
            //             templateUrl: "/system/templates/collection.html",
            //             controller: "CollectionLatestController",
            //         }
            //     }
            // })
            .state("main.home", {
                url: "/home/",
                views: {
                    "content": {
                        templateUrl: "/system/templates/collection.html",
                        controller: "MainContentController",
                    }
                }
            })
            .state("main.collection", {
                url: "/collection/:slugCollection/:page",// {slug_collection:([\w-]+)}/{page:([\d+])}
                params: {
                    "slugCollection": 'latest',
                    "page": '1'
                },
                views: {
                    "content": {
                        templateUrl: "/system/templates/collection.html",
                        controller: "CollectionPostsController"
                    }
                }
            })
            .state("main.post", {
                url: "/post/:slugPost", // {slug_post:([\w-]+)}
                views: {
                    "content": {
                        templateUrl: "/system/templates/post.html",
                        controller: 'PostController'
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
            //     url: "/home/",
            //     views: {
            //         "content": {
            //             templateUrl: "/system/templates/collection.html",
            //             controller: "CollectionLatestController",
            //         }
            //     }
            // })
            // .state("main.collection", {
            //     url: "/collection/{slug_collection:([\w-]+)}/{page:([\d+])}",
            //     views: {
            //         "content": {
            //             templateUrl: "/system/templates/collection.html",
            //             controller: "CollectionPostsController"
            //         }
            //     }
            // })
            // .state("main.post", {
            //     url: "/post/:slug_post", // {slug_post:([\w-]+)}
            //     views: {
            //         "content": {
            //             templateUrl: "/system/templates/post.html",
            //             controller: 'CollectionPostController'
            //         }
            //     }
            // })

            // MultiCriteria - processor
        ;

    }
]);

chimera.system.main.controller("MainController", ["$scope",
    function ($scope) {
        $scope.main = {
            "title": "The Rey's-ysetm main blog",
            "readMore": "ReadMe...",
            "foo": 'BAAAAAR'
        };
    }
]);


chimera.system.main.controller("MainContentController", ["$scope", "$state", "collectionLoader",
    function ($scope, $state, collectionLoader) {

        if(!$state.params.slugCollection) {
            $state.params.slugCollection = "latest";
        }            

        collectionLoader.get({}, function(response) {
            $scope.collection = response.content;
            $scope.paging = response.content.pageData;
            $scope.collection.progress = false;  
        }, function(response) {
            $scope.collection.progress = false;
        });
    }
]);

// chimera.system.main.directive('collectionPagination', function () {
//     return {
//         compile: function compile(temaplateElement, templateAttrs) {
//             console.log(templateAttrs);
//             // templateElement.prepend("<div>{{"+templateAttrs.habraHabrWork+"}}"+templateAttrs.habra+"</div>");
//             return {
//                 pre: function ($scope, element, attrs) {
//                     console.log(6);
//                 },
//                 post: function($scope, element, attrs) { 
//                     console.log(5);
//                 }
//             }
//         },
//         template: '<div><span ></span></div>',
//         // templateUrl: 'template.html',
//         restrict: 'EA',
//         scope: true,     
//     };
// });


// chimera.system.main.directive('uiPagination', function () {
//         return {
//             restrict: 'EA',
//             replace: true,
//             template:
//                 '<div class="pagination pagination-large pagination-centered">' +
//                     '<ul>' +
//                         '<li ng-class="{disabled: firstPage()}" ng-click="goToFirstPage()">' +
//                             '<a><i class="icon-step-backward"></i></a>' +
//                         '</li>' +
//                         '<li ng-class="{disabled: !hasPrev()}" ng-click="prev()">' +
//                             '<a><i class="icon-caret-left"></i></a>' +
//                         '</li>' +
//                         '<li ng-repeat="page in pages"' +
//                             'ng-class="{active: isCurrent(page)}"' +
//                             'ng-click="setCurrent(page)"' +
//                         '>' +
//                             '<a>{{page}}</a>' +
//                         '</li>' +
//                         '<li ng-class="{disabled: !hasNext()}" ng-click="next()">' +
//                             '<a><i class="icon-caret-right"></i></a>' +
//                         '</li>' +
//                         '<li ng-class="{disabled: lastPage()}" ng-click="goToLastPage()">' +
//                             '<a><i class="icon-step-forward"></i></a>' +
//                         '</li>' +
//                     '</ul>' +
//                     '</div>',
//             scope: {
//                 cur: '=',
//                 total: '=',
//                 display: '@'
//             },
//             link: function (scope, element, attrs) {
//                 var calcPages = function () {
//                     var display = +scope.display;
//                     var delta = Math.floor(display / 2);
//                     scope.start = scope.cur - delta;
//                     if (scope.start < 1) {
//                         scope.start = 1;
//                     }
//                     scope.end = scope.start + display - 1;
//                     if (scope.end > scope.total) {
//                         scope.end = scope.total;
//                         scope.start = scope.end - (display - 1);
//                         if (scope.start < 1) {
//                             scope.start = 1;
//                         }
//                     }

//                     scope.pages = [];
//                     for (var i = scope.start; i <= scope.end; ++i) {
//                         scope.pages.push(i);
//                     }
//                 };
//                 scope.$watch('cur', calcPages);
//                 scope.$watch('total', calcPages);
//                 scope.$watch('display', calcPages);

//                 scope.isCurrent = function (index) {
//                     return scope.cur == index;
//                 };

//                 scope.setCurrent = function (index) {
//                     scope.cur = index;
//                 };

//                 scope.hasPrev = function () {
//                     return scope.cur > 1;
//                 };
//                 scope.prev = function () {
//                     if (scope.hasPrev()) scope.cur--;
//                 };

//                 scope.hasNext = function () {
//                     return scope.cur < scope.total;
//                 };
//                 scope.next = function () {
//                     if (scope.hasNext()) scope.cur++;
//                 };

//                 scope.firstPage = function () {
//                     return scope.start == 1;
//                 };
//                 scope.goToFirstPage = function () {
//                     if (!scope.firstPage()) scope.cur = 1;
//                 };
//                 scope.lastPage = function () {
//                     return scope.end == scope.total;
//                 };
//                 scope.goToLastPage = function () {
//                     if (!scope.lastPage()) scope.cur = scope.total;
//                 };
//             }
//         };
//     });