// Split URL and Query
hit_url = document.URL.split('?')[0];
query = document.URL.split('?')[1];

// Parse the parameters from Query
params = [];
if (query != undefined) {
    entries = query.split('&');
    for (var i = 0; i < entries.length; i++){
        var entry = entries[i].split('=');
        params[entry[0]] = entry[1];
    }
}

// Generate random Session ID
session_id = Math.random().toString(36).substr(2, 12);

// Get the Worker ID from URI query
worker_id = params["workerId"];
assignment_id = params["assignmentId"];
hit_id = params["hitId"];

sequence = 0
message_count = 0

// Define the send_log Function
function send_log(log_type, sub_type, detail) {

    content = {}
    content[log_type] = sub_type;
    content['detail'] =  detail

    data = {
        log_type: log_type,
        sequence_number: sequence,
        browser_time: new Date(),
        session_id: session_id,
        worker_id: worker_id,
        assignment_id: assignment_id,
        hit_id: hit_id,
        content: content
    }

    sequence++

    $.ajax({
        url: "https://dke-uqcrowd-log.uqcloud.net/logger/insert",
        type: "POST",
        data: JSON.stringify(data),
        contentType: "text/plain",
        success: function(result) {
            message_count++
        }
    })

    console.log(JSON.stringify(data))
}

$(document).ready(function() {

    // Start Session
    send_log("message", "Start Session", {
        hit_url: hit_url,
        hit_query: query
    });

    // Check Screen Size
    send_log("message", "Screen Size", {
        screen_width: window.screen.width,
        screen_height: window.screen.height,
        window_width: $(window).width(),
        window_height: $(window).height()
    });

    // Track Mouse Event
    $(window).on("click", function(event) {
        event.stopPropagation();
        send_log("mouse_event", "click", {
            event_x: event.pageX,
            event_y: event.pageY
        });
    });

    $("*").on("focus", function(event) {
        send_log("html_event", "focus", {
            element_tag: $(this).prop("tagName").toLowerCase(),
            element_name: $(this).attr("name"),
            element_id: $(this).attr("id"),
        });
    });

    // Track Select Value Changes (Questions)
    $("select").on("change", function() {
        send_log("html_event", "change_value", {
            element_tag: $(this).prop("tagName").toLowerCase(),
            element_name: $(this).attr("name"),
            element_id: $(this).attr("id"),
            value: $(this).children("option:selected").val()
        });
    });

    $("input[type='text'], textarea").on("paste", function(event) {
        currentPos = $(this).prop("selectionStart");
        send_log("browser_event", "clipboard", {
            action: "paste",
            element_tag: $(this).prop("tagName").toLowerCase(),
            element_name: $(this).attr("name"),
            element_id: $(this).attr("id"),
            position: currentPos,
            value: window.event.clipboardData.getData('text'),
        });
    });

    $("input[type='text'], textarea").on("cut", function(event) {
        startPos = $(this).prop('selectionStart')
        endPos = $(this).prop('selectionEnd')
        send_log("browser_event", "clipboard", {
            action: "cut",
            element_tag: $(this).prop("tagName").toLowerCase(),
            element_name: $(this).attr("name"),
            element_id: $(this).attr("id"),
            value: $(this).val().substring(startPos, endPos)
        });
    });

    $("input[type='text'], textarea").on("copy", function(event) {
        startPos = $(this).prop('selectionStart')
        endPos = $(this).prop('selectionEnd')
        send_log("browser_event", "clipboard", {
            action: "copy",
            element_tag: $(this).prop("tagName").toLowerCase(),
            element_name: $(this).attr("name"),
            element_id: $(this).attr("id"),
            value: $(this).val().substring(startPos, endPos)
        });
    });

    $("input[type='text'], textarea").on("blur", function(event) {
        send_log("html_event", "change_value", {
            element_tag: $(this).prop("tagName").toLowerCase(),
            element_name: $(this).attr("name"),
            element_id: $(this).attr("id"),
            value: $(this).val()
        });
    });

    // Track Windows Scroll
    scroll_lock = false;
    $(window).on("scroll", function() {
        if (!scroll_lock) {
            setTimeout(function() {
                send_log("browser_event", "scroll", {
                    top: $(window).scrollTop(),
                    left: $(window).scrollLeft()
                });
                scroll_lock = false}
            , 1000);
        }
        scroll_lock = true;
    });

    // End Session
    $(window).on('beforeunload', function(){
        send_log("message", "End Session", {
            session_id: session_id,
            message_count: message_count
        });
    });

});