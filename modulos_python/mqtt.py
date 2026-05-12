"""Este módulo realiza las conexiones al broker MQTT para
suscribirse a los topics necesarios y recibir/enviar mensajes."""

import json
from robodk import robolink
import paho.mqtt.client as mqtt  # type: ignore[reportMissingImports]

broker = "broker.emqx.io"
port = 1883
#user = "giirob"
#passwd = "UPV2024"

# topics que hay en el config.h del firmware_esp32
hello_topic = "giirob/pr2/erro/hello"
led_topic = "giirob/pr2/erro/led"
button_topic = "giirob/pr2/erro/button"
emergency_stop_topic = "giirob/pr2/erro/emergency_stop"

RDK = robolink.Robolink()

def _on_connect(client, userdata, flags, reason_code, properties):
    print(f"MQTT conectado. reason_code={reason_code}", flush=True)

def _on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    print(f"MQTT desconectado. reason_code={reason_code}", flush=True)

def _on_publish(client, userdata, mid, reason_code, properties):
    print(f"MQTT publish ack. mid={mid} reason_code={reason_code}", flush=True)

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
    var_mqtt.on_connect = _on_connect
    var_mqtt.on_disconnect = _on_disconnect
    var_mqtt.on_publish = _on_publish
    var_mqtt.on_message = recibir_menssage

    #var_mqtt.username_pw_set(username = user, password = passwd)
    rc = var_mqtt.connect(broker, port, 60)
    if rc != mqtt.MQTT_ERR_SUCCESS:
        print(f"Error connect MQTT. rc={rc}", flush=True)

    var_mqtt.subscribe(hello_topic, 0)
    var_mqtt.subscribe(button_topic, 0)
    var_mqtt.subscribe(emergency_stop_topic, 0)
    print("Suscrito a topics MQTT")

    hello_payload = json.dumps({
        "msg": "Hola desde la simulacion de RoboDK en python",
    })

    info = var_mqtt.publish(hello_topic, hello_payload)
    if info.rc != mqtt.MQTT_ERR_SUCCESS:
        print(f"Error publish MQTT. rc={info.rc}", flush=True)
    
    RDK.ShowMessage("MQTT Conectado", False)

    var_mqtt.loop_start()
    
def enviar_message(topic, mensaje : str):
    global var_mqtt

    if var_mqtt is None:
        raise Exception("mqtt no conectado")

    var_mqtt.publish(topic, mensaje)

def handle_message(mqttc, topic, payload):
    global var_mqtt, _stop_callback
    print(f"Mensaje recibido. topic={topic} payload={payload}", flush=True)

    if topic == emergency_stop_topic:
        try:
            data = json.loads(payload)
            estado = data.get("estado_simulacion")
            
            if estado == "STOP":
                RDK.setSimulationSpeed(0)
                RDK.ShowMessage(f"EMERGENCIA ACTIVADA: {payload}", False)
            elif estado == "GO":
                RDK.setSimulationSpeed(5)
                RDK.ShowMessage("Simulación Reanudada", False)
        except json.JSONDecodeError:
            if payload == "STOP":
                RDK.setSimulationSpeed(0)
                RDK.ShowMessage(f"EMERGENCIA ACTIVADA: {payload}", False)
            elif payload == "GO":
                RDK.setSimulationSpeed(5)
                RDK.ShowMessage("Simulación Reanudada", False)
        


