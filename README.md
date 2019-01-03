# UQCloud Logging System

This document is to describe how to inject javascript to log user actions on a MTurk Hit,

In order to inject the logging configuration, you can simply embed the following script on top of your MTurk Template:

    <script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
    <script src="https://dke-uqcrowd-log.uqcloud.net/logger/logger.js"></script>

The default logging configuration records following type of log:

1. Start of a session with a auto-generated session_id
2. Mouse clicks and the position of the clicks
3. Text editing on TextField and TextArea
4. Focus event on HTML elements
5. Windows scroll action
6. End of a section with total message count.


In order to track additional event, you can also add more tracking script using predefined method named send_log()

The accepted log format is described in [FORMAT.md](https://github.com/d-lab/uqcrowd-log/blob/master/FORMAT.md)

For example: 

    <script>
        $(document).ready(function() {
            $("#input01").on("blur", function() {
                send_log("message", "This is the message content", {
                    item_1: "this is the detail item 1",
                    item_2: "this is the detail item 2"
                });
            });
        });
    </script>
    
If you need more information, please have a look at the full example here: [logger.html](https://github.com/d-lab/uqcrowd-log/blob/master/templates/logger.html)