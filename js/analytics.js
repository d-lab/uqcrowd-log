var baseURI = "https://dke-uqcrowd-log.uqcloud.net/analytics/session/worker/"
var histogramData
var aggregationData

// Get the worker ID from logger.js
$.ajax({
    url: baseURI + worker_id + "/histogram",
    type: "GET",
    contentType: "text/plain",
    success: function(results) {
        histogramData = results;
    }
})

$.ajax({
    url: baseURI + worker_id + "/aggregation",
    type: "GET",
    contentType: "text/plain",
    success: function(results) {
        aggregationData = results;
    }
})

google.charts.load('current', {packages: ['corechart', 'bar']});
google.charts.setOnLoadCallback(drawCharts);

function drawCharts() {
    drawHistogram();
    drawAggregation();
};

function drawHistogram() {
    var data = new google.visualization.DataTable();

    data.addColumn('string', 'Date');
    data.addColumn('number', 'Session Count');
    data.addColumn('number', 'Avg Message Count');
    data.addColumn('number', 'Average Duration');

    histogramData.forEach(function (row) {
        data.addRow([
            row.datetime,
            row.session_count,
            row.message_count/row.session_count,
            row.total_duration/1000/row.session_count
        ]);
    });

    var options = {
        title: '',
        width: 480,
        height: 240,
        legend: 'none',
        chartArea: {left:'10%',top:'15%',width:'85%',height:'60%'},
    };

    var chart = new google.visualization.ColumnChart(document.getElementById("chart-histogram"));
    chart.draw(data, options);
}

function drawAggregation() {
    var data = new google.visualization.DataTable();

    data.addColumn('string', 'HitID');
    data.addColumn('number', 'Count');

    console.log(aggregationData.hit_id)

    aggregationData.hit_id.forEach(function (row) {
        data.addRow([
            row.key,
            row.doc_count,
        ]);
    });

    var options = {
        title: '',
        width: 480,
        height: 240,
        legend: 'none',
        chartArea: {left:'10%',top:'15%',width:'85%',height:'60%'},
    };

    var chart = new google.visualization.PieChart(document.getElementById("chart-aggregation"));
    chart.draw(data, options);
}

$(document).ready(function() {
    $("#uqcrowd-analytics span").on("click", function(event) {
        $(this).parent().parent().toggleClass("show");
        send_log("message", "Analytics", {
            "action": "toggle",
            "status": $(this).parent().parent().hasClass("show")
        });
    });
});
