'use strict';

$(document).ready(function() {
    var chartData = {{data|safe}};
    // Group details charts
     var groupDetailsOptions = {
        chart: {
            renderTo: 'chart_panel',
            type: 'area',
            zoomType: 'x'
      },
        legend: {enabled: false},
        title: {text: 'Group details charts'},
        subtitle: {text: 'Last 14 Days'},
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
        series : [{}],
    };

    groupDetailsOptions.series[0].name = chartData[0].name;
    groupDetailsOptions.series[0].data = chartData[0].data;
        var chart = new Highcharts.Chart(groupDetailsOptions);
    });