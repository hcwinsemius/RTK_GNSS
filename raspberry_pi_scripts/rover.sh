#! /bin/sh
now=$(date)
echo $now" Started rover.sh, sleeping 3 minutes" >> /home/pi/test.log
sleep 60
echo "Sleeping 2 minutes" >> /home/pi/test.log
sleep 60
echo "Sleeping 1 minute" >> /home/pi/test.log
sleep 60

# Echo "Attempting to receive RTCM information from the NTRIP caster" >> /home/pi/test.log
#sudo /home/pi/RTKLIB-rtklib_2.4.3/app/str2str/gcc/str2str -in ntrip://rtk2go.com:2101/YPEN001 -out serial://ttyACM0:38400 &

now=$(date)
echo $now" Checking for the GPS receiver on port /dev/ttyS0" >> /home/pi/test.log
if [ -c /dev/ttyS0 ] 
    then
	echo "S0 present">>/home/pi/test.log
        /home/pi/RTKLIB-rtklib_2.4.3/app/str2str/gcc/str2str -in serial://ttyS0:460800:8:n:1:off -out file:///home/pi/rover_log_%Y_%m_%d_%h_%M.ubx::S=24 &
    else
        echo $now" Checking for the GPS receiver on port /dev/ttyACM0 (jumper cables)" >> /home/pi/test.log
        if [ -c /dev/ttyACM0 ]
            then
                echo "ACM0 present, beginning log" >> /home/pi/test.log
                /home/pi/RTKLIB-rtklib_2.4.3/app/str2str/gcc/str2str -in serial://ttyACM0:460800:8:n:1:off -out file:///home/pi/rover_log_%Y_%m_%d_%h_%M.ubx::S=24 &
            else
                echo "ACM0 not present" >> /home/pi/test.log
	fi
fi

exit 0
