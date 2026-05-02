"""Este archivo de python es también de gran utilidad, 
ya que realiza acciones importantes para la fluidez de la simulación en roboDK.

Se tienen implementadas metodos para ocultar, mostrar objetos, 
reemplazas posicion,adjuntar o soltar un objeto, simular una 
espera digital, establecer una salida digital y duplicar objetos.

Todo es gracias a la API de RoboDK que tiene funciones built-in 
muy útiles para conseguir información determindada de la estación
y modificar la estación en tiempo de ejecución."""

from robodk import robolink    
from robodk import robomath    
from typing import Optional

from modulos_python import variables

RDK = robolink.Robolink()

def ocultar_objeto(object_name: str):
    """Este método oculta el objeto que se le pasa por parámetro"""

    obj = RDK.Item(object_name, robolink.ITEM_TYPE_OBJECT)

    if not obj.Valid():
        raise Exception(RDK.ShowMessage("El nombre del objeto no existe"))

    obj.setVisible(False)

def mostrar_objeto(object_name: str):
    """Este método muestra el objeto que se le pasa por parámetro"""

    obj = RDK.Item(object_name, robolink.ITEM_TYPE_OBJECT)

    if not obj.Valid():
        raise Exception(RDK.ShowMessage("El nombre del objeto no existe"))

    obj.setVisible(True)

def reemplazar_pos_objeto(object_name, parent: str,  pose : robomath.Mat):
    """Este método tiene la intención de reemplazar la posición del objeto 
    que se le pasa por parametro, mediante su padre(frame) y la posicion 
    a la que queremos que vaya. Sin embargo, al hacer uso de objetos plantilla 
    no encuentro la necesidad de seguir manteniendo. 
    
    Aún esta por decidir el futuro de esta función, pero de momento no se usa en ninguna 
    parte del código, en principio solo se iva a usar para el reset, pero aún no esta implementado y no creo que lo haga - Ali Abdelhamid"""

    item = RDK.Item(object_name, robolink.ITEM_TYPE_OBJECT)
    if not item.Valid():
        raise Exception(RDK.ShowMessage("El nombre del objeto no existe"))

    parent_frame = RDK.Item(parent, robolink.ITEM_TYPE_TARGET)

    if not parent_frame.Valid():
        raise Exception(RDK.ShowMessage("No hay nada en objeto_parent"))

    item.setParentStatic(parent_frame)

    item.setPoseAbs(pose)

def adjuntar_objeto(tool_name: robolink.Item, object_name: Optional[str] = None):
    """Esta función es muy interesante porque adjunta el objeto el robot resolviendolo de dos 
    formas distintas. O mediante el padre de la herramienta o usando la funcion de la API de 
    RoboDK AttachClosest, esta segunda realmente es muy inútil para procedimientos donde hay 
    varios objetos cerca, por eso es más útil especificar el nombre del objeto a adjuntar 
    y ponerlo en el sistema de referncia de la herramienta del robot"""


    if object_name is not None:
        attached = RDK.Item(object_name, robolink.ITEM_TYPE_OBJECT)
        if not attached.Valid():
            raise Exception("No se ha adjuntado ningun objeto")

        attached.setParentStatic(tool_name)
    else:
        attached = tool_name.AttachClosest()

    if not attached.Valid():
        raise Exception("No se ha adjuntado ningun objeto")
    
    return attached

def soltar_objeto(tool_name: str, frame_name: robolink.Item):
    """Está funciópn tambien suelta objetos de dos formas distintas, 
    pero aqui nos aseguramos de que el objeto a soltar se encuentra 
    en la herramienta del robot en tiempo de ejecución mediante 
    un diccionario (tabla hash) con clave el nombre de la herramienta, 
    que debe de ser único y como valor el objeto adjuntado en la herramienta del robot."""

    if tool_name not in variables.objetos_tcp:
        return False

    obj = variables.objetos_tcp.get(tool_name)
    if obj is not None and obj.Valid():
        obj.setParentStatic(frame_name)

    tool = RDK.Item(tool_name, robolink.ITEM_TYPE_TOOL)
    if tool.Valid():
        tool.DetachAll(frame_name)

    variables.objetos_tcp.pop(tool_name, None)
    return True

def waitDI(param_name : str, valor : int):
    """Este método simula una espera digital mediante 
    un bucle con condicion de si un parametro esta a 0 o a 1,
    se realiza una pausa para que no vaya tan petado."""

    while int(RDK.getParam(param_name) or 0) != valor:
        robomath.pause(0.01)

def setDO(param_name: str, valor: int):
    """Este método tiene dos objetivos, guardar el parametros en el arhivo
    json y establecer el valor deseado al parametro de la estación."""

    variables.registrar_parametro_json(param_name)
    RDK.setParam(param_name, str(valor))

def duplicar_objeto(plantilla_name: str, frame_name: str):
    """Esta función crea un objeto duplicado a partir del nombre de un objeto 
    plantilla y lo establece en el sistema de referencia indicacdo en el parámtro frame_name.
    
    Este método es una mejora al código que nos dio Marina en AvanzaCinta.py ya que el hecho de usar 
    objetos plantilla que no se mueven nos elimina la preocupación de si un objeto 
    aún esta en el mismo frame y la posición a la que hay que ponerlo.
    
    Opcionalmente, también se contabiliza el numero de objetos duplicados a partir de una plantilla 
    para así tener información persistente en tiempo de ejecución.
    """

    plantilla_item = RDK.Item(plantilla_name, robolink.ITEM_TYPE_OBJECT)
    frame_item = RDK.Item(frame_name, robolink.ITEM_TYPE_FRAME)

    if not plantilla_item.Valid():
        raise RuntimeError(f"El objeto plantilla '{plantilla_name}' no existe. Revisa los nombres.")

    if not frame_item.Valid():
        raise RuntimeError(f"El frame de destino '{frame_name}' no existe. Revisa los nombres.")

    plantilla_item.Copy()
    
    pasted = RDK.Paste(frame_item)

    duplicado: Optional[robolink.Item] = None
    if isinstance(pasted, list):
        if len(pasted) == 0:
            raise Exception("No se pudo pegar el objeto duplicado.")
        duplicado = pasted[0]
    else:
        duplicado = pasted

    if duplicado is None or not duplicado.Valid():
        raise Exception("No se pudo crear el duplicado del objeto.")

    duplicado.setPoseAbs(plantilla_item.PoseAbs())
    duplicado.setVisible(True)

    param_name = "count_" + plantilla_name
    
    if RDK.getParam(param_name) is None:
        RDK.setParam(param_name, '0')

    count = int(RDK.getParam(param_name)) + 1
    RDK.setParam(param_name, str(count))
    
    nombre_base = plantilla_name.replace("plantilla_", "")
    duplicado.setName(f"{nombre_base}_{count}")
    
    return duplicado

