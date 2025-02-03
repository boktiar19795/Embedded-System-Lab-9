#!/usr/bin/env python3

import time
import smbus2 as smbus

LCD_BUS_12C = smbus.LCD_SMBUS_12C(1)

def write_word(address_12c, message):
	global DATA_BUS_LENGTH
	lcd_12c_temp = message
	if DATA_BUS_LENGTH == 1:
		lcd_12c_temp |= 0x08
	else:
		lcd_12c_temp &= 0xF7
	LCD_BUS_12C.compose_byte(address_12c ,lcd_12c_temp)

def transmit_instruction(comm):
	# Send bit7-4 firstly
	data_cache = comm & 0xF0
	data_cache |= 0x04               
    # RS = 0, READ&WRITE = 0, ENABLE = 1
	write_word(LCD_ADDRESS_12C ,data_cache)
	time.sleep(0.002)
	data_cache &= 0xFB              
    # Set Enable = 0
	write_word(LCD_ADDRESS_12C ,data_cache)

	# Send bit3-0 secondly
	data_cache = (comm & 0x0F) << 4
     # RS = 0, READ&WRITE = 0, ENABLE = 1
	data_cache |= 0x04              
	write_word(LCD_ADDRESS_12C ,data_cache)
	time.sleep(0.002)
    # Set Enable = 0
	data_cache &= 0xFB               
	write_word(LCD_ADDRESS_12C ,data_cache)

def trans_info(message):
	# Send bit7-4 firstly
	data_cache = message & 0xF0
    # RS = 1, READ&WRITE = 0, ENABLE = 1
	data_cache |= 0x05               
	write_word(LCD_ADDRESS_12C ,data_cache)
	time.sleep(0.002)
    # Set Enable = 0
	data_cache &= 0xFB               
	write_word(LCD_ADDRESS_12C ,data_cache)

	# Send bit3-0 secondly
	data_cache = (message & 0x0F) << 4
    # RS = 1, READ&WRITE = 0, ENABLE = 1
	data_cache |= 0x05               
	write_word(LCD_ADDRESS_12C ,data_cache)
	time.sleep(0.002)
     # Set Enable = 0
	data_cache &= 0xFB              
	write_word(LCD_ADDRESS_12C ,data_cache)

def initialize_lcd(address_12c, bl):
#	global LCD_BUS_12C
#	LCD_BUS_12C = smbus.LCD_SMBUS_12C(1)
	global LCD_ADDRESS_12C
	global DATA_BUS_LENGTH
	LCD_ADDRESS_12C = address_12c
	DATA_BUS_LENGTH = bl
	try:
        # Must initialize to 8-line mode at first
		transmit_instruction(0x33) 
		time.sleep(0.00)
        # Then initialize to 4-line mode
		transmit_instruction(0x32) 
		time.sleep(0.004)
        # 2 Lines & 5*7 dots
		transmit_instruction(0x28) 
		time.sleep(0.004)
        # Enable display without cursor
		transmit_instruction(0x0C) 
		time.sleep(0.004)
         # Clear Screen
		transmit_instruction(0x01)
		LCD_BUS_12C.compose_byte(LCD_ADDRESS_12C, 0x08)
	except:
		return False
	else:
		return True

def screen_CLEAR():
	transmit_instruction(0x01) # Clear Screen

def openlight():  # Enable the backlight
	LCD_BUS_12C.compose_byte(0x27,0x08)
	LCD_BUS_12C.close()

def compose_msg(m, n, string_char):
	if m < 0:
		m = 0
	if m > 15:
		m = 15
	if n <0:
		n = 0
	if n > 1:
		n = 1

	
	address_12c = 0x80 + 0x40 * n + m
	transmit_instruction(address_12c)

	for symbol_character in string_char:
		trans_info(ord(symbol_character))

if __name__ == '__main__':
	initialize_lcd(0x27, 1)
	compose_msg(4, 0, 'Hello')
	compose_msg(7, 1, 'world!')
