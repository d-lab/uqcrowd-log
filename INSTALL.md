# UQCrowd-Log Installation Guide

## Overall Diagram

The UQCrowd-Logging system uses HAProxy as a reverse proxy to distribute the incoming requests to multiple backends,
the optimized number of backends depends on the server's configuration, 8 is the optimized number for a server
with 40 Core, 60GB of RAM (derived from our performance test). The maximum throughput with the current configuration
 is ~2300 request/s (which can be doubled by adopting a message queue such as Redis)

![](docs/diagram.png)
**Figure 1.** Overall system diagram

_Note: The SSL certificates is handled by the UQ's Front Proxy._

## Installation Steps
This document is written for ubuntu server, the commands may be difference in various Operating System.

**1. Install dependency**
    
    apt-get install python-pip
    pip install redis elasticsearch flask


**2. Clone the source code**

    cd /opt/
    git clone https://github.com/d-lab/uqcrowd-log.git
    

## Start and monitor the system
**1. Start the logger backend**

We can start the backend using the command **python <logger-script> <listening-port>**, the listening port must match the
reverse proxy configuration.

For example: the following commands will start 04 parallel backends which listen on port 5001 to 5004

    python /opt/uqcrowd-log/logger.py 5001 &
    python /opt/uqcrowd-log/logger.py 5002 &
    python /opt/uqcrowd-log/logger.py 5003 &
    python /opt/uqcrowd-log/logger.py 5004 &

There already two bash scripts provided to automatically start and stop 08 difference,
these backends can be easily start and stop by running two commands:

    /opt/uqcrowd-log/logger-stop.sh
    /opt/uqcrowd-log/logger-start.sh
    
_Note: the logger-start.sh script will take no action if there are running backends_
    
**2. System Monitoring**

There are some cron jobs which installed on the server to monitor the services and backends.
If the elasticsearch server is not running or the server can not handle the requests, it will automatically send
a slack message to channel #system-notification to CrowOnTour Slack Team

    # make sure the loggers are started every hour (in case the server is restarted)
    30 *    * * *   root    /opt/uqcrowd-log/logger-start.sh
    
    # check the elasticsearch service every 5 mins
    */5 *   * * *   root    lsof -Pni | grep LISTEN | grep 9200 || echo [WARNING] Elasticsearch Problem! | python /opt/tools/send-slack-message.py
    
    # check the logger service every 5 mins
    */5 *   * * *   root    curl http://localhost:443/logger/insert -I -s | grep "METHOD NOT ALLOWED" || echo [WARNING] Service Problem! | python /opt/tools/send-slack-message.py

_Note: The send-slack-message.py script is located in /opt/tools/ directory_

