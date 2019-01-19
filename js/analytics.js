var jsonData
$.ajax({
    url: "https://dke-uqcrowd-log.uqcloud.net/analytics/session/worker/A1GL5AQV7VT91U/session_count",
    type: "GET",
    contentType: "text/plain",
    success: function(results) {
        jsonData = results
    }
})

google.charts.load('current', {packages: ['corechart', 'bar']});
google.charts.setOnLoadCallback(drawMultiSeries);

function drawMultiSeries() {
    var data = new google.visualization.DataTable();

    data.addColumn('string', 'Date');
    data.addColumn('number', 'Session Count');
    data.addColumn('number', 'Message Count');
    data.addColumn('number', 'Total Duration');

    jsonData.forEach(function (row) {
        data.addRow([
            row.datetime,
            row.session_count,
            row.message_count,
            row.total_duration
        ]);
    });

    var options = {
        title: 'Session Count by Day',
        width: 480,
        height: 240,
        legend: 'none',
        chartArea: {left:'15%',top:'15%',width:'80%',height:'60%'},
    };

    var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}

$(document).ready(function() {
    $("#toggle").on("click", function(event) {
        $(this).parent().parent().toggleClass("show");
    });
});
