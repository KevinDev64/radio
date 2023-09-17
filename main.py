#!/bin/python3

import time
import serial
import button
import os
import subprocess
from systemd.daemon import notify, Notification

stop_var = False     # button flag
send = False         # status of sending

# Read config
try:
    file = open("config", "r")
    data = file.readlines()
    for i in range(len(data)):
        data[i] = data[i].replace("\n", "")
    file.close()
    print("READ SUCCESSFULLY!")
    # Translates to normal types
    data[0] = int(data[0]) # speed
    data[3] = int(data[3]) # stop bits
    data[4] = int(data[4]) # byte size
    data[5] = int(data[5]) # button pin
    data[6] = int(data[6]) # led pin
    data[9] = int(data[9]) # codec2 arg

except:
    # throw error with led
    pass             
    
else:
    # initialize serial
    ser = serial.Serial(
        port = data[1],
        baudrate = data[0],
        parity = data[2],
        stopbits = data[3],
        bytesize = data[4],
        timeout = 0
    )

    # send function
    def send_file():
        print("I sending...")
        with open("record.gpg", "rb") as file:
            data = file.readlines()                  # Читаем строки в файле и записываем как список в переменную
            for string in data:                      # Перебираем строки в списке
                ser.write(string)                    # Отправляем строку
        ser.write(b'\nEOF')                          # Когда передача завершена, отправляем EOF (конец передачи)
    
    # recieve function 
    def recieve_file():
        print("I receving...")
        with open("sound.gpg", "wb") as file:        # Открываем файл на запись
            while True:                              # Уходим в вечный цикл приёма
                data = ser.readline()                # Читаем строку из эфира и записываем в переменную
                if data == b'EOF':                   # Если получили EOF, то возвращаем ИСТИНУ (т.к. приём файл прошёл успешно)
                    return True
                    break
                elif data != b'':                    # Если строка не пустая и не равна EOF, то пишем эту строку в файл
                    print("I recieved -> ", data)
                    file.write(data)
                else:                                # Иначе (строка пустая) возвращаем ЛОЖЬ (т.к. мы ничего не приняли)
                    return False
                    break
                  
    notify("READY=1") # notifying systemd READY status
    # main loop
    while True:
        if button.is_pressed(data[5]):
            
            if stop_var == False and send == False:
                print("Pressed!")
                stop_var = True  # change flags
                send = True        
                subprocess.Popen(["/bin/arecord", "-D", data[8], data[10], "-t", "raw", "record.raw"])   # Запись файла
            else:
                pass
            
        if not(button.is_pressed(data[5])) and send == True:
            print("Button not pressed! Sending...!")
            os.system("killall -s 9 arecord")    # stop recording
            os.system(f"c2enc {data[9]} record.raw record.bin") # use codec2 to encode
            os.remove("record.raw")  # delete raw record
            os.system(f"gpg --batch --output record.gpg --passphrase {data[11]} --symmetric record.bin") # encrypt record
            os.remove("record.bin")  # delete encode record
            send_file()              # send file
            os.remove("record.gpg")  # delete encrypted record
            
            send = False             # change flags
            stop_var = False         
            
        if not(button.is_pressed(data[5])) and send == False:
            if not(recieve_file()):  # if there is nothing on air then skip this part
                pass
            else:                    # listen data
                os.system(f"gpg --batch --output sound.bin --passphrase {data[11]} --decrypt sound.gpg") # decrypt record
                os.remove("sound.gpg") # delete encrypted record
                os.system(f"c2dec {data[9]} sound.bin sound.raw")   # decode
                os.remove("sound.bin") # delete encode record
                os.system(f"aplay -D {data[7]} {data[10]} -t raw sound.raw")  # play the raw record
                os.remove("sound.raw")   # delete raw record