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
alsa_args = "-f S16_LE -r 48000"
key = 'qwerty0000'

elements = [speed, port, parity, stopbits, bytesize, button, led, speaker, mic, codec2, alsa_args, key]
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
    data = [speed, port, parity, stopbits, bytesize, button, led, speaker, mic, codec2, alsa_args, key] 
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
    4. Stop Bits
    5. Byte Size

    ------ GPIO PINS ------
    6. Button GPIO Pin
    7. Led GPIO Pin

    -------- SOUND --------
    8. PCM of Speaker By Name(ALSA)
    9. PCM of Microphone By Name(ALSA)
    10. Codec2 bitrate
    11. Arguments for alsa when recording/playback
    
    ------- SECURITY -------
    12. Encryption Key

    ------ FUNCTIONS ------
    13. Update Software
    14. SAVE CHANGES
    15. EXIT
    """)
    inp = input(">>> ")
    
    if inp == "1":
        os.system("clear")
        print("UART Baud Rate")
        print("-" * 20)
        print("\nDefault -> 38400")
        print("NOW -> {}".format(data[0]))
        uart_inp = input("""Enter a new value(number) or enter "cancel" to cancel >>> """)
        if uart_inp == "cancel":
            os.system("clear")
        else:
            try:
                uart_inp = int(uart_inp)
            except:
                print("\nERROR: You entered something other than a number!\nPress Enter to continue...")
                input()
                os.system("clear")
            else:
                data[0] = uart_inp
                print("\nSUCCESS! Press Enter to continue")
                input()
                os.system("clear")
    
    if inp == "2":
        os.system("clear")
        print("Serial Device File (/dev)")
        print("-" * 20)
        print("NOW -> {}".format(data[1]))
        dev_file_inp = input("""Enter a new value(full path) or enter "cancel" to cancel >>> """)
        if dev_file_inp == "cancel":
            os.system("clear")
        else:
            data[1] = dev_file_inp
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
        print("\nDefault -> N")
        print("\nNOW -> {}".format(data[2]))
        parity_inp = input("""Enter a new value(letter) or enter "cancel" to cancel >>> """)
        if parity_inp == "cancel":
            os.system("clear")
        elif parity_inp in available:
            data[2] = parity_inp
            print("\nSUCCESS! Press Enter to continue")
            input()
            os.system("clear")
        else:
            print("\nERROR: You entered an invalid value!\nPress Enter to continue...")
            input()
            os.system("clear")
    
    if inp == "4":
        os.system("clear")
        print("Stop Bits")
        print("-" * 20)
        print("\nDefault -> 1")
        print("NOW -> {}".format(data[3]))
        stopbits_inp = input("""Enter a new value(number) or enter "cancel" to cancel >>> """)
        if stopbits_inp == "cancel":
            os.system("clear")
        else:
            try:
                stopbits_inp = int(stopbits_inp)
            except:
                print("\nERROR: You entered something other than a number!\nPress Enter to continue...")
                input()
                os.system("clear")
            else:
                data[3] = stopbits_inp
                print("\nSUCCESS! Press Enter to continue")
                input()
                os.system("clear")
                
    if inp == "5":
        os.system("clear")
        print("Byte Size")
        print("-" * 20)
        print("\nDefault -> 8")
        print("NOW -> {}".format(data[4]))
        bytesize_inp = input("""Enter a new value(number) or enter "cancel" to cancel >>> """)
        if bytesize_inp == "cancel":
            os.system("clear")
        else:
            try:
                bytesize_inp = int(bytesize_inp)
            except:
                print("\nERROR: You entered something other than a number!\nPress Enter to continue...")
                input()
                os.system("clear")
            else:
                data[4] = bytesize_inp
                print("\nSUCCESS! Press Enter to continue")
                input()
                os.system("clear")
                
    if inp == "6":
        os.system("clear")
        print("Button GPIO Pin")
        print("-" * 20)
        print("\nDefault -> 23")
        print("NOW -> {}".format(data[5]))
        button_pin_inp = input("""Enter a new value(number) or enter "cancel" to cancel >>> """)
        if button_pin_inp == "cancel":
            os.system("clear")
        else:
            try:
                button_pin_inp = int(button_pin_inp)
            except:
                print("\nERROR: You entered something other than a number!\nPress Enter to continue...")
                input()
                os.system("clear")
            else:
                data[5] = button_pin_inp
                print("\nSUCCESS! Press Enter to continue")
                input()
                os.system("clear")
                
    if inp == "7":
        os.system("clear")
        print("LED GPIO Pin")
        print("-" * 20)
        print("\nDefault -> 26")
        print("NOW -> {}".format(data[6]))
        led_pin_inp = input("""Enter a new value(number) or enter "cancel" to cancel >>> """)
        if led_pin_inp == "cancel":
            os.system("clear")
        else:
            try:
                led_pin_inp = int(led_pin_inp)
            except:
                print("\nERROR: You entered something other than a number!\nPress Enter to continue...")
                input()
                os.system("clear")
            else:
                data[6] = led_pin_inp
                print("\nSUCCESS! Press Enter to continue")
                input()
                os.system("clear")

    if inp == "8":
        os.system("clear")
        print("PCM of Speaker By Name(ALSA)")
        print("-" * 20)
        print("Example -> plughw:CARD=Device,DEV=0")
        print("NOW -> {}".format(data[7]))
        speaker_alsa_name_inp = input("""Enter a new value(alsa name) or enter "cancel" to cancel >>> """)
        if speaker_alsa_name_inp == "cancel":
            os.system("clear")
        else:
            data[7] = speaker_alsa_name_inp
            print("\nSUCCESS! Press Enter to continue")
            input()
            os.system("clear")
            
    if inp == "9":
        os.system("clear")
        print("PCM of Microphone By Name(ALSA)")
        print("-" * 20)
        print("Example -> plughw:CARD=Device,DEV=0")
        print("NOW -> {}".format(data[8]))
        mic_alsa_name_inp = input("""Enter a new value(alsa name) or enter "cancel" to cancel >>> """)
        if mic_alsa_name_inp == "cancel":
            os.system("clear")
        else:
            data[8] = mic_alsa_name_inp
            print("\nSUCCESS! Press Enter to continue")
            input()
            os.system("clear")
    
    if inp == "10":
        available = ['3200', '2400', '1600', '1400', '1300', '1200', '700C', '450', '450PWB']
        os.system("clear")
        print("Codec2 Bitrate")
        print("-" * 20)
        print("""Available:
    3200
    2400
    1600
    1400
    1300
    1200
    700C
    450
    450PWB""")
        print("\nDefault -> 3200")
        print("NOW -> {}".format(data[9]))
        codec2_bitrate_inp = input("""Enter a new value(bitrate) or enter "cancel" to cancel >>> """)
        if codec2_bitrate_inp == "cancel":
            os.system("clear")
        elif codec2_bitrate_inp in available:
            data[9] = codec2_bitrate_inp
            print("\nSUCCESS! Press Enter to continue")
            input()
            os.system("clear")
        else:
            print("\nERROR: You entered an invalid value!\nPress Enter to continue...")
            input()
            os.system("clear")
            
    if inp == "11":
        os.system("clear")
        print("Arguments for alsa when recording/playback")
        print("-" * 30)
        print("NOW -> {}".format(data[10]))
        alsa_args_inp = input("""Enter a new value(string of args) or enter "cancel" to cancel >>> """)
        if alsa_args_inp == "cancel":
            os.system("clear")
        else:
            data[10] = alsa_args_inp
            print("\nSUCCESS! Press Enter to continue")
            input()
            os.system("clear")
    
    if inp == "12":
        os.system("clear")
        print("Encryption Key")
        print("-" * 20)
        print("""ATTENTION! If the encryption key is too complex, 
the data transmission time will be increased. 
At the same time, a simple key exposes your data to hacking.""")
        print("-" * 20)
        print("NOW -> {}".format(data[11]))
        key_inp = input("""Enter a new value(encryption key) or enter "cancel" to cancel >>> """)
        if key_inp == "cancel":
            os.system("clear")
        else:
            data[11] = key_inp
            print("\nSUCCESS! Press Enter to continue")
            input()
            os.system("clear")
        
    if inp == "13":
        # UPDATE SOFTWARE
        pass
    
    if inp == "14":
        file = open("config", "w")
        for element in data:
            file.write(str(element))
            file.write("\n")
        file.close()                
        print("SUCCESS! Press Enter to continue...")
        input()
        
    if inp == "15":
        os.system("clear")
        print("Goodbye!")
        exit()
        
    os.system("clear")