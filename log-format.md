# uqcrowd-log format

This document is to describe the log format of UQCrowd Logging system

The base log message will have the following compulsory field: **log_type**, **sequence_number**, **browser_time**, **session_id**, **worker_id**, **hit_id**, **assessment_id**, **job_id**, **content**

The structure of the **content** field may be different according to the log_type,
this field provides the flexibility for defining the message structures, 
Moreover, inside each **content** object, there is an **optional** object named **details** which gives the ability to extent the data in the future
 
The session_id is generated randomly using javascript:

    <script>
        // Generate random Session ID
        session_id = Math.random().toString(36).substr(2, 12);
	</script>
 
Sample log message:

    {
        "log_type": "message",
        "sequence_number": 1,
        "browser_time": "2018-09-16T23:40:28+00:00",
        "session_id": "ojkjj8pvav",
        "worker_id": <Worker_ID from Mturk,
        "hit_id": <Hit_ID from MTurk>,
        "assessment_id": <Assessment_ID from Mturk>,
        "job_id": "TEST1234",
        "content": {
            "message": "Start Session"
        }
    }


### Content structure for each log\_type:

#### 1. message
Compulsory: **message**, Optional: **details**

    "type": "message",
    "content": {
        "message": "Start Session"
        "details": {
            "topic": "random topic name" 
        }
    }
    
or 

    "type": "message",
    "content": {
        "message": "End Session",
        "details": {
            "final_result": true
            "check_result": [true, false]
            "components": []
        }
    }
    
or 


#### 2. mouse_event: 
Compulsory: **mouse_event**, the value must be one of **left_click, right_click, double_click, select**
Optional: **details**

An example of a left-click action message

    "type": "mouse_event",
    "content": {
        "mouse_event": "left_click",
        "details": {
            "x": 100,
            "y": 400
        }
    }

or double-click 

    "type": "mouse_event",
    "content": {
        "mouse_event": "double_click",
        "details": {
            "from_x": 100,
            "from_y": 400,
            "to_x": 200,
            "to_y": 300
        }
    }
    
or selection 

    "type": "mouse_event",
    "content": {
        "mouse_event": "select",
        "details": {
            "from_x": 100,
            "from_y": 400,
            "to_x": 200,
            "to_y": 300
        }
    }
    
#### 3. keyboard_event
Compulsory: **keyboard_event**, the value must be one of **edit_text, key_pressed, multiple_keys_pressed**
Optional: **details**

    "type": "keyboard_event",
    "content": {
        "keyboard_event": "edit_text",
        "details": {
            "before": "text before editing",
            "after": "the edited text"
         }
    }

or 

    "type": "keyboard_event",
    "content": {
        "keyboard_event": "key_pressed",
        "details": {
            "key": 30,
            "duration": 10,
            "hold": ["ctrl", "shift"]
        }
    }


#### 4. browser_event
Compulsory: **browser_event**, the value must be one of **change_tab, clipboard, scroll**
Optional: **details**
    
    "type": "browser_event",
    "content": {
        "browser_event": "change_tab",
        "details": {
            "url_before": "this is the url of the previous tab"
            "url_after": "this is the url of the current tab"
        }
    }
    
or 

    "type": "browser_event",
    "content": {
        "browser_event": "clipboard",
        "details": {
            "type": "paste",
            "value": "the content goes here"
        }
    }
	
#### 5. html_element
Compulsory: **html_event**, the value must be one of **focus, click, hover, drag, change_value**
Optional: **details**

    "type": "html_event",e
    "content": {
        "html_event": "focus",
        "details": {
            "element_tag": "section",
            "element_id": "product_detail"
            "element_class": ["active", "left"]
        }
    }
	
or	

	"type": "html_event",
    "content": {
        "html_event": "click",
        "details": {
            "element_tag": "input",
            "element_id": "product_detail"
            "element_class": ["active", "left"]
        }
    }

