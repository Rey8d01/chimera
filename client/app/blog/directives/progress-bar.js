/**
 * Анимированный компонент для демонстрации процесса загрузки приложения.
 */
chimera.system.blog.directive('progressBar', function () {
    return {
        restrict: 'EA',
        scope: {
            progress: '=',
        },
        templateUrl: "/app/blog/directives/progress-bar.html"
    };
});