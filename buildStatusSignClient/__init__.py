import RPi.GPIO as GPIO
import time


def run():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    pins = [7, 11, 12, 13, 15, 16, 18, 22, 23, 29, 31, 33, 35, 36, 37, 38, 40]

    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)

    for pin in pins:
        GPIO.output(pin, GPIO.HIGH)

    time.sleep(3)

    for pin in pins:
        GPIO.output(pin, GPIO.LOW)
