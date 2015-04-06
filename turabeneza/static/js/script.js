'use strict';

var myApp = angular.module('myApp', ["highcharts-ng"]);

myApp.controller('MyController', ['$scope', '$http', function($scope, $http) {
$http.get('/report/group/?format=json').success(function(data) {
    console.log(data)
    $scope.groups = data;
});

}]);
