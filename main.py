#!/bin/python3

""""
Этапы программы:
1) Объявляние частей программы
2) Опрос кнопки по циклу
3) При удержании кнопки запись
4) При отпускании убиваем процесс записи
5) Кодириуем и отправляем
6) Если надо принимаем.
"""

import time
import serial
import button
import os
from systemd.daemon import notify, Notification

stop_var = False
send = False

ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate = 38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = 10
)
def send_file():
    with open("record.bin", "rb") as file:
        data = file.readlines()
        for string in data:
            ser.write(string)
    ser.write(b'\nEOF')
    
def recieve_file():
    with open("sound.bin", "wb") as file:
        while True:
            data = ser.readline()
            if data == b'EOF':
                return True
                break
            elif data != b'':
                print("OHH! I recieved ->", data)
                file.write(data)
            else:
                return False
                break
            
    
    
notify(Notification.READY) # Notify READY state!

while True:
    if button.is_pressed(23):
        if stop_var == False and send == False:
            stop_var = True
            send = True
            
            os.system("arecord -f S16_LE -r 44100 -t raw record.raw")
        else:
            pass
    if not(button.is_pressed(23)) and send == True:
        os.system("killall -s 9 arecord")
        os.system("c2enc 1300 record.raw record.bin")
        os.remove("record.raw")
        
        send_file()
        send = False
        stop_var = False
    if not(button.is_pressed(23)) and send == False:
        if not(recieve_file()):
            pass
        else:
            os.system("c2dec 1300 sound.bin sound.raw")
            os.remove("sound.bin")
            os.system("aplay -f S16_LE -r 44100 -t raw sound.raw")
            os.remove("sound.raw")
        

