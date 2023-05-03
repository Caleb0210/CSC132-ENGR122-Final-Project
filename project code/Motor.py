import RPi.GPIO as GPIO
import requests
import time

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

enA = 13
in1 = 12
in2 = 26

GPIO.setup(enA, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)

pwm = GPIO.PWM(enA, 100)
pwm.start(0)

def open():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    pwm.ChangeDutyCycle(100)
    time.sleep(3)
    pwm.ChangeDutyCycle(0)

def close():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    pwm.ChangeDutyCycle(100)
    time.sleep(3)
    pwm.ChangeDutyCycle(0)

while True:
    response = requests.get("https://www.protohacks.net/LATech/AutomaticFeeder/read.php").text
    if response == "1":
        open()
    elif response == "2":
        close()
    time.sleep(1)