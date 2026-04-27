from robodk import robolink    
from robodk import robomath    
RDK = robolink.Robolink()

import paho.mqtt.client as mqtt  # type: ignore[reportMissingImports]

import RobotController as rc  # type: ignore[reportMissingImports]

broker = "mqtt.dsic.upv.es"
port = 1883
user = "giirob"
passwd = "UPV2024"
base_topic = "giirob/pr2/station/"
station_name = "demo"
station_commands_topic = base_topic+station_name+"/commands"
station_status_topic = base_topic+station_name+"/status"


def on_message(mqttc, obj, msg):
    payload = msg.payload.decode('utf-8')
    topic = msg.topic
    qos = msg.qos
    rc.handle_message(mqttc, topic, payload)

var_mqtt = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
var_mqtt.on_message = on_message

var_mqtt.username_pw_set(username = user, password = passwd)
var_mqtt.connect(broker, port, 60)
var_mqtt.subscribe(station_commands_topic, 0)

var_mqtt.publish(station_status_topic, "ready")

var_mqtt.loop_forever()


def handle_message(mqttc, topic, payload):

    if topic == "giirob/pr2/demo/commands":
        pass




