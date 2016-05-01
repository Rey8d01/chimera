chimera.system.blog = angular.module("blog", ["ngResource", "ngSanitize"]);

/**
 * AuthorHandler
 */
chimera.system.blog.factory("authorService", ["$resource",
    function ($resource) {
        return $resource("/author/:userId/:page", {page: "1"});
    }
]);

/**
 * PostItemHandler
 */
chimera.system.blog.factory("postItemService", ["$resource",
    function ($resource) {
        return $resource("/post-item/:postAlias", {postAlias: null}, {
            save: {method: "POST", params: {postAlias: null}}
        });
    }
]);

/**
 * PostListHandler
 */
chimera.system.blog.factory("postListService", ["$resource",
    function ($resource) {
        return $resource("/post-list");
    }
]);

/**
 * TagItemHandler
 */
chimera.system.blog.factory("tagItemService", ["$resource",
    function ($resource) {
        return $resource("/tag-item/:tagAlias/:page", {page: "1"}, {
            save: {method: "POST", params: {tagAlias: null, page: null}}
        });
    }
]);

/**
 * TagListHandler
 */
chimera.system.blog.factory("tagListService", ["$resource",
    function ($resource) {
        return $resource("/tag-list");
    }
]);
