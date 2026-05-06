"""Este módulo realiza las conexiones al broker MQTT para
suscribirse a los topics necesarios y recibir/enviar mensajes. .

Aún no se ha integrado con la estación de RoboDK."""

import json
from robodk import robolink
import paho.mqtt.client as mqtt  # type: ignore[reportMissingImports]
from modulos_python import variables
from modulos_python import bbdd

broker = "broker.emqx.io"
port = 1883
#user = "giirob"
#passwd = "UPV2024"

# topics que hay en el config.h del firmware_esp32
hello_topic = "giirob/pr2/devices/hello"
button_topic = "giirob/pr2/devices/button"
emergency_stop_topic = "giirob/pr2/devices/emergency_stop"

RDK = robolink.Robolink()

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

    #var_mqtt.username_pw_set(username = user, password = passwd)
    var_mqtt.connect(broker, port, 60)

    var_mqtt.subscribe(hello_topic, 0)
    var_mqtt.subscribe(button_topic, 0)
    var_mqtt.subscribe(emergency_stop_topic, 0)

    hello_payload = json.dumps({
        "estado_led": "off",
        "msg": "Hola desde la simulacion de RoboDK en python",
    })
    var_mqtt.publish(hello_topic, hello_payload)
    RDK.ShowMessage("MQTT Conectado AELL", False)

    var_mqtt.loop_start()
    
def enviar_message(topic, mensaje : str):
    global var_mqtt

    if var_mqtt is None:
        raise Exception("mqtt no conectado")

    var_mqtt.publish(topic, mensaje)

def handle_message(mqttc, topic, payload):
    global var_mqtt, _stop_callback
    
    if topic == emergency_stop_topic and payload == "STOP":
        RDK.setSimulationSpeed(0)
        RDK.ShowMessage(f"Mensaje recibido: {payload}", False)
    
    elif topic == emergency_stop_topic and payload == "GO":
        RDK.setSimulationSpeed(5) 
        RDK.ShowMessage("Simulación Reanudado", False)
        


