# Environment Sensor | Raspberry Pi # 

## Purpose ## 
The purpose of this project is to utilize a Raspberry Pi to retreive temperature, humidity and lumens to store this data and host it in a way users can view this data. 
This project has expanded to include a camera for timealpse. 

## Components ## 
### Raspberry Pi 4 ModelB ###
I recommend installing remote desktop so your interaction with this device is not limited to ssh. 
![GPIO Pinout!](https://i.pinimg.com/originals/78/71/2d/78712d34559353e662bbe2c767ce4702.png "GPIO Pinout")
### DHT11 Temperature and Humidity Sensor ### 
![Wiring Diagram!](https://www.thegeekpub.com/wp-content/uploads/2019/05/Using-the-DHT11-Temperature-Sensor-with-the-Raspberry-Pi-DHT11-DHT22-Module-Wiring-Diagram.jpg "Wiring Diagram")
### BH1750FVI Light Sensor ### 
![Wiring Diagram!](https://i1.wp.com/www.pibits.net/wp-content/uploads/2016/09/PI-AND-bh1750_bb.png?resize=500%2C1024 "Wiring Diagram")
### 4GB USB Flash Drive ### 
Any flash drive or external hard drive will work. It will not be best to store this data to the operating SD card. 
### BrosTrend USB Wifi Adapter ###
Any Rasberry Pi or linux capable device should work. Make sure you check not all Wifi extenders are compatable. 
### Arducam 2MP Infrared USB2.0 ### 
Any USB camera should work. Make sure that it will be compatable. 

## Raspberry Pi Set Up ## 
### Enable I2C ### 
Prefrences> Rasberry Pi Configuration> Interfaces> I2C -> Enabled
### Install Software for BrosTrend USB Wifi Adapter ### 
	sh -c 'wget deb.trendtechcn.com/installer.sh -O /tmp/installer.sh && sh /tmp/installer.sh'
### Disable Onboard Wifi ###
	sudo nano /boot/config.txt
Find the following line:
"Additional overlays and parameters are documented /boot/overlays/README "
And add these two lines under it

	dtoverlay=disable-wifi
	dtoverlay=disable-bt
### Auto-Mount USB Drive ###
https://www.shellhacks.com/raspberry-pi-mount-usb-drive-automatically/
	sudo cp /etc/fstab /etc/fstab.back
	sudo nano /etc/fstab
	UUID=58B5-F0CA /mnt/usb0 vfat defaults,auto,users,rw,nofail,umask=000 0 0
### INSTALL SSH ### 
	sudo apt install openssh-server
	systemctl status ssh
	sudo service ssh start

## Start Scripts on Boot ## 
Create Service
	sudo nano /lib/systemd/system/EnvironmentSensor.service
Add the text
	[Unit]
	Description=EnvironmentServer
	After=network.target
	[Service]
	ExecStart=/usr/bin/python3 /home/PI/Documents/EnvironmentSensor/EnvironmentSensor.py
	Restart=always
	User=PI 
	[Install]
	WantedBy=multi-user.target
Enable the service
	sudo systemctl enable EnvironmentSensor.service
Chech the status of the service
	sudo systemctl status EnvironmentSensor.service

For the most convenience create services for all the python scripts:
EnvironmentSensor.py
EnvironmentServer.py
ImageCapture.py