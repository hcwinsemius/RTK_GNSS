# Create a Raspberry Pi W image for serial logging with u-Blox ZED-F9P

## Steps (draft)

- Download [Raspberry Pi OS](https://www.raspberrypi.com/software/operating-systems/#raspberry-pi-os-32-bit)
- Download [portable appimage of Balena Etcher](https://etcher.balena.io/#download-etcher), flash the image to the sd card
- Mount and open the SD card, whicch should now have partitions ```rootfs``` and ```bootfs```. Go into ```bootfs```
- In ```bootfs``` create an empty file called ```ssh``` in boot.
- In ```bootfs```, create a file wpa_supplicant.conf with contents:
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=GB

network={
     ssid="your_network_name"
     psk="your_wifi_password"
     key_mgmt=WPA-PSK
}
```
- Put the flashed SD card into the pi, and attach power to the micro-USB port at the end opposite the SD card (the one nearer the middle is for data, you'll need it for the ArduSimple). After a few minutes, if all goes well (not guaranteed) the pi will be on the wifi.
- Find the IP address that the pi has been given using ```nmap``` or ```arp-scan``` (which might go something like ```sudo arp-scan --interface=wlp166s0 --localnet; find out your interface name with ```ip addr show```
```).
- If that worked, you can ssh into the pi. 
- Put the ```log_ubx.py``` script into the ```/rootfs/home/pi/``` directory.
- Create a file called ```/usr/lib/systemd/system/gnss_base.service``` and populate it with
```
[Unit]
Description=GNSS logging
After=multi-user.target

[Service]
ExecStart=/home/pi/log_ubx.py
WorkingDirectory=/home/pi/
User=pi
Restart=on-abort
StandardOutput=file:/home/pi/log.txt
StandardError=file:/home/pi/error.log

[Install]
WantedBy=multi-user.target
```
(or just copy the file from this repo into that location).
- Enable the service with ```sudo systemctl enable gnss_base.service```. Now the Pi should start logging raw satellite data in .ubx format as soon as it starts up. You can recover the data by pulling out the SD card and copying it out of the /home/pi/ directory.


