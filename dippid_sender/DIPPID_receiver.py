import time
from DIPPID import SensorUDP

#From demo_device.py in the example files

# use UPD (via WiFi) for communication
PORT = 5700
sensor = SensorUDP(PORT)


def print_data(data):
    print(sensor._capabilities)
    print(data)


# register callback (runs in own thread)
sensor.register_callback('accelerometer', print_data)
sensor.register_callback('button_1', print_data)

while True:
    time.sleep(1)



