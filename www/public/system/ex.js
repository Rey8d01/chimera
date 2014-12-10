// var twitterApp = angular.module('twitterApp', ['twitterApp.services']);

angular.module('twitterApp.services', []).factory('twitterService', function($q) {

    var authorizationResult = false;

    // Представление серверу
    var introduceToServer = function(full) {
        if (full == undefined) {
            full = false
        }

        promise = authorizationResult.me().done(function(data) {
            console.log(data);
            $.post(chimera.config.baseUrl+"/introduce", {
                type: "twitter", 
                id: data.id,
                info: full ? info : null
            });
        });

    }

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
            OAuth.clearCache('twitter');
            authorizationResult = false;
        },
        getLatestTweets: function () {
            //create a deferred object using Angular's $q service
            var deferred = $q.defer();
            var promise = authorizationResult.get('/1.1/statuses/home_timeline.json').done(function(data) { //https://dev.twitter.com/docs/api/1.1/get/statuses/home_timeline
                //when the data is retrieved resolved the deferred object
                deferred.resolve(data)
            });
            //return the promise of the deferred object
            return deferred.promise;
        }
    }
    
});

//inject the twitterService into the controller
chimera.system.main.controller('TwitterController', function($scope, $q, twitterService) {

    $scope.tweets; //array of tweets
    
    twitterService.initialize();

    //using the OAuth authorization result get the latest 20 tweets from twitter for the user
    $scope.refreshTimeline = function() {
        twitterService.getLatestTweets().then(function(data) {
            $scope.tweets = data;
        });
    }

    //when the user clicks the connect twitter button, the popup authorization window opens
    $scope.connectButton = function() {
        twitterService.connectTwitter().then(function() {
            if (twitterService.isReady()) {
                //if the authorization is successful, hide the connect button and display the tweets
                $('#connectButton').fadeOut(function(){
                    $('#getTimelineButton, #signOut').fadeIn();
                    $scope.refreshTimeline();
                });
            }
        });
    }

    //sign out clears the OAuth cache, the user will have to reauthenticate when returning
    $scope.signOut = function() {
        twitterService.clearCache();
        $scope.tweets.length = 0;
        $('#getTimelineButton, #signOut').fadeOut(function(){
            $('#connectButton').fadeIn();
        });
    }

    //if the user is a returning user, hide the sign in button and display the tweets
    if (twitterService.isReady()) {
        $('#connectButton').hide();
        $('#getTimelineButton, #signOut').show();
        $scope.refreshTimeline();
    }

});
