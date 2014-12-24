// var twitterApp = angular.module('twitterApp', ['twitterApp.services']);

angular.module('twitterApp.services', ['ngCookies']).factory('twitterService', function($q, $location, $cookieStore) {

    var authorizationResult = false;

    // Представление серверу
    var introduceToServer = function(full) {
        promise = authorizationResult.me().done(function(data) {
            console.log('introduceToServer')
            xhr = $.post(chimera.config.baseUrl+"/introduce", {
                auth_type: "twitter", 
                user_id: data.id,
                user_info: full ? data : null
            }, function(response) {
                $location.path('/main/home/');
                $location.replace();
            });
        });
    };

    // logout
    var logoutServer = function() {
        $.get(chimera.config.baseUrl+"/logout");
        $location.path('/login/');
        $location.replace();
    };

    return {
        initialize: function() {
            //initialize OAuth.io with public key of the application
            OAuth.initialize('t3zjIiwpODrlse81ifHaaTC-VPs', {cache:true});
            //try to create an authorization result when the page loads, this means a returning user won't have to click the twitter button again
            authorizationResult = OAuth.create('twitter');
            if (authorizationResult) {
                introduceToServer();
            };
        },
        isReady: function() {
            return (authorizationResult);
        },
        connectTwitter: function() {
            var deferred = $q.defer();
            OAuth.popup('twitter', {cache:true}, function(error, result) { //cache means to execute the callback if the tokens are already present
                console.log(error, result);
                if (!error) {
                    authorizationResult = result;
                    deferred.resolve();

                    // Introduce
                    introduceToServer(true);
                } else {
                    console.log('error');
                    //do something if there's an error
                }
            });
            return deferred.promise;
        },
        clearCache: function() {
            logoutServer();
            OAuth.clearCache('twitter');
            authorizationResult = false;
        }
    }
    
});

//inject the twitterService into the controller
chimera.system.main.controller('TwitterController', function($scope, $q, twitterService) {

    
    twitterService.initialize();

    $scope.connectButton = function() {
        twitterService.connectTwitter().then(function() {
            if (twitterService.isReady()) {
                $('#connectButton').fadeOut();
                $('#signOut').fadeIn();
            }
        });
    }

    $scope.signOut = function() {
        twitterService.clearCache();
        $('#connectButton').fadeIn();
        $('#signOut').fadeOut();
    }

    if (twitterService.isReady()) {
        $('#connectButton').hide();
        $('#signOut').fadeIn();
    }

});
