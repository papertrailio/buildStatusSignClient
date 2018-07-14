import RPi.GPIO as GPIO
import time
import pyrebase

pins = [7, 11, 12, 13, 15, 16, 18, 22, 23,
        26, 29, 31, 33, 35, 36, 37, 38, 40]

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

config = {
    "authDomain": "buildstatussign.firebaseapp.com",
    "databaseURL": "https://buildstatussign.firebaseio.com",
    "apiKey": "AIzaSyBKSq7AaHLrp4PPj3l54LBFza3HFWXO8f4",
    "storageBucket": "buildstatussign.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()
statuses = db.child("statuses")


def stream_handler(message):
    statuses.get()
    print(statuses.val())
    # print(users.val())
    # print(message["path"])  # /-K7yGTTEp7O549EzTYtI
    # print(message["data"])  # {'title': 'Pyrebase', "body": "etc..."}


def run():
    my_stream = statuses.stream(stream_handler)

    # while True:

    #     for pin in pins:
    #         GPIO.output(pin, GPIO.HIGH)

    #     time.sleep(3)

    #     for pin in pins:
    #         GPIO.output(pin, GPIO.LOW)
