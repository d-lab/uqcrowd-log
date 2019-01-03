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


In order to track additional event, you can also add more tracking script using predefined method named **send_log(log_type, sub_type, detail)**
The detailed log format is described in [FORMAT.md](https://github.com/d-lab/uqcrowd-log/blob/master/FORMAT.md)

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

The second example will send the message with **html_event** type with **hover** sub_type when user hover on any images
in the document. The information of tag, name, id of those images will be sent along with the message.
    

_If you need more information, please have a look at the full example here:_ [logger.html](https://github.com/d-lab/uqcrowd-log/blob/master/templates/logger.html)