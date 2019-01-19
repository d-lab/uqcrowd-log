var jsonData

// Get the worker ID from logger.js
$.ajax({
    url: "https://dke-uqcrowd-log.uqcloud.net/analytics/session/worker/" + worker_id + "/session_count",
    type: "GET",
    contentType: "text/plain",
    success: function(results) {
        jsonData = results;
        $("#uqcrowd-analytics").show()
    }
})

google.charts.load('current', {packages: ['corechart', 'bar']});
google.charts.setOnLoadCallback(drawMultiSeries);

function drawMultiSeries() {
    var data = new google.visualization.DataTable();

    data.addColumn('string', 'Date');
    data.addColumn('number', 'Session Count');
    data.addColumn('number', 'Message Count');
    data.addColumn('number', 'Avg Duration');

    jsonData.forEach(function (row) {
        data.addRow([
            row.datetime,
            row.session_count,
            row.message_count,
            row.total_duration/1000/row.session_count
        ]);
    });

    var options = {
        title: '',
        width: 480,
        height: 240,
        legend: 'none',
        chartArea: {left:'15%',top:'15%',width:'80%',height:'60%'},
    };

    var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}

$(document).ready(function() {
    $("#uqcrowd-analytics").hide();
    $("#uqcrowd-analytics .toggle").on("click", function(event) {
        $(this).parent().parent().toggleClass("show");
    });
});
