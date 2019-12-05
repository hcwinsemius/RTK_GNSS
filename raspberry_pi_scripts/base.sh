#!/bin/bash

# Startup script for a Raspberry Pi Zero connected by USB or jumpercables
# (UART) to a uBlox ZED-F9P GNSS receiver.
# Checks for the presense of serial ports /dev/ttyS0 and /dev/ttyACM0.
# If it finds them, checks for incoming data. If it finds incoming data
# launches the str2str utility from RTKLIB to create a .ubx-format GNSS log.
# Loops 10 times to check for the presence of serial devices and incoming data.
# No verification of baud rate, or if the data is garbage, or anything other
# than the presence of incoming bits.
# Sleeps 30 seconds between tries.


sleep 10
# Put a blank line in the log
echo >> ~/log.txt

# Log function makes it easier to write to the log with date/time prepended.
log () { 
    echo "$(date) $1" >> ~/log.txt 
}

log "Hi, starting base.sh"

# Takes a device name (without "/dev/" prepended) as argument.
checkstream () {
    device=$1
    devicedata=
    log "Checking for presence of $device"
    if [ -c /dev/$device ]
    then
	log "$device present, checking for incoming data stream"
	read devicedata < /dev/$device
	if [ ! -z $devicedata ]
	then
	    log "Stream data coming through $device."
	else
	    log "$device is present but no data is coming from it"
	fi
    else
	log "$device is not present or is inaccessible"
    fi
}

# Expecting user to ssh into the Pi and use tail -f log.txt.
echo >> ~/log.txt
log "Started base.sh, sleeping 1 minute"
sleep 60

# Can't return values from Bash functions so here are global variables (sorry).
device=
devicedata=

for i in {9..0}
do
    for dev in "fakedevice" "ttyS0" "ttyACM0" #TODO remove fakedevice
    do
	device=$dev
	checkstream $device
	if [ ! -z $devicedata ]
	then
	    ~/RTKLIB-rtklib_2.4.3/app/str2str/gcc/str2str -in serial://$device:115200:8:n:1:off -out file:///home/pi/base_log_%Y_%m_%d_%h_%M.ubx::S=24 &
	    exit 0
	else
	fi
    done
    log "Sleeping for 30 seconds before trying again $i more times."
    sleep 30
done

exit 0

# For use if base station is streaming to an Internet-based NTRIP caster.
#log "Streaming to NTRIP caster"
#/home/pi/RTKLIB-demo5/app/str2str/gcc/str2str -in serial://ttyACM0:115200:8:n:1:off -out ntrips://:BETATEST@rtk2go.com:2101/HOT_TZ_003:"DarEsSalaam;;;;;;TZA;;" &
