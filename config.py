#!/bin/python3
import serial
import os

speed = 38400
port = "/dev/ttyAMA0"
parity = 'N'
stopbits = 1
bytesize = 8
button = 23
led = 26
speaker = "plughw:CARD=Device,DEV=0"
mic = "plughw:CARD=Device,DEV=0" 
codec2 = 3200
quality = "-f S16_LE -r 48000"

elements = [speed, port, parity, stopbits, bytesize, button, led, speaker, mic, codec2, quality]
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
    file = open("config", "w")               
    data = [speed, port, parity, stopbits, bytesize, button, led, speaker, mic, codec2, quality] 
    for element in data:
        file.write(str(element))
        file.write("\n")
    file.close()                
    print("WRITE SUCCESSFULLY!")
    
print("|-----------------------------------------------------------|")
print("|Welcome to the application for configuring device settings!|")
print("|                                                           |")
print("|   Only change something if you know what you are doing!   |")
print("|                                                           |")
print("|                     Made by KevinDev64                    |")
print("|-----------------------------------------------------------|")
while True:
    print("\nSelect action (enter a number)")
    print("""
    ----- CONNECTION ------
    1. UART Baud Rate
    2. Serial Device File (/dev)
    3. Parity
    4. Byte Size

    ------ GPIO PINS ------
    5. Button GPIO Pin
    6. Led GPIO Pin

    -------- SOUND --------
    7. PCM of Speaker By Name(ALSA)
    8. PCM of Microphone By Name(ALSA)
    9. Codec2 bitrate
    10. Arguments for alsa when recording/playback

    ------ FUNCTIONS ------
    11. SAVE CHANGES
    12. EXIT
    """)
    inp = input(">>> ")
    if inp == "1":
        os.system("clear")
        print("UART BAUD RATE")
        print("-" * 20)
        print("\nRecommended -> 38400")
        print("NOW -> {}".format(data[0]))
        uart = input("""Enter a new value(number) or enter "cancel" to cancel >>> """)
        if uart == "cancel":
            os.system("clear")
        else:
            try:
                uart = int(uart)
            except:
                print("\nERROR: You entered something other than a number!\nPress Enter to continue...")
                input()
                os.system("clear")
            else:
                data[0] = uart
                print("\nSUCCESS! Press Enter to continue")
                input()
                os.system("clear")
    
    if inp == "2":
        os.system("clear")
        print("Serial Device File (/dev)")
        print("-" * 20)
        print("NOW -> {}".format(data[1]))
        dev_file = input("""Enter a new value(full path) or enter "cancel" to cancel >>> """)
        if dev_file == "cancel":
            os.system("clear")
        else:
            data[1] = dev_file
            print("\nSUCCESS! Press Enter to continue")
            input()
            os.system("clear")
    
    if inp == "3":
        available = ['N', 'E', 'O', 'M', 'S']
        os.system("clear")
        print("Parity")
        print("-" * 20)
        print("""Available:
    N. None
    E. Even
    O. Odd
    M. Mark
    S. Space""")
        print("\nNOW -> {}".format(data[1]))
        temp_parity = input("""Enter a new value(letter) or enter "cancel" to cancel >>> """)
        if temp_parity == "cancel":
            os.system("clear")
        elif temp_parity in available:
            data[2] = temp_parity
            print("\nSUCCESS! Press Enter to continue")
            input()
            os.system("clear")
        else:
            print("\nERROR: You entered an invalid value!\nPress Enter to continue...")
            input()
            os.system("clear")
