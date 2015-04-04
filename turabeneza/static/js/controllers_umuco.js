/**
* myApp Module
*
* Description
*/
var groupControllers = angular.module('groupControllers', ['ngAnimate']);

groupControllers.controller('ListController', ['$scope', '$http', function ($scope, $http){
    $http.get('api/v1/groups/').success(function (data) {
        $scope.groups= data;
        $scope.groupOrder= 'name';
    });
    }]);

groupControllers.controller('DetailsController', ['$scope', '$http', '$routeParams' , function ($scope, $http, $routeParams){
    $http.get('js/data.json').success(function (data) {
        $scope.groups= data;
        $scope.whichItem = $routeParams.itemId;
        if ($routeParams.itemId > 0) {
            $scope.prevItem = Number($routeParams.itemId) - 1;
        } else{
            $scope.prevItem = $scope.groups.length -1;
        };
        if ($routeParams.itemId < $scope.groups.length-1) {
            $scope.nextItem = Number($routeParams.itemId) + 1;
        } else{
            $scope.nextItem = 0;
        };
    });
    }]);
