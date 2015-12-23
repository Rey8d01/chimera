/**
 * Информация по авторизованному пользователю.
 */

chimera.system.user = angular.module("user", ["ngResource"]);

chimera.system.user.factory("userMeService", ["$resource",
    function ($resource) {
        return $resource("/me");
    }
]);
