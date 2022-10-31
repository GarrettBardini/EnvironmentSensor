# Environment Sensor | Raspberry Pi # 

## Purpose ## 
The purpose of this project is to utilize a Raspberry Pi to retreive temperature, humidity and lumens to store this data and host it in a way users can view this data. 
This project has expanded to include a camera for timealpse. 

## Components ## 
### Raspberry Pi 4 ModelB ###
I recommend installing remote desktop so your interaction with this device is not limited to ssh. 
### DHT11 Temperature and Humidity Sensor ###
![Wiring Diagram!](https://www.thegeekpub.com/wp-content/uploads/2019/05/Using-the-DHT11-Temperature-Sensor-with-the-Raspberry-Pi-DHT11-DHT22-Module-Wiring-Diagram.jpg "Wiring Diagram")
### BH1750FVI Light Sensor ### 
![Wiring Diagram!](https://i1.wp.com/www.pibits.net/wp-content/uploads/2016/09/PI-AND-bh1750_bb.png?resize=500%2C1024 "Wiring Diagram")
### 4GB USB Flash Drive ### 
### BrosTrend USB Wifi Adapter ###
### Arducam 2MP Infrared USB2.0 ### 


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
