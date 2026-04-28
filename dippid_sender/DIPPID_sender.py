import socket
import time
import json
import numpy

#Notes:
# Observing the Data in the App, the accelometer when not moving works like a gyroscope

IP = '127.0.0.1'
PORT = 5700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    t = time.time()

    #determines the simulated state, my thoughts were: 
    # mostly sitting/smartphone lying around = 0.65, 
    # looking at resembles average screentime of adult in germany = 3h = 3/24
    # shaking is very rare = 0.05 (could be even lower, but should have a chance to appear in data), 
    # movement isn't very much for a lot of people so.. = 0.175
    currentState = numpy.random.choice(
        a= ["idle", "looking", "shake", "movement"],
        p= [0.65, 0.125, 0.05, 0.175]
    )


    #idle is for simulating laying around, in that case the following ranges were observed
    if currentState == "idle":
        cordinatesNumbers = [
            numpy.random.uniform(-0.1, 0.1), #left/right sway = noise
            numpy.random.uniform(-0.1, 0.1), #up/down angle = noise
            numpy.random.uniform(0, 1) #under the assumption the screen points up, else it would be (-1,0), a range (-1,1) would mean constant flipping of the phone
        ]
    #looking simulates the normal usage, the following ranges were observed (not including laying on the side)
    elif currentState == "looking":
        cordinatesNumbers = [
            numpy.random.uniform(-0.2, 0.2), #left/right sway
            numpy.random.uniform(0.4, 1), #up/down angle, depending on viewing angle
            numpy.random.uniform(0.2, 0.8) #up/down angle
        ]
    #shake simulates light to medium shaking, for light/medium shaking values between 2-5 were common, for heavy shaking values of 6-11
    elif currentState == "shake":
        cordinatesNumbers = [
            numpy.random.uniform(-3.5, 3.5),
            numpy.random.uniform(-3.5, 3.5),
            numpy.random.uniform(-3.5, 3.5)
        ]
    #normal light (caotic) movement
    elif currentState == "movement":
        cordinatesNumbers = [
            numpy.sin(t),
            numpy.sin(t * 0.49),
            numpy.sin(t * 0.31)
        ]

    acceleratorData = {
        "x": cordinatesNumbers[0],
        "y": cordinatesNumbers[1],
        "z": cordinatesNumbers[2]
    }

    data = {
        "accelerometer" : acceleratorData,
        "button_1" : numpy.random.randint(0,2)
    }
    package = json.dumps(data)

    print(currentState)
    print(package)
    sock.sendto(package.encode(), (IP, PORT))

    time.sleep(1) #timing of real sensor is much faster, but for readability kept it at 1