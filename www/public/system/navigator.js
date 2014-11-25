/**
 * Модуль управляющий навигацией.
 * Формирует навигационное меню и собирает прочие подобные элементы в кучу.
 */

chimera.system.navigator = angular.module('navigator', ['ngResource']);

// Контроллер
chimera.system.navigator.controller('NavigatorController', ['$scope', 'navigatorLoader',
    function ($scope, navigatorLoader) {
        navigatorLoader.get({}, function(response) {
        	$scope.navigator = response.content.navigator
        });
    }
]);

// Сервис
chimera.system.navigator.factory('navigatorLoader', ['$resource',
    function ($resource) {
        return $resource(chimera.config.baseUrl + "/navigator");
    }]);