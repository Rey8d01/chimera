/**
 * Дирекива для построения списка постов.
 *
 * Применяется при отображении текстовых материалов в рамках категории, автора, тегов и т.д.
 */
chimera.system.main.directive('listPosts', function () {
    return {
        restrict: 'EA',
        scope: {
            posts: '=',
            paginationData: '=',
            readMore: '=',
            state: '@',
            catalogAlias: '='
        },
        templateUrl: "/system/templates/blog/content/listPosts.html"
    };
});