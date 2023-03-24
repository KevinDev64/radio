#!/bin/python3

# Подключаем библиотеки
import time
import serial
import button
import os
import subprocess
from systemd.daemon import notify, Notification

stop_var = False     # Переменная остановки залипания кнопки
send = False         # Переменная состояния отправки

# Инициализируем SerialPort

ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate = 38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = 1
)

# Функция отправки
def send_file():
    print("I sending...")
    with open("record.bin", "rb") as file:
        data = file.readlines()                  # Читаем строки в файле и записываем как список в переменную
        for string in data:                      # Перебираем строки в списке
            ser.write(string)                    # Отправляем строку
    ser.write(b'\nEOF')                          # Когда передача завершена, отправляем EOF (конец передачи)
  
# Функция получения  
def recieve_file():
    print("I receving...")
    with open("sound.bin", "wb") as file:        # Открываем файл на запись
        while True:                              # Уходим в вечный цикл приёма
            data = ser.readline()                # Читаем строку из эфира и записываем в переменную
            if data == b'EOF':                   # Если получили EOF, то возвращаем ИСТИНУ (т.к. приём файл прошёл успешно)
                return True
                break
            elif data != b'':                    # Если строка не пустая и не равна EOF, то пишем эту строку в файл
                print("OHH! I recieved ->", data)
                file.write(data)
            else:                                # Иначе (строка пустая) возвращаем ЛОЖЬ (т.к. мы ничего не приняли)
                return False
                break
            
    
    
notify(Notification.READY) # Уведомляем systemd, что всё хорошо

# Главный цикл программы
while True:
    if button.is_pressed(23):
        
        if stop_var == False and send == False:
            print("Pressed!")
            stop_var = True   # Запрещаем залипание
            send = True       # Т.к. мы отправляем файл, меняем переменную
            
            subprocess.Popen(["/bin/arecord", "-D", "plughw:CARD=Device,DEV=0", "-f", "S16_LE", "-r" "48000", "-t", "raw", "record.raw"])   # Запись файла
        else:
            pass
        
    if not(button.is_pressed(23)) and send == True:
        print("Button not pressed! Sending...!")
        os.system("killall -s 9 arecord")    # Останавливаем запись, если кнопка была отпущена и мы в это время отправляли
        os.system("c2enc 1600 record.raw record.bin") # Кодируем файл
        os.remove("record.raw")  # Удаляем оригинальную запись
        
        send_file()              # Отправляем файл
        
        os.remove("record.bin")
        
        send = False             # После отправки меняем переменную, т.к. передача завершена
        stop_var = False         # Разрешаем нажимать кнопку
        
    if not(button.is_pressed(23)) and send == False:
        if not(recieve_file()):  # Если ничего нет в эфире, то пропускаем
            pass
        else:                    # Как только появились данные после приёма, сразу декодируем их и воспроизводим
            os.system("c2dec 1600 sound.bin sound.raw")   # Декодируем
            os.remove("sound.bin")                        # Удаляем закодированный файл
            os.system("aplay -D plughw:CARD=Device,DEV=0 -f S16_LE -r 48000 -t raw sound.raw")  # Воспроизводим декодированный файл
            os.remove("sound.raw")                                  # Удаляем декодированный файл
        

