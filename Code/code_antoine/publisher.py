from paho.mqtt import client as mqtt_client

import decision
import json


def publish_CommandSkynet(client,commands_skynets):
    for command_skynet in commands_skynets:
        topic = "SKYNET" + str(command_skynet.num)
        command_intensity = command_skynet.get_command_intensity()
        payload = json.dump()
        client.publish(topic,payload)
