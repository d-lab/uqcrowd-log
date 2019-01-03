var message_count
$.ajax({
    url: "https://dke-uqcrowd-log.uqcloud.net/analytics/message-count",
    type: "GET",
    contentType: "text/plain",
    success: function(result) {
        message_count = result
    }
})

google.charts.load('current', {packages: ['corechart', 'bar']});
google.charts.setOnLoadCallback(drawMultSeries);

function drawMultSeries() {
    mydata = [["date","count"]]
    mydata = mydata.concat(message_count)
    var data = google.visualization.arrayToDataTable(mydata);

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