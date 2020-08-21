# UQCrowd Logging System

**More Documents:**

1. Installation & Operation Guide: [README-MANUAL.md](README-MANUAL.md)
1. Log Message Format: [README-FORMAT.md](README-FORMAT.md)

## System Overall

The UQCrowd-Logging system uses HAProxy as a reverse proxy to distribute the incoming requests to multiple backends,
the optimized number of backends depends on the server's configuration, 8 is the optimized number for a server
with 40 Core, 60GB of RAM (derived from our performance test). The maximum throughput with the current configuration
 is ~2300 request/s (which can be doubled by adopting a message queue such as Redis)

![](docs/diagram.png)
**Figure 1.** Overall system diagram

_Note: The SSL certificates is handled by the UQ's Front Proxy._

## How To Use

This document is to describe how to inject javascript to record user actions on a MTurk Hit,

In order to inject the default logging configuration, you can simply embed the following script on top of your MTurk Template **(Please change the experiment ID to yours)**:

    <!-- BEGIN -->
    
    <!-- Jquery and Google Chart Library -->
    <script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    
    <!-- Set experiment ID -->
    <script type="text/javascript">
        exp_id_preDefined = "tom_exp1";  // change to your experiment ID
    </script>
    
    <!-- Logging System Script -->
    <script type="text/javascript" src="https://dke-uqcrowd-log.uqcloud.net/logger/fingerprint.js"></script>
    <script type="text/javascript" src="https://dke-uqcrowd-log.uqcloud.net/logger/logger.js"></script>
    
    <!-- Analytics Script and Style -->
    <script type="text/javascript" src="https://dke-uqcrowd-log.uqcloud.net/analytics/analytics.js"></script>
    <link rel="stylesheet" href="https://dke-uqcrowd-log.uqcloud.net/analytics/analytics.css"/>
    
    <!-- Analytics Charts Container -->
    <div id="uqcrowd-analytics">
        <div class="title"><span>+</span>Performance Analytics</div>
        <div class="row">
            <div id="uqcrowd-histogram"></div>
        </div>
        <div class="row">
            <div class="col">
                <div id="uqcrowd-hit"></div>
            </div>
            <div class="col">
                <div id="uqcrowd-assignment"></div>
            </div>
        </div>
    </div>
    
    <!-- END  -->

The default logging configuration records following type of log:

1. Start of a session with a auto-generated session_id,
1. Record the client's screen size and window size 
1. Record the browser fingerprint and client IP
1. Mouse clicks and the position of the clicks
1. Text editing on \<input type="text"\> and \<textarea\>
1. Value change of any \<select\> element
1. Focus event on HTML elements
1. Windows scroll action
1. End of a section with total message count.


In order to track additional event, you can also add more tracking script using predefined method named **send_log(log_type, sub_type, detail)**
The detailed log format is described in [README-FORMAT.md](README-FORMAT.md)


For example: 

    <script>
        $(document).ready(function() {
            // First example 
            $("#input01").on("click", function() {
                send_log("message", "Hello World!", {
                    item_1: "this is the detail item 1",
                    item_2: "this is the detail item 2"
                });
            });  
        });
    </script>
    
The first example will send the a **message** log, with the content of "Hello World!" along with an detailed object which contains two child elements when the
user clicks on the textfield with ID of **input01**

    <script>
        $(document).ready(function() {
            // Second example 
            $("img").on("mouseover", function() {
                send_log("html_event", "mouseover", {
                    element_tag: $(this).prop("tagName").toLowerCase(),
                    element_name: $(this).attr("name"),
                    element_id: $(this).attr("id"),
                });
            });      
        });
    </script>

The second example will send the message with **html_event** type with **mouseover** sub_type when user hover on any images
in the document. The information of tag, name, id of those images will be sent along with the message.

All log message will be printed on console so that you can test and verify the injection offline before Publishing a task

*If you need more information, please have a look at the full example here:* [templates/macbook.html](./templates/macbook.html)
