#!/usr/bin/env python3
#################################################################
#####     ENVIRONMENT SENSOR | TEMPERATURE HUMIDITY LUX     #####
#####     AUTHOR: GARRETT PETER BARDINI (GPB)               #####
#####     CREATE_DATE: 2022/09/10                           #####
#####     LAST_MODIFIED: 2022/10/14                         #####
#################################################################
import os
# import Adafruit_DHT
import adafruit_dht
from board import *
#pip3 install adafruit-circuitpython-dht
import smbus
# You need to Enable IC2
import time
import pandas as pd
import datetime
# External Drive # 
workingdir = (r"/mnt/usb0/EnvironmentData")

DHT11_PIN = D4
DHT11_SENSOR = adafruit_dht.DHT11(DHT11_PIN, use_pulseio=False)
DEVICE     = 0x23 # Default device I2C address
ONE_TIME_HIGH_RES_MODE = 0x20
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

def get_temp(df,numtry):
    attempts = 0
    while attempts < numtry:
        try:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %X')
            temp = (((DHT11_SENSOR.temperature) *1.8)+32)
            humidity = DHT11_SENSOR.humidity
            lux = bus.read_i2c_block_data(DEVICE,ONE_TIME_HIGH_RES_MODE)
            lux = ((lux[1] + (256 * lux[0])) / 1.2) # Simple function to convert 2 bytes of data into a decimal number
            if humidity is not None and temp is not None and lux is not None:
                df = df.append({'DateTime':timestamp,'Temperature_F':temp,'Humidity':humidity,'Lux':round(lux,2)}, ignore_index=True)
                return df
        except:
            attempts += 1
            print ('Retry: ' + str(attempts) + '/' +str(numtry))
            time.sleep(1)

if os.path.exists(os.path.join(workingdir,'EnvironmentResults.csv')):
    df = pd.read_csv(os.path.join(workingdir,'EnvironmentResults.csv'))
else:
    df = pd.DataFrame()
    
while True:
    minute = datetime.datetime.now().minute
    min_remainder = minute%10
    if min_remainder == 0:
        df = get_temp(df,5)
        # print(df)
        df.to_csv(os.path.join(workingdir,'EnvironmentResults.csv'),index = False)
        time.sleep(60*8)
        pass
    
    time.sleep(1)
    