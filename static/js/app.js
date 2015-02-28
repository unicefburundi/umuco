
$(function () {
    var data = [];
    var raba = {{timess|safe}};
    for (var i = 0; i < raba.length; i+=2) {
        data.push([parseInt(moment(raba[i+1]).format("x")), raba[i]] );
    };
    $('#container').highcharts({
        chart: {
            type: 'spline'
        },
        title: {
            text: 'Amount set aside for Children'
        },
        subtitle: {
            text: 'Irregular time data collected'
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
                text: 'Montant in Fb'
            },
            min: 0
        },
        tooltip: {
            headerFormat: '<b>{series.name}</b><br>',
            pointFormat: '{point.x:%e. %b}: {point.y} Fb'
        },

        plotOptions: {
            spline: {
                marker: {
                    enabled: true
                }
            }
        },
        series: [
            {
                name:'Montant',
                data: data
            }]
    });
});