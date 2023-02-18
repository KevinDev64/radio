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
with open("output.bin", "rb") as file:
    data = file.readlines()
    for string in data:
        print("I sent -> ", string)
        ser.write(string)

ser.write(b'\nEOF')
        