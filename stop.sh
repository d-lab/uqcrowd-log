#!/bin/sh
ps -ef | grep python | grep logger.py | awk '{print $2}' | xargs kill -9
ps -ef | grep logger.py | grep -v grep || echo Stopped!
