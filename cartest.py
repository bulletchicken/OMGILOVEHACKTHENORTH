from serial import Serial
import os

import subprocess
ser = Serial('/dev/cu.usbserial-1110', 9600)
#data = ser.readline().decode().strip()

while(True):

    ser.write(input().encode())
