# Environment Sensor | Raspberry Pi # 

## Purpose ## 
The purpose of this project is to utilize a Raspberry Pi to retreive temperature, humidity and lumens to store this data and host it in a way users can view this data. 
This project has expanded to include a camera for timealpse. 

## Components ## 
### Raspberry Pi 4 ModelB ###
### DHT11 Temperature and Humidity Sensor ###
### BH1750FVI Light Sensor ### 
![Wiring Diagram!](https://www.raspberrypi-spy.co.uk/wp-content/uploads/2015/03/BH1750-Module-Setup.png "Diagram")
### Arducam 2MP Infrared USB2.0 ### 
### BrosTrend USB Wifi Adapter ###
### 4GB USB Flash Drive ### 

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
