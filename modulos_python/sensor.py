"""Este archivo implementa la solución para que un sensor detecte cualquier objeto."""

from robodk import robolink    
from robodk import robomath    
from modulos_python import variables
from typing import List

from modulos_python import simulation

def productorEvento(nombre_sensor: str, detectados: List[robolink.Item], RDK : robolink.Robolink):
    """Este método mira si hay algún objeto nuevo detectado en la lista 
    y los añade a un diccionario que lleva como valor una cola de objetos pendientes, 
    que son utiles para que el robot yaskawa sepa que hay un objeto esperando a ser cogido.
    
    También establece salidas digitales para el correcto funcionamiento de las cintas."""
    if detectados:

        simulation.setDO(nombre_sensor, 1)

        for idx in detectados:
            variables.objetos_pendientes[nombre_sensor].put(idx.Name())
            RDK.ShowMessage(f"objeto {idx.Name() } detectado en {nombre_sensor}", False)

        simulation.setDO(nombre_sensor, 0)

def detectar_objeto(nombre_sensor, frame_name : str):
    """Este metodo es una gran solucion al problema de la simulacion en robodk, 
    ya que la api de robodk ofrece la funcion sensor.Collision(obj) el cual 
    devolvia si el sensor se habia chocado con un obj que tu mismo le pasas por parametro.
    
    Esto para un sensor es ineficiente, ya que el desconoce el nombre de los objetos 
    que van a pasar por delante de él. Asi que se ha implementado gracias a las funciones 
    .ItemList y .Parent una forma de que un sensor detecte todos los objetos de la cinta que colision con él.

    Se hace uso de algoritmos voraces y conjuntos se ha podido realizar esta operación.
    """
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
    