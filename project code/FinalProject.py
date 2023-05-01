# IR sensor
import RPi.GPIO as GPIO

#importing the library of RPi.GPIO

import time

#importing the library of time

sensor = 16

#declaring BCM pin 16 which is GPIO 23 of Raspberry Pi

led = 18

#declaring BCM pin 18 which is GPIO 24 of Raspberry Pi

GPIO.setmode(GPIO.BOARD)

#declaring the BCM mode of pins

GPIO.setup(sensor,GPIO.IN)

#set the behaviour of sensor as input

GPIO.setup(led,GPIO.OUT)

#set the behaviour of led as output

try:

while True:

#initiated a infinite while loop

if GPIO.input(sensor):

#checking input on sensor

GPIO.output(led, False)

#led turned on

while GPIO.input(sensor):

#checking input on sensor again

time.sleep(0.2)

#generate time delay of 0.2 seconds

else:

GPIO.output(led,True)

#led turned off if there is no input on sensor

except KeyboardInterrupt:

#if any key is pressed on keyboard terminate the program

GPIO.cleanup()

#cleanup the GPIO pins for any other program use







#API
