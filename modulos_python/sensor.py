from robodk import robolink    
from robodk import robomath    
from modulos_python import var, simulation
from typing import List

def productorEvento(nombre_sensor: str, detectados: List[robolink.Item], RDK : robolink.Robolink):

    if detectados:

        simulation.setDO(nombre_sensor, 1)

        for idx in detectados:
            var.objetos_pendientes[nombre_sensor].put(idx)
            RDK.ShowMessage(f"objeto {idx.Name() } detectado en {nombre_sensor}", False)

def detectar_objeto(nombre_sensor, frame_name : str):

    RDK = robolink.Robolink()
    
    sensor = RDK.Item(nombre_sensor)
    frame = RDK.Item(frame_name, robolink.ITEM_TYPE_FRAME)

    if not sensor.Valid():
        raise Exception("El sensor que me has pasado no existe en tu estación, revisa nombres")    

    if not frame.Valid():
        raise Exception("El frame que me has pasado no existe en tu estación, revisa nombres")
    
    detectados_anterior = set()

    while True:
        
        """ 
            la lista se podria cargar solo una vez 
            fuera del while o refrescarla bajo una condicion
            pero es optimizacion, no logica.
        """
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
    