#!/bin/sh
for i in $(seq 5001 5008); do
    ps -ef | grep logger.py | grep $i || python /opt/uqcrowd-log/logger.py $i > /dev/null &
done

ps -ef | grep analytics.py | grep 6001 || python /opt/uqcrowd-log/analytics.py 6001 > /dev/null &
