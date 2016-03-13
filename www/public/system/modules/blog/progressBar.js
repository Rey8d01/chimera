/**
 * Анимированный компонент для демонстрации процесса загрузки приложения.
 */
chimera.system.main.directive('progressBar', function () {
    return {
        restrict: 'EA',
        scope: {
            progress: '=',
        },
        templateUrl: "/system/templates/blog/progressBar.html"
    };
});