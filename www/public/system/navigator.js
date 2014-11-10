/**
 * Модуль управляющий навигацией.
 * Формирует навигационное меню и собирает прочие подобные элементы в кучу.
 */

chimera.system.navigator = angular.module('navigator', ['ngResource']);

// Контроллер
chimera.system.navigator.controller('NavigatorController', ['$scope', 'NavigatorData',
    function ($scope, NavigatorData) {
        $scope.navigatorData = NavigatorData.getNavigatorData();
    }
]);

// Сервис
chimera.system.navigator.factory('NavigatorData', ['$resource',
    function ($resource) {
        return $resource(chimera.config.baseUrl + ":navigator", {navigator: 'navigator'}, {
            getNavigatorData: {method: 'GET', isArray: true}
        });
    }]);