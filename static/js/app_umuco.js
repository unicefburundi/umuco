 var umucoApp = angular.module('umucoApp', [
    'ngRoute',
    'groupControllers'
    ]);

var groupControllers = angular.module('groupControllers', ['ngAnimate']);

groupControllers.controller('ListController', ['$scope', '$http', function ($scope, $http){
    $http.get('/report/groups/').success(function (data) {
        console.log(data);
        $scope.groups= data;
        $scope.groupOrder= 'name';
    });
    }]);