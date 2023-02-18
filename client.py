#!/bin/python3

from serial import Serial
ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate = 38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = 10
)
ser.write(b'"<<SENDFILE>>\n"') #tell server we are ready to recieve
readline = lambda : iter(lambda:ser.read(1),"\n")
with open("sometext.txt","wb") as outfile:
   while True:
       line = "".join(readline())
       if line == "<<EOF>>":
           break #done so stop accumulating lines
       print >> outfile,line