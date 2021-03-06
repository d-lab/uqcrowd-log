# User Manuals 

1. Installation Guide
1. Start and Stop Server
1. Export and Import Data


## Installation Steps
This document is written for ubuntu server, the commands may be difference in various Operating System.

**1. Install dependency**
    
    apt-get install python-pip
    pip install redis elasticsearch flask


**2. Clone the source code**

    cd /opt/
    git clone https://github.com/d-lab/uqcrowd-log.git


## Start and Stop the Server
We can start the backend using the command **python <logger-script> <listening-port>**, the listening port must match the
reverse proxy configuration.

For example: the following commands will start 04 parallel backends which listen on port 5001 to 5004

    python /opt/uqcrowd-log/logger.py 5001 &
    python /opt/uqcrowd-log/logger.py 5002 &
    python /opt/uqcrowd-log/logger.py 5003 &
    python /opt/uqcrowd-log/logger.py 5004 &

There already two bash scripts provided to automatically start and stop 08 difference,
these backends can be easily start and stop by running two commands:

    # Stop all the Loggers
    /opt/uqcrowd-log/stop.sh
    # Start the Loggers
    /opt/uqcrowd-log/start.sh
    
*Note: the logger-start.sh script will take no action if there are running backends*
    
## Scheduled Jobs System Monitoring

There are some cron jobs which installed on the server to monitor the services and backends.
If the elasticsearch server is not running or the server can not handle the requests, it will automatically send
a slack message to channel #system-notification to CrowOnTour Slack Team

    # make sure the loggers are started every hour (in case the server is restarted)
    30 *    * * *   root    /opt/uqcrowd-log/start.sh
    
    # check the elasticsearch service every 5 mins
    */5 *   * * *   root    lsof -Pni | grep LISTEN | grep 9200 || echo [WARNING] Elasticsearch Problem! | python /opt/tools/send-slack-message.py
    
    # check the logger service every 5 mins
    */5 *   * * *   root    curl http://localhost:443/logger/insert -I -s | grep "METHOD NOT ALLOWED" || echo [WARNING] Service Problem! | python /opt/tools/send-slack-message.py

*Note: The send-slack-message.py script is located in /opt/tools/ directory*

## Export and Import Data

**1. Export data from elasticsearch**
    
    python /opt/uqcrowd-log/export.py filename.jl

**2. (NEW) Export data from elasticsearch (tom-200109)**

Step (1/2) change the parameters (you can Google "vim" or "vi" to see how to use the editor in linux, such as insert, save, etc.)

    sudo vi /opt/uqcrowd-log/exportParameters.json
    
    # { "your_filename": <the file name you want to save>,
    #   "experiment_id": <experiment ID your want to export>,
    #   "start_time": 1578202000632,
    #   "end_time": 1588213632000 }

1. *If experiment_id is provided, both start_time and end_time will be skipped*
1. *If we want to select by time (not experiment_id), then experiment_id should be set as NULL using double quote (i.e., "")*
1. *Both start_time and end_time are in milliseconds. If time=1578202632 (in seconds), then add "000" to change it to milliseconds (i.e., time=1578202632000)*

Step (2/2) run the following script

    sudo python /opt/uqcrowd-log/tomExport.py

*Then the exported file should be in /opt/uqcrowd-log/exportLogFile/*

**3. Import the data into elasticsearch**

    python /opt/uqcrowd-log/import.py filename.jl
