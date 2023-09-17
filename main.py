#!/bin/python3

try:
    import time
    import serial
    import pin
    import os
    import subprocess
    from systemd.daemon import notify
except:
    # error init libs
    pin.power_off(data[6])
    time.sleep(1)
    for _ in range(5):
        pin.power_on(data[6])
        time.sleep(0.5)    
        pin.power_off(data[6])
        time.sleep(0.5)
    time.sleep(5)
    exit()

stop_var = False     # button flag
send = False         # status of sending

# read config
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
    # config error
    pin.power_off(data[6])
    time.sleep(1)
    for _ in range(3):
        pin.power_on(data[6])
        time.sleep(0.5)    
        pin.power_off(data[6])
        time.sleep(0.5)
    time.sleep(5)
    exit()
    
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
            data = file.readlines()                  # read lines and write into list
            for string in data:                      # select every element in list
                ser.write(string)                    # send string (element)
        ser.write(b'\nEOF')                          # if sending is completed, throw EOF (end of file)
    
    # recieve function 
    def recieve_file():
        print("I receving...")
        with open("sound.gpg", "wb") as file:        # open file in bin read mode
            while True:                              # endless loop for recieve
                data = ser.readline()                # read string from the air
                if data == b'EOF':                   # if recieve EOF, return TRUE (recieving is completed)
                    return True
                    break
                elif data != b'':                    # if string not EOF and not NULL, write this string into file
                    print("I recieved -> ", data)
                    file.write(data)
                else:                                # else (if NULL) return FALSE (because recieving isn't started)
                    return False
                    break
                  
    notify("READY=1") # notifying systemd READY status
    # main loop
    while True:
        if pin.is_pressed(data[5]):
            
            if stop_var == False and send == False:
                print("Pressed!")
                stop_var = True  # change flags
                send = True        
                subprocess.Popen(["/bin/arecord", "-D", data[8], data[10], "-t", "raw", "record.raw"])   # Запись файла
            else:
                pass
            
        if not(pin.is_pressed(data[5])) and send == True:
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
            
        if not(pin.is_pressed(data[5])) and send == False:
            if not(recieve_file()):  # if there is nothing on air then skip this part
                pass
            else:                    # listen data
                os.system(f"gpg --batch --output sound.bin --passphrase {data[11]} --decrypt sound.gpg") # decrypt record
                os.remove("sound.gpg") # delete encrypted record
                os.system(f"c2dec {data[9]} sound.bin sound.raw")   # decode
                os.remove("sound.bin") # delete encode record
                os.system(f"aplay -D {data[7]} {data[10]} -t raw sound.raw")  # play the raw record
                os.remove("sound.raw")   # delete raw record