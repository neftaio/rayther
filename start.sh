#!/bin/bash
#start supervisord to bring up webserver and sleep to be sure it's up
supervisord -n &
sleep 15

#Run letsencrypt, if the parameters were given.  Output a log of the letsencrypt attempt
if [ -n "$1" ]; then
    python /home/flask/conf/setup-https.py $1 > /home/flask/letsencrypt-setup.txt
fi
