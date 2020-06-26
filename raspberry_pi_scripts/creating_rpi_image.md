# Create a Raspberry Pi W image for serial logging with u-Blox ZED-F9P

## Steps (draft)

- Download Raspberry Pi OS, flash
- Add empty file called ssh in boot partition
- Modify wpa_supplicant.conf to get on the wifi
- Turn it on, change default password, update/upgrade
- Install Pip
- [Disable login shell over serial, enable serial port hardware](https://www.raspberrypi.org/documentation/configuration/uart.md), reboot
- 