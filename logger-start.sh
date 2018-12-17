#!/bin/sh
for i in $(seq 5001 5008); do
    ps -ef | grep logger.py | grep $i || python /opt/uqcrowd-log/logger.py $i > /dev/null &
done
