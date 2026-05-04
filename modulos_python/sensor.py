"""Este archivo implementa la lógica para que un sensor detecte objetos."""

from robodk import robolink    
from robodk import robomath    
from modulos_python import variables
from typing import List

from modulos_python import simulation

def productorEvento(nombre_sensor: str, detectados: List[robolink.Item], RDK : robolink.Robolink):
    """Añade objetos detectados a la cola del sensor y ajusta salidas digitales."""
    if detectados:

        simulation.setDO(nombre_sensor, 1)

        for idx in detectados:
            variables.objetos_pendientes[nombre_sensor].put(idx.Name())
            RDK.ShowMessage(f"objeto {idx.Name() } detectado en {nombre_sensor}", False)

        simulation.setDO(nombre_sensor, 0)

def detectar_objeto(nombre_sensor, frame_name : str):
    """Detecta objetos que colisionan con un sensor en un frame concreto.

    Usa ItemList y Parent para identificar objetos dentro del frame y
    comprobar colisiones sin conocer sus nombres previamente."""
    RDK = robolink.Robolink()
    
    sensor = RDK.Item(nombre_sensor)
    frame = RDK.Item(frame_name, robolink.ITEM_TYPE_FRAME)

    if not sensor.Valid():
        raise Exception("El sensor que me has pasado no existe en tu estación, revisa nombres")    

    if not frame.Valid():
        raise Exception("El frame que me has pasado no existe en tu estación, revisa nombres")
    
    detectados_anterior = set()

    while True:
        
        # La lista se podría cargar una vez fuera del while o refrescarla
        # bajo una condición, pero es optimización, no lógica.
        lista_objetos = RDK.ItemList(robolink.ITEM_TYPE_OBJECT, True)  

        detectados_actuales = set()

        for idx in lista_objetos:

            if isinstance(idx, str):
                idx = RDK.Item(idx)     

            if idx.Valid() and idx.Parent() == frame:
                if sensor.Collision(idx):
                    detectados_actuales.add(idx)
        
        entradas_nuevas = list(detectados_actuales - detectados_anterior)

        if entradas_nuevas:
            productorEvento(nombre_sensor, entradas_nuevas, RDK)
        
        detectados_anterior = detectados_actuales.copy()

        robomath.pause(0.01)
    