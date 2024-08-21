# Environment Sensor | Raspberry Pi # 

## Purpose ## 
The purpose of this project is to utilize a Raspberry Pi to retreive and store temperature, humidity, and LUX (unit of illuminance) as time series data. Host this data locally as a webserver so that users can view and interact with this data. 

This project has expanded to include a camera for timealpse and real time viewing. This project has also expanded to include an OLED display to view data in near real time without having to visit the website. 

This repo contains all the python scripts and STL files utilized for this project. 
## Components ## 
### Raspberry Pi 4 ModelB ###
Any Raspberry Pi with a current rasbian distro should work. Installing XRDP (remote desktop) makes communication with the Rasberry Pi significantly easier. 
![GPIO Pinout!](https://i.pinimg.com/originals/78/71/2d/78712d34559353e662bbe2c767ce4702.png "GPIO Pinout")
### DHT11 Temperature and Humidity Sensor ### 
![Wiring Diagram!](https://www.thegeekpub.com/wp-content/uploads/2019/05/Using-the-DHT11-Temperature-Sensor-with-the-Raspberry-Pi-DHT11-DHT22-Module-Wiring-Diagram.jpg "Wiring Diagram")
### BH1750FVI Light Sensor ### 
![Wiring Diagram!](https://i1.wp.com/www.pibits.net/wp-content/uploads/2016/09/PI-AND-bh1750_bb.png?resize=500%2C1024 "Wiring Diagram")
### LCD OLED Display Board Module 12864 (white) ### 
![Wiring Diagram!](https://1.bp.blogspot.com/-yoz8zAb34HM/XnN0l9CfE8I/AAAAAAABOsw/UTQzuACNbhY2mn8__NOVGAFUZZHweb-mwCLcBGAsYHQ/s1600/rpi_bb.png "Wiring Diagram")
Note: the Light Sensor and the OLED Display use the same GPIO pins on the Rasberry Pi. The I2C protocol has the ability to receive many data streams at the same time. This means that you can splice the SDA and SCL wires. Additionally, the power load is low enought that you can also splice the 3.3v power (GPIO pin 17) and ground wires to reduce complexity and improve cable management. 

### Digital Loggers IOT Relay ### 
![Wiring Diagram!](https://support.rfwel.com/galleryDocuments/edbsne8e36e5f37badc7a1ede4d71fbb845a13ee94b3c0151edadf5ffcac52570f3376b956a57dbe2dbc90142ba1394741459?inline=true "Wiring Diagram")

Remove the green Phoenix connector by pulling gently. It slides out horizontally. Use the screw terminals to attach two wires, -GROUND and +TRIGGER. In this case I used GPIO pin 20 for the ground and GPIO pin 14 for the trigger. 
### 4GB USB Flash Drive ### 
Any flash drive or external hard drive will work. It is not best to store the time series sensor data to the operating SD card. This could lead to a data overflow which could coroupt the SD card. 
### BrosTrend USB Wifi Adapter ###
Any Rasberry Pi or linux capable device should work. Make sure you check, not all Wifi extenders are compatable. 
### Arducam 2MP Infrared USB2.0 ### 
Any USB camera should work. Make sure that it will be compatable. 

## Raspberry Pi Set Up ## 
### Update Hostname ### 
	
	hostname
	sudo nano /etc/hostname
	sudo reboot

 * Menu>Preferances>Pasberry Pi configuration> Enter new Hostname
### Update Device ### 
	sudo apt update -y 
	sudo apt full-upgrade -y
	sudo apt autoremove -y
	sudo apt clean -y 
### Set Static IP Address ### 
https://www.tomshardware.com/how-to/static-ip-raspberry-pi

	sudo nano /etc/dhcpcd.conf

Add these lines of text to the end of the dhcpcd.conf file

	interface wlan0
	static routers=10.0.0.1
	static domain_name_servers=10.0.0.1
	static ip_address=10.0.0.15/24

Save and exit the dhcpcd.conf file and reboot to fetch assigned IP address
	
	sudo reboot

Check the the IP address is the one you assigned 

	hostname -I

### Install Software for BrosTrend USB Wifi Adapter ### 
Run the following code to install the USB Wifi adapter

	sh -c 'wget deb.trendtechcn.com/installer.sh -O /tmp/installer.sh && sh /tmp/installer.sh'

### Disable Onboard Wifi ###
	sudo nano /boot/config.txt
Find the following line:

 * "Additional overlays and parameters are documented /boot/overlays/README"

And add these two lines below 

	dtoverlay=disable-wifi
	dtoverlay=disable-bt

### Auto-Mount USB Drive ###
https://www.shellhacks.com/raspberry-pi-mount-usb-drive-automatically/

	sudo mkdir /mnt/usb0
	sudo cp /etc/fstab /etc/fstab.back
	sudo nano /etc/fstab
Add this line to the end of the fstab file 

	UUID=58B5-F0CA /mnt/usb0 vfat defaults,auto,users,rw,nofail,umask=000 0 0
Reboot to save changes 

	sudo reboot
Navigate to the location /mnt/usb0 to check that the USB Drive mounts automatically on boot

### Enable I2C ### 
This step is required to receive data over SDA and SCL<br>
https://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi/

	sudo raspi-config
 * Select "Interface Options"<br>
 * Highlight the "I2C" option and activate "Select"<br>
 * Select and activate "Yes"<br>
 * Reboot if prompted<br>

Confirm I2C is enabled:<br>
 * Menu>Prefrences>Rasberry Pi Configuration>Interfaces>I2C -> Enabled

Install I2C utilities

	sudo apt-get update
	sudo apt-get install -y python3-smbus i2c-tools
	sudo halt

Once the Rasberry PI is shut down now you are ready to connect your I2C hardware

Check if I2c is working 

	i2cdetect -y 1
### Install SSH ### 
Install SSH so files can be coppied from the Rasberry PI to other devices on the Wifi network

	sudo apt install openssh-server
	systemctl status ssh
	sudo service ssh start

## Python Scrpits ## 

### Move the python scripts to these respective folders ### 
* /home/GPI/Documents/OLEDDisplay/OLEDDisplay.py
* /home/Hostname/Documents/EnvironmentSensor/EnvironmentSensor.py
* /home/Hostname/Documents/EnvironmentSensor/ImageCapture.py
* /home/Hostname/Documents/EnvironmentServer/EnvironmentServer.py
* /home/Hostname/Documents/LightControl/LightControl.py

### Run the following commands to install the required dependencies ### 
	pip install Adafruit_GPIO
	pip install adafruit-circuitpython-dht
	pip install plotly
	sudo apt install python3-opencv
	pip install opencv-python

### Optional ###
	sudo apt install ttf-mscorefonts-installer

## Create Services to Start Scripts on Boot ##
### OLED Display ###
Create Service

	sudo nano /lib/systemd/system/OLEDDisplay.service
Add the text

	[Unit]
	Description=OLEDDisplay
	After=network.target
	[Service]
	ExecStart=/usr/bin/python3 /home/Hostname/Documents/OLEDDisplay/OLEDDisplay.py
	Restart=always
	User=Hostname 
	[Install]
	WantedBy=multi-user.target
Enable the service

	sudo systemctl enable OLEDDisplay.service
Start the service

	sudo service OLEDDisplay start
	
Check the status of the service

	sudo service OLEDDisplay status
### Environment Sensor ###
Create Service

	sudo nano /lib/systemd/system/EnvironmentSensor.service
Add the text

	[Unit]
	Description=EnvironmentSensor
	After=network.target
	[Service]
	ExecStart=/usr/bin/python3 /home/Hostname/Documents/EnvironmentSensor/EnvironmentSensor.py
	Restart=always
	User=Hostname 
	[Install]
	WantedBy=multi-user.target
Enable the service

	sudo systemctl enable EnvironmentSensor.service
Start the service

	sudo service EnvironmentSensor start

Check the status of the service

	sudo service EnvironmentSensor status

Stop service

	sudo service EnvironmentSensor stop

### Image Capture ###
Create Service

	sudo nano /lib/systemd/system/ImageCapture.service
Add the text

	[Unit]
	Description=ImageCapture
	After=network.target
	[Service]
	ExecStart=/usr/bin/python3 /home/Hostname/Documents/EnvironmentSensor/ImageCapture.py
	Restart=always
	User=Hostname 
	[Install]
	WantedBy=multi-user.target
Enable the service

	sudo systemctl enable ImageCapture.service
Start the service

	sudo service ImageCapture start

Check the status of the service

	sudo service ImageCapture status

Stop service

	sudo service ImageCapture stop

### Environment Server ###
Create Service

	sudo nano /lib/systemd/system/EnvironmentServer.service
Add the text

	[Unit]
	Description=EnvironmentServer
	After=network.target
	[Service]
	ExecStart=/usr/bin/python3 /home/Hostname/Documents/EnvironmentServer/EnvironmentServer.py
	Restart=always
	User=Hostname 
	[Install]
	WantedBy=multi-user.target
Enable the service

	sudo systemctl enable EnvironmentServer.service
Start the service

	sudo service EnvironmentServer start

Check the status of the service

	sudo service EnvironmentServer status

Stop service

	sudo service EnvironmentServer stop

### LIGHT CONTROLLER ###
Create Service

	sudo nano /lib/systemd/system/LightControl.service
Add the text

	[Unit]
	Description=LightControl
	After=network.target
	[Service]
	ExecStart=/usr/bin/python3 /home/Hostname/Documents/LightControl/LightControl.py
	Restart=always
	User=Hostname 
	[Install]
	WantedBy=multi-user.target
Enable the service

	sudo systemctl enable LightControl.service
Start the service

	sudo service LightControl start

Check the status of the service

	sudo service LightControl status

Stop service

	sudo service LightControl stop
