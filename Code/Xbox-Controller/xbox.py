from xinput import  XInputJoystick
import ctypes
import sys
import time
from operator import itemgetter, attrgetter
from itertools import count, starmap
from pyglet import event

from paho.mqtt import client as mqtt_client
import random
import json

broker = '192.168.0.217'
port = 1883
topic = "desk/light"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


client = connect_mqtt()



def sample_first_joystick():
    """
    Grab 1st available gamepad, logging changes to the screen.
    L & R analogue triggers set the vibration motor speed.
    """
    joysticks = XInputJoystick.enumerate_devices()
    device_numbers = list(map(attrgetter('device_number'), joysticks))


    print('found %d devices: %s' % (len(joysticks), device_numbers))

    if not joysticks:
        sys.exit(0)

    j = joysticks[0]

    print('using %d' % j.device_number)

    battery = j.get_battery_information()
    print(battery)


    @j.event
    def on_button(button, pressed):
        print('button', button, pressed)
        payload = json.dumps({"button" : button, "value": pressed } )
        client.publish("robot/button", payload)

    left_speed = 0
    right_speed = 0

    @j.event
    def on_axis(axis, value):
        left_speed = 0
        right_speed = 0


        print('axis', axis, round(value*1000))
        if axis == "left_trigger":
            left_speed = value
        elif axis == "right_trigger":
            right_speed = value

        #j.set_vibration(left_speed, right_speed)


        payload = json.dumps({"axis" : axis, "value": round(value*1000)} )

        client.publish("robot/axis", payload)

    while True:
        j.dispatch_events()

        time.sleep(.01)
        if client.is_connected():
           
            print("disconnected")

if __name__ == "__main__":
    sample_first_joystick()
    determine_optimal_sample_rate()