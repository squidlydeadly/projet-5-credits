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

broker = '10.42.0.1'
port = 1883

HUMANITY_1 = 'HUMANITY_1'
HUMANITY_2 = 'HUMANITY_2'
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



    j0 = joysticks[0]
    print('using %d' % j0.device_number)
    battery = j0.get_battery_information()
    print(battery)

    @j0.event
    def on_button(button, pressed):
        print('humanity 1 button:', button, pressed)
        payload = json.dumps({"button" : button, "value": pressed } )
        client.publish(HUMANITY_1, payload)
        time.sleep(0.1)

    @j0.event
    def on_axis(axis, value):
        left_speed = 0
        right_speed = 0
        print('axis', axis, round(value*1000))
        if abs(value *1000) >= 10:
            if axis == "left_trigger":
                left_speed = value
            elif axis == "right_trigger":
                right_speed = value
            payload = json.dumps({"axis" : axis, "value": round(value*1000)} )
            client.publish(HUMANITY_1, payload)





    j1 = joysticks[1]
    print('using %d' % j1.device_number)
    battery = j1.get_battery_information()
    print(battery)

    @j1.event
    def on_button(button, pressed):
        print('humanity 2 button:', button, pressed)
        payload = json.dumps({"button" : button, "value": pressed } )
        client.publish(HUMANITY_2, payload)
        time.sleep(0.1)

    @j1.event
    def on_axis(axis, value):
        left_speed = 0
        right_speed = 0
        print('axis', axis, round(value*1000))
        if abs(value *1000) >= 10:
            if axis == "left_trigger":
                left_speed = value
            elif axis == "right_trigger":
                right_speed = value
            payload = json.dumps({"axis" : axis, "value": round(value*1000)} )
            client.publish(HUMANITY_2, payload)



    while True:
        j0.dispatch_events()
        j1.dispatch_events()

        time.sleep(.01)
        if client.is_connected():
           
            print("disconnected")

if __name__ == "__main__":
    sample_first_joystick()
    determine_optimal_sample_rate()