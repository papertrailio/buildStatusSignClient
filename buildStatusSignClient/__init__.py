import RPi.GPIO as GPIO
import time
import pyrebase

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

OFF = 'OFF'
ON = 'ON'
FLASH = 'FLASH'

pins = {
    'webslient': [
        {
            'green': {'pin': 7, 'state': OFF},
            'amber': {'pin': 11, 'state': OFF},
            'red': {'pin': 12, 'state': OFF}
        },
        {
            'green': {'pin': 13, 'state': OFF},
            'amber': {'pin': 15, 'state': OFF},
            'red': {'pin': 16, 'state': OFF}
        },
    ],
    'api': [
        {
            'green': {'pin': 18, 'state': OFF},
            'amber': {'pin': 22, 'state': OFF},
            'red': {'pin': 23, 'state': OFF}
        },
        {
            'green': {'pin': 26, 'state': OFF},
            'amber': {'pin': 29, 'state': OFF},
            'red': {'pin': 32, 'state': OFF}
        },
    ],
    'ptapp': [
        {
            'green': {'pin': 33, 'state': OFF},
            'amber': {'pin': 35, 'state': OFF},
            'red': {'pin': 36, 'state': OFF}
        },
        {
            'green': {'pin': 37, 'state': OFF},
            'amber': {'pin': 38, 'state': OFF},
            'red': {'pin': 40, 'state': OFF}
        },
    ]
}

for key, project in pins.iteritems():
    for build in project:
        for color, value in build.iteritems():
            GPIO.setup(value["pin"], GPIO.OUT)
            GPIO.output(value["pin"], GPIO.HIGH)

config = {
    "authDomain": "buildstatussign.firebaseapp.com",
    "databaseURL": "https://buildstatussign.firebaseio.com",
    "apiKey": "AIzaSyBKSq7AaHLrp4PPj3l54LBFza3HFWXO8f4",
    "storageBucket": "buildstatussign.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()


def resetPinsForProject(projectName):
    for build in pins[projectName]:
        for color in build.iteritems():
            build[color]["state"] = OFF
            GPIO.output(value["pin"], GPIO.LOW)


def setPinStates(projectName, projectStates):
    resetPinsForProject(projectName)


def stream_handler(message):
    statuses = db.child("statuses").get()
    for project in statuses.each():
        print(project.key())  # Morty
        print(project.val())
        print('data', project.key(), project.val())
        setPinStates(project.key(), project.val())
        print('pins', pins)


def streamData():
    db.child("statuses").stream(stream_handler)


def run():
    streamData()

    # while True:

    #     for pin in pins:
    #         GPIO.output(pin, GPIO.HIGH)

    #     time.sleep(3)

    #     for pin in pins:
    #         GPIO.output(pin, GPIO.LOW)
