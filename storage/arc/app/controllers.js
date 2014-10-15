/* Controllers */

var phonecatControllers = angular.module('phonecatControllers', []);

phonecatControllers.controller('PhoneListCtrl', ['$scope', 'Phone',
    function ($scope, Phone) {
        $scope.phones = Phone.query();
        $scope.orderProp = 'age';
    }]);

phonecatControllers.controller('PhoneDetailCtrl', ['$scope', '$routeParams', 'Phone',
    function ($scope, $routeParams, Phone) {
        $scope.phone = Phone.get({phoneId: $routeParams.phoneId}, function(data) {
            $scope.mainImageUrl = data.images[0].big;
        });

        $scope.setImage = function(imageUrl) {
            $scope.mainImageUrl = imageUrl;
        }
    }
]);

/* Controllers */
//var phonecatApp = angular.module('phonecatApp', []);
//
//phonecatApp.controller('PhoneListCtrl', function($scope, $http) {
//
//    $http.get('app/phones.json').success(function(data) {
//        $scope.phones = data;
//    });
//
//    $scope.orderProp = 'age';
//});