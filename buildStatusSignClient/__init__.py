import RPi.GPIO as GPIO
import time
import pyrebase

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

OFF = 'OFF'
ON = 'ON'
FLASH = 'FLASH'

GREEN = 'green'
AMBER = 'amber'
RED = 'red'

FLASH_STATE = OFF

pins = {
    'webclient': [
        {
            GREEN: {'pin': 7, 'state': OFF},
            AMBER: {'pin': 11, 'state': OFF},
            RED: {'pin': 12, 'state': OFF}
        },
        {
            GREEN: {'pin': 13, 'state': OFF},
            AMBER: {'pin': 15, 'state': OFF},
            RED: {'pin': 16, 'state': OFF}
        },
    ],
    'api': [
        {
            GREEN: {'pin': 18, 'state': OFF},
            AMBER: {'pin': 22, 'state': OFF},
            RED: {'pin': 23, 'state': OFF}
        },
        {
            GREEN: {'pin': 29, 'state': OFF},
            AMBER: {'pin': 31, 'state': OFF},
            RED: {'pin': 32, 'state': OFF}
        },
    ],
    'ptapp': [
        {
            GREEN: {'pin': 33, 'state': OFF},
            AMBER: {'pin': 35, 'state': OFF},
            RED: {'pin': 36, 'state': OFF}
        },
        {
            GREEN: {'pin': 37, 'state': OFF},
            AMBER: {'pin': 38, 'state': OFF},
            RED: {'pin': 40, 'state': OFF}
        },
    ]
}

config = {
    "authDomain": "buildstatussign.firebaseapp.com",
    "databaseURL": "https://buildstatussign.firebaseio.com",
    "apiKey": "AIzaSyBKSq7AaHLrp4PPj3l54LBFza3HFWXO8f4",
    "storageBucket": "buildstatussign.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()


def setup():
    for key, project in pins.iteritems():
        for build in project:
            for key, colorState in build.iteritems():
                GPIO.setup(colorState["pin"], GPIO.OUT)
                colorState["state"] = ON

    switchGPIOs(OFF)
    time.sleep(2)


def switchGPIOs(flashState):
    for key, projectData in pins.iteritems():
        for build in projectData:
            for key, colorState in build.iteritems():
                if colorState["state"] == OFF:
                    GPIO.output(colorState["pin"], GPIO.LOW)
                elif colorState["state"] == FLASH:
                    if flashState == OFF:
                        GPIO.output(colorState["pin"], GPIO.LOW)
                    else:
                        GPIO.output(colorState["pin"], GPIO.HIGH)
                else:
                    GPIO.output(colorState["pin"], GPIO.HIGH)


def setStateForProjectBuild(buildPins, buildBuildState):
    if buildBuildState == 'success':
        buildPins[GREEN]["state"] = ON
        buildPins[AMBER]["state"] = OFF
        buildPins[RED]["state"] = OFF
    elif buildBuildState == 'stopped':
        buildPins[GREEN]["state"] = OFF
        buildPins[AMBER]["state"] = ON
        buildPins[RED]["state"] = OFF
    elif buildBuildState == 'testing':
        buildPins[GREEN]["state"] = OFF
        buildPins[AMBER]["state"] = FLASH
        buildPins[RED]["state"] = OFF
    else:
        buildPins[GREEN]["state"] = OFF
        buildPins[AMBER]["state"] = OFF
        buildPins[RED]["state"] = ON


def setStateForProjectBuilds(projectName, projectBuildStates):
    setStateForProjectBuild(pins[projectName][0], projectBuildStates[0])
    setStateForProjectBuild(pins[projectName][1], projectBuildStates[1])


def setPinStates(projectName, projectBuilds):
    setStateForProjectBuilds(projectName, projectBuilds)


def stream_handler(message):
    statuses = db.child("statuses").get()
    for project in statuses.each():
        setPinStates(project.key(), project.val())


def streamData():
    db.child("statuses").stream(stream_handler)


def run():
    setup()
    streamData()
    while True:
        switchGPIOs(ON)
        time.sleep(1)
        switchGPIOs(OFF)
        time.sleep(1)
