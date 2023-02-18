#!/bin/python3

from serial import Serial
ser = Serial("/dev/ttyAMA0") #or whatever 
readline = lambda : iter(lambda:ser.read(1),"\n")
while "".join(readline()) != "<<SENDFILE>>": #wait for client to request file
    pass #do nothing ... just waiting ... we could time.sleep() if we didnt want to constantly loop
ser.write(open("sometext.txt","rb").read()) #send file
ser.write("\n<<EOF>>\n") #send message indicating file transmission complete