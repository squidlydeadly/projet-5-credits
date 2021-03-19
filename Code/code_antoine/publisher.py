
import json
from paho.mqtt import client as mqtt_client


def publish_CommandSkynet(client,command_skynet):
    topic = "SKYNET_" + str(command_skynet.num)
    command_intensity = command_skynet.get_command_intensity()
    if(command_skynet.kick):
        print(topic + ' kick et bouge ' + str(command_intensity.clockwise_intensity) +', ' +  str(command_intensity.foward_intensity))
        payload = json.dumps({'axis':'skynet',
        'x_axis':command_intensity.clockwise_intensity,
        'y_axis':command_intensity.foward_intensity,
        'button':13})
    else:
        print(topic + ' bouge ' + str(command_intensity.clockwise_intensity) +', ' +  str(command_intensity.foward_intensity))
        payload = json.dumps({'axis':'skynet',
        'x_axis':command_intensity.clockwise_intensity,
        'y_axis':command_intensity.foward_intensity})
    client.publish(topic,payload)

def start_skynet_client():
        port = 1883
        client_id = "CONTROLLER OF SKYNET"
        keepalive = 5000
        broker = "localhost"


        def connect_mqtt()-> mqtt_client:
            def on_connect(client,userdata,flags,rc):
                if rc == 0:
                    print("connected to mqtt broker")
                else:
                    print("connection failed")

            client = mqtt_client.Client(client_id)
            client.on_connect = on_connect
            client.connect(broker, port, keepalive = keepalive)
            return client

        return connect_mqtt()

if __name__ == '__main__':
    import decision
    import time

    commands = [decision.CommandeSkynet(0,angle=90,grandeur=300,kick=True),
                decision.CommandeSkynet(1,angle=30,grandeur=1000,is_clockwise=False,is_foward=False),
                decision.CommandeSkynet(2,angle=40,is_clockwise=False)]
    client = start_skynet_client()
    for command in commands:
        publish_CommandSkynet(client,command)
