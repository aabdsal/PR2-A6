"""Este módulo realiza las conexiones al broker MQTT para
suscribirse a los topics necesarios y recibir/enviar mensajes. .

Aún no se ha integrado con la estación de RoboDK."""

from robodk import robolink
from robodk import robomath

import paho.mqtt.client as mqtt 
from modulos_python import variables
from modulos_python import actualizarBD

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
    global var_mqtt, _stop_callback
    
    # Lógica de parada de emergencia
    if topic == emergency_stop_topic and payload == "STOP":
        if _stop_callback is not None:
            print(f"Mensaje recibido: {payload}")
            _stop_callback()
            return  
    elif topic == emergency_stop_topic and payload == "GO":
        print("Emergencia limpia. Reanudando simulación...")
        RDK.setSimulationSpeed(1) # Vuelve a la velocidad normal
        RDK.ShowMessage("Sistema Reanudado", False)
        
    # Lógica de producto terminado (LED ON)
    elif topic == hello_topic and payload == "on":
        obj_terminado = None
        
        # Buscamos el primer objeto que tenga registrados ambos tiempos
        for nombre_obj, tiempos in variables.tiempos_proceso.items():
            if tiempos.get("ini") is not None and tiempos.get("fin") is not None:
                obj_terminado = nombre_obj
                break # Encontramos la pieza terminada
                
        if obj_terminado:
            t_ini = variables.tiempos_proceso[obj_terminado]["ini"]
            t_fin = variables.tiempos_proceso[obj_terminado]["fin"]
            
            # 1. Enviamos los tiempos a la Base de Datos
            actualizarBD.registrar_producto_terminado(t_ini, t_fin)
            
            # 2. Eliminamos el objeto del diccionario para no volver a procesarlo
            del variables.tiempos_proceso[obj_terminado]
        else:
            print("Aviso MQTT: Se recibió 'on' pero no hay piezas con tiempos de proceso completos.")



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



