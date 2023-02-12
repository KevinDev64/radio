#!/bin/python3

import  RPi.GPIO as GPIO
import time

def is_pressed(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    inputValue = GPIO.input(pin)
    if (inputValue == False):
        return True
    else:
        return False

if __name__ == "__main__":    
    a = int(input())
    print(is_pressed(a))
