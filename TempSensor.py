#!/usr/bin/env python
#Stolen from https://www.sunfounder.com/learn/sensor-kit-v2-0-for-raspberry-pi-b-plus/lesson-26-ds18b20-temperature-sensor-sensor-kit-v2-0-for-b-plus.html
#Logan Stoll added the LCD interface
#----------------------------------------------------------------
#	Note:
#		ds18b20's data pin must be connected to pin7.
#		replace the 28-XXXXXXXXX as yours.
#----------------------------------------------------------------
#SIG to #4
#VCC to 5.0 Volts
#GND to GND
#----------------------------------------------------------------
import socket
import os
import subprocess
import time
import os
import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
lcd = LCD.Adafruit_CharLCDPlate()
SERVERIP = "10.0.0.22"
n = 0


ds18b20 = ''

def setup():
	global ds18b20
	for i in os.listdir('/sys/bus/w1/devices'):
		if i != 'w1_bus_master1':
			ds18b20 = i

def read():
#	global ds18b20
	location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
	tfile = open(location)
	text = tfile.read()
	tfile.close()
	secondline = text.split("\n")[1]
	temperaturedata = secondline.split(" ")[9]
	temperature = float(temperaturedata[2:])
	temperature = temperature / 1000
	return temperature

def loop():
	global n
	while True:
		if read() != None:
			Celsius = read()
			Fahrenheit = 9.0/5.0 * Celsius + 32
			print "Current temperature : %0.3f F" % Fahrenheit
			Output_String = "Temp is: \n %.1f Fahrenheit" % Fahrenheit
			time.sleep(.1)
			lcd.message(Output_String)
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((SERVERIP,8881))
			print "%d : Connected to server" % n,
			data = "'Logan-Stoll', %d , %0.3f F" % (n, Fahrenheit)
			sock.sendall(data)
			print " Sent :", data
			sock.close( )
			n += 1
			time.sleep(20)
			lcd.clear()
			continue


def destroy():
	pass

if __name__ == '__main__':
	try:
		setup()
		loop()
	except KeyboardInterrupt:
		destroy()

