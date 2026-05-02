"""Este módulo realiza las conexiones al broker MQTT para
suscribirse a los topics necesarios y recibir/enviar mensajes.

Aún no se ha integrado con la estación de RoboDK.
"""

from robodk import robolink    
from robodk import robomath    
RDK = robolink.Robolink()

import paho.mqtt.client as mqtt  # type: ignore[reportMissingImports]

import RobotController as rc  # type: ignore[reportMissingImports]

broker = "mqtt.dsic.upv.es"
port = 1883
user = "giirob"
passwd = "UPV2024"
base_topic = "giirob/pr2_a6/station/"
station_name = "demo"
station_commands_topic = base_topic+station_name+"/commands"
station_status_topic = base_topic+station_name+"/status"


def on_message(mqttc, obj, msg):
    """Decodifica el mensaje y delega la acción al controlador."""
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
    """Este método gestiona las acciones que hara la estacion con los 
    robots al recibir ciertos mensajes por cada topic correspondiente"""
    
    if topic == station_commands_topic:
        pass
    elif topic == station_status_topic:
        pass




