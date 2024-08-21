#!/usr/bin/env python3
#################################################################
#####     LIGHT CONTROL | IOT REALY LIGHT CONTROLLER        #####
#####     AUTHOR: GARRETT PETER BARDINI (GPB)               #####
#####     CREATE_DATE: 2024/08/10                           #####
#####     LAST_MODIFIED: 2024/08/21                         #####
#################################################################
import time
import datetime
import board
from digitalio import DigitalInOut, Direction

startTime = '20:00'
endTime = '8:00'

pin = board.D14
power = DigitalInOut(pin)
power.direction = Direction.OUTPUT
power.value = False
print("POWER OFF")

startHour = int(startTime.split(':')[0])
startMinute = int(startTime.split(':')[1])
endHour = int(endTime.split(':')[0])
endMinute = int(endTime.split(':')[1])
while True:
    now = datetime.datetime.now()
    start = now.replace(hour=startHour)
    start = start.replace(minute=startMinute)
    end = now.replace(hour=endHour)
    end = end.replace(minute=endMinute)
    if end < start:
        # print("ERROR: Start time must be less than end time")
        if (start <= now) | (end >= now) & (power.value == False):
            print("POWER ON 1")
            power.value = True
        elif (now > end) & (power.value == True):
            print("POWER OFF 1")
            power.value = False
    elif start < end :
        if (start <= now) & (end >= now) & (power.value == False):
            print("POWER ON 2")
            power.value = True
        elif (now > end) & (power.value == True):
            print("POWER OFF 2")
            power.value = False
    time.sleep(10)