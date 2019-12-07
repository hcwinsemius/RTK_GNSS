#!/bin/bash
#set -e

# Startup script for a Raspberry Pi Zero connected by USB or jumpercables
# (UART) to a uBlox ZED-F9P GNSS receiver.
#
# Checks for the presense of serial devices /dev/ttyS0 and /dev/ttyACM0.
# If it finds them, launches str2str utility from RTKLIB to create .ubx log.
# Checks if that log is growing. If yes, quits. If no, retries several times.

# Make it easier to write to the log with date/time prepended.
log () { 
    echo "$(date) $1"
}

log "Starting base.sh"

# Expecting user to ssh into the Pi and use tail -f log.txt.
log "Started base.sh, sleeping 1 minute"
sleep 60

# Can't return values from Bash functions so here are global variables (sorry).
device=
devicedata=
outfile=
success=

for i in {4..0}
do
    for dev in "fakedevice" "ttyACM0" "ttyS0" #TODO remove fakedevice
    do
	device=$dev
	if [ -c "/dev/$device" ]
	then
	    outfile="/home/pi/base_log_$(date "+%Y_%m_%d_%H_%M").ubx"
	    log "Attempting to launch log from $device"
	    ~/RTKLIB-rtklib_2.4.3/app/str2str/gcc/str2str -in serial://$device:115200:8:n:1:off -out file://$outfile::S=24 &
	else
	    log "$device is not present or is inaccessible"
	fi
	if [ -f "$outfile" ]
	then
	    log "$outfile created, checking to see if it's growing"
	    oldfilesize=$(stat -c%s "$outfile")
	    sleep 10
	    newfilesize=$(stat -c%s "$outfile")
	    log "Started at $oldfilesize and after 10 seconds $newfilesize"
	    if [ $newfilesize -gt $oldfilesize ]
	    then
		log "$outfile is growing. Survey in progress."
		exit 0
	    else
		log "Nope, it is not growing, let us try again"
		rm $outfile
	    fi
	fi    
    done
    log "Sleeping for 30 seconds before trying again $i more times."
    sleep 30
done

log "Was not able to start a stream, giving up."

exit 0

# For use if base station is streaming to an Internet-based NTRIP caster.
#log "Streaming to NTRIP caster"
#/home/pi/RTKLIB-demo5/app/str2str/gcc/str2str -in serial://ttyACM0:115200:8:n:1:off -out ntrips://:BETATEST@rtk2go.com:2101/HOT_TZ_003:"DarEsSalaam;;;;;;TZA;;" &
