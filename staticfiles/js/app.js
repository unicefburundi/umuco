'use strict';

var myapp = angular.module('myapp', ["highcharts-ng"]);

myapp.controller('myctrl',['$scope', '$http', function ($scope, $http)  {

  $scope.chartTypes = [
    {"id": "line", "title": "Ligne"},
    {"id": "spline", "title": "Ligne lisse"},
    {"id": "area", "title": "surface"},
    {"id": "areaspline", "title": "surface lisse"},
    {"id": "column", "title": "Colonne"},
    {"id": "bar", "title": "Barre"},
    {"id": "pie", "title": "Tarte"},
    {"id": "scatter", "title": "Dispersion"}
  ];

  $scope.dashStyles = [
    {"id": "Solid", "title": "Solid"},
    {"id": "ShortDash", "title": "ShortDash"},
    {"id": "ShortDot", "title": "ShortDot"},
    {"id": "ShortDashDot", "title": "ShortDashDot"},
    {"id": "ShortDashDotDot", "title": "ShortDashDotDot"},
    {"id": "Dot", "title": "Dot"},
    {"id": "Dash", "title": "Dash"},
    {"id": "LongDash", "title": "LongDash"},
    {"id": "DashDot", "title": "DashDot"},
    {"id": "LongDashDot", "title": "LongDashDot"},
    {"id": "LongDashDotDot", "title": "LongDashDotDot"}
  ];

  $scope.chartSeries1  = [];
  $scope.chartSeries2  = [];
  $scope.chartSeries3  = [];

  $http.get('/report/overview/').success(function(data) {
      // console.log(data)
      $scope.chartConfig1.series.push(data[0]);
      $scope.chartConfig2.series.push(data[1]);
      $scope.chartConfig3.series.push(data[2]);
      console.log($scope.chartConfig1.series);

   }).
  error(function(data, status, headers, config) {
    // called asynchronously if an error occurs
    // or server returns response with an error status.
    console.log(status);
    console.log(data);
  });

  $scope.chartStack = [
    {"id": '', "title": "Sans"},
    {"id": "normal", "title": "Normale"},
    {"id": "percent", "title": "Poucent"}
  ];


  $scope.chartConfig1 = {
    options: {
      chart: {
        type: 'areaspline',
        zoomType: 'x'
      },
      plotOptions: {
        series: {
          stacking: '',
          fillColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1},
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                },
                marker: {
                    radius: 2
                },
                lineWidth: 1,
                states: {
                    hover: {
                        lineWidth: 1
                    }
                },
                threshold: null
            }
      }
    },
    series: $scope.chartSeries1,
    title: {
      text: 'Montant mis de côté dans le fonds de OEV',
    },
    subtitle: {text: 'Cumulatif pour tous les groupes'},
    credits: {
      enabled: true
    },
    xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: { // don't display the dummy year
                month: '%b \'%y',
                day: '%e. %b',
                // year: '%Y. %b'
            },
            title: {
                text: 'Date'
            }
        },
     yAxis: {
            title: {
                text: 'Fbu'
            }
        },
    loading: false,
    size: {}
  };

$scope.chartConfig2 = {
    options: {
      chart: {
        type: 'areaspline',
        zoomType: 'x'
      },
      plotOptions: {
        series: {
          stacking: '',
           fillColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1},
                    stops: [
                        [0, Highcharts.getOptions().colors[1]],
                        [1, Highcharts.Color(Highcharts.getOptions().colors[1]).setOpacity(0).get('rgba')]
                    ]
                },
                marker: {
                    radius: 2
                },
                lineWidth: 1,
                states: {
                    hover: {
                        lineWidth: 1
                    }
                },
                threshold: null
            }
      }
    },
    series: $scope.chartSeries2,
    title: {
      text: 'Lampes rechargées'
    },
    subtitle: {text: 'Cumulatif pour tous les groupes'},
    credits: {
      enabled: true
    },
     xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: { // don't display the dummy year
                month: '%b \'%y',
                day: '%e. %b',
                // year: '%Y. %b'
            },
            title: {
                text: 'Date'
            }
        },
     yAxis: {
            title: {
                text: 'Unités'
            }
        },
    loading: false,
    size: {}
  };

  $scope.chartConfig3 = {
    options: {
      chart: {
        type: 'areaspline',
        zoomType: 'x'
      },
      plotOptions: {
        series: {
          stacking: '',
          fillColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1},
                    stops: [
                        [0, Highcharts.getOptions().colors[2]],
                        [1, Highcharts.Color(Highcharts.getOptions().colors[3]).setOpacity(0).get('rgba')]
                    ]
                },
                marker: {
                    radius: 2
                },
                lineWidth: 1,
                states: {
                    hover: {
                        lineWidth: 1
                    }
                },
                threshold: null
            }
      }
    },
    series: $scope.chartSeries3,
    title: {
      text: 'Lampes vendues'
    },
    subtitle: {text: 'Cumulatif pour tous les groupes'},
    credits: {
      enabled: true
    },
     xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: { // don't display the dummy year
                month: '%b \'%y',
                day: '%e. %b',
                // year: '%Y. %b'
            },
            title: {
                text: 'Date'
            }
        },
     yAxis: {
            title: {
                text: 'Unités'
            }
        },
    loading: false,
    size: {}
  };


}]);