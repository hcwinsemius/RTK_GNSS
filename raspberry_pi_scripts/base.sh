#!/bin/bash
#set -e

# Startup script for a Raspberry Pi Zero connected by USB or jumpercables
# (UART) to a uBlox ZED-F9P GNSS receiver.
#
# Intended to be run as a service from systemd.
# gnss.service file included in code repo.
#
# Checks for the presense of serial devices /dev/ttyS0 and /dev/ttyACM0.
# If it finds them, launches str2str utility from RTKLIB to create .ubx log.
# Checks if that log is growing. If not, retries forever.

# Make it easier to write to the log with date/time prepended.
# Expecting user to ssh into the Pi and use tail -f log.txt.
log () { 
    echo "$(date) $1"
}

launch () {
    device=$1
    log "Trying with $device"
    if [ -c "/dev/$device" ]
    then
	outfile="/home/pi/base_log_$(date "+%Y_%m_%d_%H_%M").ubx"
	log "Attempting to launch log from $device"
	~/RTKLIB-rtklib_2.4.3/app/str2str/gcc/str2str -in serial://$device:115200:8:n:1:off -out file://$outfile::S=24 &
	sleep 2
	if [ -f "$outfile" ]
	then
	    log "$outfile created from $device, checking if it's growing"
	    oldfilesize=$(stat -c%s "$outfile")
	    sleep 30
	    newfilesize=$(stat -c%s "$outfile")
	    log "Started at $oldfilesize, after 30 seconds $newfilesize"
	    if [ $newfilesize -gt $oldfilesize ]
	    then
		log "$outfile is growing. Survey in progress."
		success=true
	    else
		log "Nope, it is not growing, let us try again"
		success=
	    fi
	fi
    fi
}

log "Started base.sh, sleeping 2 minutes"
sleep 60
log "Still sleeping, 1 more minute"
sleep 60
success=

while true
do
    for dev in "ttyACM0" "ttyS0"
    do
	if [ ! "$success" = true ]
	then
	    launch "$dev"
	fi
    done
    sleep 5
done


		 
	
