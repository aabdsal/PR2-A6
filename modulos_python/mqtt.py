"""Este módulo realiza las conexiones al broker MQTT para
suscribirse a los topics necesarios y recibir/enviar mensajes.

Aún no se ha integrado con la estación de RoboDK."""

from robodk import robolink
from robodk import robomath

import paho.mqtt.client as mqtt  # type: ignore[reportMissingImports]

broker = "broker.emqx.io"
port = 1883
#user = "giirob"
#passwd = "UPV2024"

# topics que hay en el config.h del firmware_esp32
hello_topic = "giirob/pr2/devices/hello"
button_topic = "giirob/pr2/devices/button"
emergency_stop_topic = "giirob/pr2/devices/emergency_stop"

_stop_callback = None


def set_stop_callback(callback):
    """Permite registrar una funcion que detenga la ejecucion."""
    global _stop_callback
    _stop_callback = callback


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

    var_mqtt.publish(hello_topic, "Hola desde la simulacion de RoboDK en python")

    var_mqtt.loop_start()
    

def enviar_message(topic, mensaje : str):
    global var_mqtt

    if var_mqtt is None:
        raise Exception("mqtt no conectado")

    var_mqtt.publish(topic, mensaje)


def handle_message(mqttc, topic, payload):
    global var_mqtt
    
    if topic == emergency_stop_topic and payload == "STOP":
        if _stop_callback is not None:
            RDK.ShowMessage(f"Mensaje recibido: {payload}", True)
            _stop_callback()
            return
    elif topic == emergency_stop_topic and payload == "GO":
        print("Emergencia limpia. Reanudando simulación...")
        RDK.setSimulationSpeed(1) # Vuelve a la velocidad normal
        RDK.ShowMessage("Sistema Reanudado", False)


# 1. Creamos la conexión con la aplicación RoboDK abierta
RDK = robolink.Robolink()

# 2. Definimos la función que detiene la estación
def mi_funcion_de_paro():
    print("[ROBODK] ¡ORDEN DE PARO RECIBIDA!")
    
    # ponemos la velocidad a 0
    # Esto congela todos los robots y cintas de la estación
    RDK.setSimulationSpeed(0)
    
    # Mostramos el mensaje en la pantalla de RoboDK
    RDK.ShowMessage("PARADA DE EMERGENCIA: Sistema detenido", False)

# 3. Registramos esta función en el sistema que ya tenías
set_stop_callback(mi_funcion_de_paro)
        

if __name__ == "__main__":
    conectar()



