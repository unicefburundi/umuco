// for the application myApp using AngularJs
'use strict';

var myApp = angular.module('myApp', ["highcharts-ng"]);

myApp.controller('ListController', ['$scope', '$http', function($scope, $http) {
$http.get('/report/group/?format=json').success(function(data) {
    $scope.groups = data;
});

}]);

$(document).ready(function(){
    $('select[name=province]').change(function(){
            province_id = $(this).val();
            request_url = '/get_districts/' + province_id + '/';
            $.ajax({
                url: request_url,
                success: function(data){
                    $('select[name=districts]').val(''); // remove the value from the input
                    console.log(data); // log the returned json to the console
                    $.each(data[0], function(key, value){
                        $('select[name=districts]').append('<option value="' + key + '">' + value +'</option>');
                    });
                }
            });
            return false; //<---- move it here
        });
});