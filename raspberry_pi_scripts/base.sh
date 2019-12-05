#!/bin/bash

# Startup script for a Raspberry Pi Zero connected by USB or jumpercables
# (UART) to a uBlox ZED-F9P GNSS receiver.
# Checks for the presense of serial ports /dev/ttyS0 and /dev/ttyACM0.
# If it finds them, checks for incoming data. If it finds incoming data
# launches the str2str utility from RTKLIB to create a .ubx-format GNSS log.
# Loops 10 times to check for the presence of serial devices and incoming data.
# Sleeps 30 seconds between tries.

# TODO: currently launches the str2str utility from within checkstream
# function, which is brittle and stupid (and causes the main loop to have
# repetitive code). Should probably fix that to separate the concerns of
# determining if serial data is arriving and where from, and launching the
# actual logging of GNSS information.

# Makes it easier to write to the log with date/time prepended.
log () { 
    echo "$(date) $1" >> ~/log.txt 
}

# Takes a device name (without "/dev/" prepended) as argument.
# Checks for presence of said device, and then checks if it's sending data.
# No verification of baud rate, or if the data is garbage in any way.
# Launches the str2str utility to log data from the device in a .ubx file
# and breaks (stupid way to do it but works for now). 
checkstream () {
    device=$1
    log "Checking for presence of $device"
    if [ -c /dev/$device ]
    then
	log "$device present, checking for incoming data stream"
	read devicedata < /dev/$device
	if [ ! -z $devicedata ]
	then
	    log "Stream data coming through $device"
	    ~/RTKLIB-rtklib_2.4.3/app/str2str/gcc/str2str -in serial://$device:115200:8:n:1:off -out file:///home/pi/base_log_%Y_%m_%d_%h_%M.ubx::S=24 &
	    log "Logging started from $device"
	    # TODO: LIGHT UP GREEN LED
	else
	    log "$device is present but no data is coming from it"
	fi
    fi
}

# Expecting user to be following what's going by ssh'ing into the Pi and
# using tail -f log.txt. So we talk to the user using the log function.
echo >> ~/log.txt
log "Started base.sh, sleeping 1 minute"
sleep 60

# Don't know how to return useful values from Bash functions so here are some
# global variables (sorry)
device=
devicedata=

# TODO make an inner loop that checks all relevant devices in a list
for i in {20..1}
do
    device="ttyS0"
    checkstream $device
    if [ ! -z $devicedata ]
    then
	break
    fi
    
    device="ttyACM0"
    checkstream $device
    if [ ! -z $devicedata ]
    then
	break
    fi

    log "Sleeping 30 seconds before trying again"
    sleep 30   
done

if [ -z devicedata ]
then
    log "Looks like there's no incoming data. Gave up."
fi


#log "Streaming to NTRIP caster"
#/home/pi/RTKLIB-demo5/app/str2str/gcc/str2str -in serial://ttyACM0:115200:8:n:1:off -out ntrips://:BETATEST@rtk2go.com:2101/HOT_TZ_003:"DarEsSalaam;;;;;;TZA;;" &

exit 0
