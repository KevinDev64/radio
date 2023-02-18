#!/bin/python3

import serial
ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate = 38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = 10
)
input("Ready! Press enter to continue!")
with open("sometext.txt", "wb") as file:
    data = ser.readline()
    file.write(data + b"\n")