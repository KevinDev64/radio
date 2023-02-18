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
readline = lambda : iter(lambda:ser.read(1),"\n")
while "".join(readline()) != "<<SENDFILE>>": #wait for client to request file
    pass #do nothing ... just waiting ... we could time.sleep() if we didnt want to constantly loop
ser.write(open("sometext.txt","rb").read()) #send file
ser.write("\n<<EOF>>\n") #send message indicating file transmission complete