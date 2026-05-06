"""Este módulo contiene las funciones necesarias para
simular el movimiento de los objetos sobre las cintas.

Queda por decidir si el duplicado de objetos se implementa aquí o en otro sitio."""

import threading
from robodk import robolink
from robodk import robomath
from modulos_python import variables as var
from modulos_python import simulation as sim
from modulos_python import mqtt, bbdd

def _mover_cinta(cinta_name, param_sensor, frame_name: str, objeto_plantilla : str | None = None, RDK : robolink.Robolink | None = None):
    """Mueve una cinta mientras el sensor no detecte ningún objeto.

    Si no se recibe un Robolink, crea una conexión local para permitir
    mover varias cintas en paralelo."""

    if RDK is None:
        RDK = robolink.Robolink()
    
    cinta = RDK.Item(cinta_name, robolink.ITEM_TYPE_ROBOT)
    if not cinta.Valid():
        raise RuntimeError("El nombre de la cinta no existe")

    incremento = 15.0
    distancia = 0.0
    espacio_objetos = 1000

    while param_sensor is not None and int(RDK.getParam(param_sensor) or 0) != 1:
        
        cinta.setJoints(cinta.Joints() + robomath.Mat([[incremento]]))
        distancia += incremento

        if objeto_plantilla and distancia >= espacio_objetos:
            sim.duplicar_objeto(objeto_plantilla, frame_name)
            distancia = 0.0
        
        robomath.pause(0.01)

def mover_cinta_larga():
    """Método que mueve la cinta por donde pasan las planchas largas, 
    y el sensor encargado de notificar si hay objeto es el SensorCL"""
    
    
    _mover_cinta(var.cinta_larga, "SensorCL", "FramePlanchaLarga", var.plantilla["larga"])

def mover_cinta_ancha():
    """Método que mueve la cinta por donde pasan las planchas anchas, 
    y el sensor encargado de notificar si hay objeto es el SensorCA"""
    
    
    _mover_cinta(var.cinta_ancha, "SensorCA", "FramePlanchaAncha", var.plantilla["ancha"])

def mover_cinta_tapa():
    """Método que mueve la cinta por donde pasan las tapas, 
    y el sensor encargado de notificar si hay objeto es el SensorTapa"""
    

    _mover_cinta(var.cinta_tapa, "SensorTapa","FrameTapa", var.plantilla["tapa"])

def mover_cinta_main(RDK : robolink.Robolink):
    """Método que mueve la cinta principal, donde van las planchasLargas2 
    y planchasAnchas2. El sensor encargado de notificar si hay objeto es el SensorCC.

    Implementa una espera digital que se activa cuando el yaskawa pone una plancha prensada en la cinta"""

    sim.waitDI("enCintaMain", 1)
    sim.setDO("enCintaMain", 0)
    
    _mover_cinta(var.cinta_main, "SensorCC", "FramePlanchaMain", RDK=RDK)

def mover_cinta_cuadro_acabada():
    """Mueve la cinta final donde salen los cuadros eléctricos hacia el túnel.

    Implementa una espera digital que se activa cuando el ABB paletizado
    pone el cuadro con tapa en la cinta. Falta la lógica para detenerse
    2 segundos en el túnel de etiquetado."""

    sim.waitDI("EnCintaEtiquetar", 1)
    sim.setDO("EnCintaEtiquetar", 0)
        
    _mover_cinta(var.cinta_etiqueta, "SensorEtiqueta", "FrameCuadroAcabada")
    
    mqtt.enviar_message(mqtt.led_topic, "ON")

    threading.Thread(target=bbdd.actualizar_unidad).start()