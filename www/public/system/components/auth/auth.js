chimera.system.auth = angular.module('auth', ['ngCookies']);

// Внедрение компонента авторизации в систему
chimera.system.main.controller("AuthController", ["$scope", "$q", "authService",
    function($scope, $q, authService) {

        console.log('AuthController');

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

        $scope.pass = {
            word: ''
        };
        $scope.privateConnectButton = function() {
            authService.private($scope.pass.word).then(function(data) {
                $(".sign-in-button").fadeOut();
                $(".sign-out-button").fadeIn();
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


chimera.system.auth.factory("authService", ["$q", "$location", "$cookies",
    function($q, $location, $cookies) {

        // Объект авторизации через который происходят все соединения с сервером авторизации
        var authorization = false;
        // Имя сервиса через который произошла авторизация
        var authorizationType = false;

        // Попытка пересоздать подключение при перезагрузке страницы
        var reConnect = function() {
            console.log($cookies.getAll());
            var tryAuthorization = false,
                authType = null;
            for (var i in chimera.config.auth) {
                authType = chimera.config.auth[i];
                if (authType != 'manual') {
                    tryAuthorization = OAuth.create(authType);
                    if (tryAuthorization) {
                        authorizationType = authType;
                        authorization = tryAuthorization
                        return true;
                    }
                }
            }
            return false;
        };

        // Представление серверу
        var introduce = function(full) {
            console.log('introduce', full);
            authorization.me().done(function(data) {
                if (!data.id) {
                    disconnect();
                }

                $.post(chimera.config.baseUrl + "/introduce", {
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
            console.log('disconnect', authorization);
            // Выход из системы, очистка кук
            OAuth.clearCache(authorizationType);
            authorization = authorizationType = false;

            $.get(chimera.config.baseUrl + "/logout");
            $location.path("/login").replace();
        };

        return {
            initialize: function() {
                console.log('init', authorization);
                // Соединение с OAuth.io
                OAuth.initialize("t3zjIiwpODrlse81ifHaaTC-VPs", {
                    cache: true
                });
                if (reConnect()) {
                    console.log('reConnect true', authorization);
                    authorization || introduce();
                } else {
                    console.log('reConnect false', authorization);
                    authorization || disconnect();
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
                OAuth.popup(typeAuthService, {
                    cache: true
                }, function(error, result) { //cache means to execute the callback if the tokens are already present
                    if (!error) {
                        authorization = result;
                        authorizationType = typeAuthService;
                        deferred.resolve();

                        introduce(true);
                    } else {
                        deferred.reject();
                        console.log("error");
                    }
                });
                return deferred.promise;
            },
            private: function(passphrase) {
                var deferred = $q.defer();
                $.post(chimera.config.baseUrl + "/private", {
                    passphrase: passphrase
                }, function(response) {
                    if (response.content.auth && ($location.path() == "/login")) {
                        deferred.resolve();
                        authorization = true;
                        authorizationType = 'manual'
                        $location.path("/main/home").replace();
                    } else {
                        deferred.reject();
                    }
                });

                return deferred.promise;
            },
            disconnect: disconnect,
            getMeData: function() {
                //create a deferred object using Angular's $q service
                var deferred = $q.defer();

                if (authorizationType == 'manual') {
                    var data = {
                        id: '',
                        name: 'Admin',
                        firstname: '',
                        lastname: '',
                        alias: '',
                        email: '',
                        birthdate: '',
                        gender: '',
                        location: '',
                        local: '',
                        company: '',
                        occupation: '',
                        raw: {}
                    };
                    deferred.resolve(data);
                } else {
                    var promise = authorization.me().done(function(data) {
                        //when the data is retrieved resolved the deferred object
                        deferred.resolve(data);
                    });
                }
                //return the promise of the deferred object
                return deferred.promise;
            }
        }

    }
]);
