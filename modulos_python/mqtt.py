"""Este módulo realiza las conexiones al broker MQTT para
suscribirse a los topics necesarios y recibir/enviar mensajes.

Aún no se ha integrado con la estación de RoboDK."""

from robodk import robolink    
from robodk import robomath    
RDK = robolink.Robolink()

import paho.mqtt.client as mqtt  # type: ignore[reportMissingImports]

broker = "192.168.1.153"
port = 1883
user = "giirob"
passwd = "UPV2024"

# topics que hay en el config.h del firmware_esp32
hello_topic = "giirob/pr2/devices/hello"
button_topic = "giirob/pr2/devices/button"
emergency_stop_topic = "giirob/pr2/devices/emergency_stop"


def recibir_menssage(mqttc, obj, msg):
    """Decodifica el mensaje y delega la acción al controlador."""
    payload = msg.payload.decode('utf-8')
    topic = msg.topic
    qos = msg.qos

    handle_message(mqttc, topic, payload)

var_mqtt = None
def conectar():
    global var_mqtt
    var_mqtt = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    var_mqtt.on_message = recibir_menssage

    var_mqtt.username_pw_set(username = user, password = passwd)
    var_mqtt.connect(broker, port, 60)

    var_mqtt.subscribe(hello_topic, 0)
    var_mqtt.subscribe(button_topic, 0)
    var_mqtt.subscribe(emergency_stop_topic, 0)

    var_mqtt.publish(hello_topic, "Hola desde la simulacion de RoboDK en python")

    var_mqtt.loop_start()

def enviar_message(topic, mensaje : str):
    global var_mqtt

    if var_mqtt is None:
        raise Exception("mqtt no conectado")

    var_mqtt.publish(topic, mensaje)


def handle_message(mqttc, topic, payload):
    """Este método gestiona las acciones que hara la estacion con los 
    robots al recibir ciertos mensajes por cada topic correspondiente"""
    
    if topic == emergency_stop_topic and payload == "STOP":
        # hacer que pare la simulacion
        robomath.pause(100000)




