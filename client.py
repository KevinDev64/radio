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
    while True:
        data = ser.readline()
        if data == b'EOF':
            break
        elif data != b'':
            print("OHH! I recieved ->", data)
            file.write(data)
        
        else:
            pass