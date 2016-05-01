/**
 * Директива для построения списка постов.
 *
 * Применяется при отображении текстовых материалов в рамках категории, автора, тегов и т.д.
 */
chimera.system.main.directive('postList', function () {
    return {
        restrict: 'EA',
        scope: {
            posts: '=',
            paginationData: '=',
            readMore: '=',
            state: '@',
            catalogAlias: '='
        },
        templateUrl: "/app/blog/directives/post-list.html"
    };
});