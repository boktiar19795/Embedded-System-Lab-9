#!/usr/bin/env python3

from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
from sys import version_info
import time

if version_info.major == 3:
    keyboar_input = input
def print_instructions():
    print ("========================================")
    print ("|                LCD1602               |")
    print ("|    ------------------------------    |")
    print ("|         GND connect to PIN 6         |")
    print ("|         VCC connect to PIN 2         |")
    print ("|         SDA connect to PIN 3         |")
    print ("|         SCL connect to PIN 5         |")
    print ("|                                      |")
    print ("|           Control LCD1602            |")
    print ("|                                      |")
    print ("|                              You Zhou|")
    print ("========================================\n")
    print ("Program is running...")
    print ("Please press Ctrl+C to end the program...")
    keyboar_input ("Press Enter to begin\n")

lcd_12c = LCD()
def secure_exit(signum, frame):
    exit(1)

signal(SIGTERM, secure_exit)
signal(SIGHUP, secure_exit)

def main():
    print_instructions()
    msg_display = "you did good job"
    start_index = 0
    while True:
        if start_index + 16 < len(msg_display):
            lcd_12c.message(msg_display[start_index:start_index+16],1)
        if start_index + 16 >= len(msg_display):
            remaining_text = msg_display[start_index:len(msg_display)]
            padding = 16 - len(remaining_text)
            lcd_12c.message(remaining_text + '   ' + msg_display[0:padding], 1)
        if start_index == len(msg_display):
            start_index = -1
        start_index += 1
        time.sleep(0.5)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        lcd_12c.clear()
