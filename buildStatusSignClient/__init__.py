import RPi.GPIO as GPIO
import time
import pyrebase

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

OFF = 'OFF'
ON = 'ON'
FLASH = 'FLASH'

pins = {
    'webclient': [
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
            'green': {'pin': 29, 'state': OFF},
            'amber': {'pin': 31, 'state': OFF},
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
        for colorName, colorState in build.iteritems():
            GPIO.setup(colorState["pin"], GPIO.OUT)
            colorState["state"] = ON

config = {
    "authDomain": "buildstatussign.firebaseapp.com",
    "databaseURL": "https://buildstatussign.firebaseio.com",
    "apiKey": "AIzaSyBKSq7AaHLrp4PPj3l54LBFza3HFWXO8f4",
    "storageBucket": "buildstatussign.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()


def switchGPIOs():
    while True:
        for key, projectData in pins.iteritems():
            for build in projectData:
                for key, colorState in build.iteritems():
                    if colorState["state"] == OFF:
                        GPIO.output(colorState["pin"], GPIO.LOW)
                    else:
                        GPIO.output(colorState["pin"], GPIO.HIGH)


def resetStateForProject(projectName):
    for build in pins[projectName]:
        for key, colorState in build.iteritems():
            print('color state', colorState)
            colorState["state"] = OFF


def setStateForProjectBuild(buildPins, buildBuildState):
    print("setStateForProjectBuild", buildBuildState)

    if buildBuildState == 'success':
        buildPins["green"]["state"] = ON
    else:
        buildPins["green"]["state"] = OFF


def setStateForProjectBuilds(projectName, projectBuildStates):
    setStateForProjectBuild(pins[projectName][0], projectBuildStates[0])
    setStateForProjectBuild(pins[projectName][1], projectBuildStates[1])


def setPinStates(projectName, projectBuilds):
    resetStateForProject(projectName)
    setStateForProjectBuilds(projectName, projectBuilds)


def stream_handler(message):
    statuses = db.child("statuses").get()
    for project in statuses.each():
        setPinStates(project.key(), project.val())


def streamData():
    db.child("statuses").stream(stream_handler)


def run():
    streamData()

    switchGPIOs()
