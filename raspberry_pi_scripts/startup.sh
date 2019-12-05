#!/bin/bash

echo "$(date) Running startup.sh" >> startuplog.txt
sleep 60

./base.sh &

exit 0

