
chimera.system.auth = angular.module('auth', ['ngCookies']);

// Внедрение компонента авторизации в систему
chimera.system.main.controller("AuthController", ["$scope", "$q", "authService", 
    function($scope, $q, authService) {

        authService.initialize();

        $scope.main = {
            "title": "Rey's-ysetm",
            "readMore": "ReadMe...",
            "foo": "BAAAAAR"
        };

        // Отложенная запись в скоп всех данных
        if (authService.isReady()) {
            authService.getMeData().then(function(data) {
                $scope.user = data;
            });
        }

        $scope.connectButton = function(typeAuthService) {
            authService.connect(typeAuthService).then(function() {
                if (authService.isReady()) {
                    $(".sign-in-button").fadeOut();
                    $(".sign-out-button").fadeIn();
                }
            });
        }

        $scope.signOut = function() {
            authService.disconnect();
            $(".sign-in-button").fadeIn();
            $(".sign-out-button").fadeOut();
        }

        if (authService.isReady()) {
            $(".sign-in-button").hide();
            $(".sign-out-button").fadeIn();
        }

    }
]);


chimera.system.auth.factory("authService", ["$q", "$location", "$cookieStore", 
    function($q, $location, $cookieStore) {

        // Объект авторизации через который происходят все соединения с сервером авторизации
        var authorization = false;
        // Имя сервиса через который произошла авторизация
        var authorizationType = false;

        // Попытка пересоздать подключение при перезагрузке страницы
        var reConnect = function() {
            var tryAuthorization = false
            for(var i in chimera.config.auth) {
                tryAuthorization = OAuth.create(chimera.config.auth[i]);
                if (tryAuthorization) {
                    authorizationType = chimera.config.auth[i];
                    authorization = tryAuthorization
                    return true;
                }
            }
            return false;
        };

        // Представление серверу
        var introduce = function(full) {
            authorization.me().done(function(data) {
                if(!data.id) {
                    disconnect();
                }

                $.post(chimera.config.baseUrl+"/introduce", {
                    auth_type: authorizationType, 
                    user_id: data.id,
                    user_info: full ? data : null
                }, function(response) {
                    if ($location.path() == "/login") {
                        $location.path("/main/home").replace();
                    }
                });
            });
        };

        var disconnect = function() {
            // Выход из системы, очистка кук
            OAuth.clearCache(authorizationType);
            authorization = authorizationType = false;

            $.get(chimera.config.baseUrl+"/logout");
            $location.path("/login").replace();
        };

        return {
            initialize: function() {
                // Соединение с OAuth.io
                OAuth.initialize("t3zjIiwpODrlse81ifHaaTC-VPs", {cache:true});
                // authorizationResult = OAuth.create('twitter');
                // console.log(authorizationResult);
                if (reConnect()) {
                    introduce();
                } else {
                    disconnect();
                }
            },
            isReady: function() {
                return authorization;
            },
            connect: function(typeAuthService) {
                // Процесс авторизации через сторонний сервис
                if (!_.contains(chimera.config.auth, typeAuthService)) {
                    return false;
                }

                var deferred = $q.defer();
                OAuth.popup(typeAuthService, {cache:true}, function(error, result) { //cache means to execute the callback if the tokens are already present
                    if (!error) {
                        authorization = result;
                        authorizationType = typeAuthService;
                        deferred.resolve();

                        introduce(true);
                    } else {
                        console.log("error");
                    }
                });
                return deferred.promise;
            },
            disconnect: disconnect,
            getMeData: function () {
                //create a deferred object using Angular's $q service
                var deferred = $q.defer();
                var promise = authorization.me().done(function(data) {
                    //when the data is retrieved resolved the deferred object
                    deferred.resolve(data)
                });
                //return the promise of the deferred object
                return deferred.promise;
            }
        }
        
    }
]);
