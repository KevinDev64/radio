#!/bin/python3

import time 
import serial

ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate = 38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
counter = 0

while 1:
    data = str.encode("Hello, World!")
    ser.write(data)
    print("I sent!")
    time.sleep(3)