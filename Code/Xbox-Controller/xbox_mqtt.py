import signal
import  json
import  sys
#pip3 install xbox360controller
from xbox360controller import Xbox360Controller
#pip3 install paho-mqtt
from paho.mqtt import client as mqtt_client

try:
    robot_number = sys.argv[1]
except :
    print("Specify robot name")
    print("1 -> HUMANITY_1")
    print("2 -> HUMANITY_2")
    exit()

robotName = "HUMANITY_" + robot_number

broker = "localhost"
port = 1883
client_id = "CONTROLLER OF " + robotName
keepalive = 5000

def connect_mqtt()-> mqtt_client:
    def on_connect(client,userdata,flags,rc):
        if rc == 0:
            print("connected o mqtt broker")
        else:
            print("connection failed")

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port, keepalive = keepalive)
    return client

client = connect_mqtt()

def on_button_pressed(button):
    print('Button {0} was pressed'.format(button.name))

    payload = json.dumps({"button" : 13, "value" : 1})
    client.publish(robotName, payload)


def on_button_released(button):
    print('Button {0} was released'.format(button.name))
    

def on_axis_moved(axis):
    x_axis = round(axis.x * 500)
    y_axis = round(axis.y * -500)

    if abs(x_axis) <= 150:
        x_axis = 0
    if abs(y_axis) <= 150:
        y_axis = 0

    print('Axis {0} moved to {1} {2}'.format(axis.name, x_axis, y_axis))

    payload = json.dumps({"axis" : axis.name , "x_axis" :x_axis , "y_axis" : y_axis})
    client.publish(robotName, payload)

try:
    with Xbox360Controller(int(robot_number) - 1, axis_threshold=0.2) as controller:
        # Button A events
        controller.button_a.when_pressed = on_button_pressed
        controller.button_a.when_released = on_button_released

        # Left and right axis move event
        controller.axis_l.when_moved = on_axis_moved
        signal.pause()

except KeyboardInterrupt:
    pass