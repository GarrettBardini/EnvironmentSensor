#!/usr/bin/env python3
#################################################################
#####     OLED DIAPLAY | TEMPERATURE HUMIDITY LUX           #####
#####     AUTHOR: GARRETT PETER BARDINI (GPB)               #####
#####     CREATE_DATE: 2024/07/20                           #####
#####     LAST_MODIFIED: 2024/07/21                         #####
#################################################################
import os
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import adafruit_dht
from board import *
import smbus
# import subprocess

DHT11_PIN = D4
DHT11_SENSOR = adafruit_dht.DHT11(DHT11_PIN, use_pulseio=False)

DEVICE     = 0x23 # Default device I2C address
ONE_TIME_HIGH_RES_MODE = 0x20
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

RST = None # on the PiOLED this pin isnt used
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# INITIALIZE DISPLAY LIBRARY # 
disp.begin()
disp.clear()
disp.display()

# CRATE BLANK IMAGE # 
width = disp.width
height = disp.height
image = Image.new('1', (width, height)) # mode '1' for 1-bit color
draw = ImageDraw.Draw(image)

# DEFINE SHAPE CONSTRAINTS # 
padding = -2
top = padding
bottom = height-padding
x = 0

# LOAD DEFAULT FONT #
# font = ImageFont.load_default()
# ALTERNATIVELY LOAD A TTF FONT # 
font = ImageFont.truetype("arial.ttf", 12)
# OTHER FONTS try: http://www.dafont.com/bitmap.php #
# DEFINE STATUSES FOR TEMP, HUMIDITY, AND LUMINOUS FLUX # 
def GetTempStatus(temp):
    if temp >= 120:
        temp_status = "Extreme"
    elif (temp < 120) & (temp >= 100):
        temp_status = "Very Hot"
    elif (temp < 100) & (temp >= 85):
        temp_status = "Hot"
    elif (temp < 85) & (temp >= 75):
        temp_status = "Warm"
    elif (temp < 75) & (temp >= 65):
        temp_status = "Nice"
    elif (temp < 65) & (temp >= 50):
        temp_status = "Cool"
    elif (temp < 50) & (temp >= 32):
        temp_status = "Cold"
    elif temp < 32:
        temp_status = "Freezing"
    return temp_status

def GetHumidityStatus(humidity):
    if humidity >= 95:
        humidity_status = "Percip"
    elif (humidity < 95) & (humidity >= 80):
        humidity_status = "V High"
    elif (humidity < 80) & (humidity >= 60):
        humidity_status = "High"
    elif (humidity < 60) & (humidity >= 40):
        humidity_status = "Comfort"
    elif (humidity < 40) & (humidity >= 30):
        humidity_status = "Low"
    elif (humidity < 30) & (humidity >= 20):
        humidity_status = "V Low"
    elif humidity < 20:
        humidity_status = "Arid"
    return humidity_status

def GetLuxStatus(lux):
    if lux >= 25000:
        lux_status = "Direct"
    elif (lux < 25000) & (lux >= 10000):
        lux_status = "Full"
    elif (lux < 10000) & (lux >= 1000):
        lux_status = "Bright"
    elif (lux < 1000) & (lux >= 100):
        lux_status = "Light"
    elif (lux < 100) & (lux >= 50):
        lux_status = "Low"
    elif (lux < 50) & (lux >= 20):
        lux_status = "Dim"
    elif lux < 20:
        lux_status = "Dark"
    return lux_status

while True:
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    attempts = 0
    while attempts < 5:
        try:
            temp = (((DHT11_SENSOR.temperature) *1.8)+32)
            humidity = DHT11_SENSOR.humidity
            lux = bus.read_i2c_block_data(DEVICE,ONE_TIME_HIGH_RES_MODE)
            lux = ((lux[1] + (256 * lux[0])) / 1.2) # Simple function to convert 2 bytes of data into a decimal number
            break
        except:
            attempts += 1
            print ('Retry: ' + str(attempts) + '/' +str(5))
            time.sleep(1)

    draw.text((x, top),f"Temp: {temp:,.1f}° {GetTempStatus(temp)}", font=font, fill=255)
    draw.text((x, top+11),f"Humidity: {humidity:,.0f}% {GetHumidityStatus(humidity)}",  font=font, fill=255)
    if lux >= 1000:
        draw.text((x, top+22),f"Lumens: {lux:,.0f} {GetLuxStatus(lux)}",  font=font, fill=255)
    elif (lux < 1000) & (lux >= 50):
        draw.text((x, top+22),f"Lumens: {lux:,.1f} {GetLuxStatus(lux)}",  font=font, fill=255)
    elif lux < 50:
        draw.text((x, top+22),f"Lumens: {lux:,.2f} {GetLuxStatus(lux)}",  font=font, fill=255)

    # DISPLAY IMAGE # 
    disp.image(image)
    disp.display()
    time.sleep(1) # REFRESH RATE # 