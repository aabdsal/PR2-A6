"""Este archivo implementa la lógica para que un sensor detecte objetos."""

from robodk import robolink, robomath    
from modulos_python import variables as var, simulation as sim
from datetime import datetime

def productorEvento(nombre_sensor: str, detectados: list[robolink.Item], RDK : robolink.Robolink):
    if detectados:
        for idx in detectados:
            nombre_obj = idx.Name()
            var.objetos_pendientes[nombre_sensor].put(nombre_obj)
            
            if nombre_sensor == "SensorCA":
                var.tiempo_ini.put(datetime.now().time())
                
            elif nombre_sensor == "SensorEtiqueta":
                var.tiempo_fini.put(datetime.now().time())

            if nombre_sensor == "SensorCC":
                pass


def detectar_objeto(nombre_sensor, frame_name : str):
    """Detecta objetos que colisionan con un sensor en un frame concreto."""
    RDK = robolink.Robolink()
    
    sensor = RDK.Item(nombre_sensor)
    frame = RDK.Item(frame_name, robolink.ITEM_TYPE_FRAME)

    if not sensor.Valid():
        raise Exception("El sensor que me has pasado no existe en tu estación, revisa nombres")    

    if not frame.Valid():
        raise Exception("El frame que me has pasado no existe en tu estación, revisa nombres")
    
    detectados_anterior = set()

    while True:
        
        lista_objetos = frame.Childs()

        detectados_actuales = set()

        if lista_objetos:
            for idx in lista_objetos:
                if idx.Valid() and sensor.Collision(idx):
                    detectados_actuales.add(idx)

        entradas_nuevas = list(detectados_actuales - detectados_anterior)
        if entradas_nuevas:
            sim.setDO(nombre_sensor, 1)
            productorEvento(nombre_sensor, entradas_nuevas, RDK)
        else:
            sim.setDO(nombre_sensor, 0)
        
        detectados_anterior = detectados_actuales.copy()

        robomath.pause(0.01)
    