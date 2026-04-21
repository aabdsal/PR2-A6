from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox
from typing import Optional

from modulos_python import var
RDK = robolink.Robolink()

def simulation_ocultar_objeto(object_name: str):
    obj = RDK.Item(object_name, robolink.ITEM_TYPE_OBJECT)
    obj.setVisible(False)

def simulation_mostrar_objeto(object_name: str):
    obj = RDK.Item(object_name, robolink.ITEM_TYPE_OBJECT)
    obj.setVisible(True)

def simulation_reemplazar_pos_objeto(object_name: str):
    obj = RDK.Item(object_name, robolink.ITEM_TYPE_OBJECT)
    #obj.setPose()

def simulation_adjuntar_objeto(tool_name: robolink.Item, object_name: Optional[str] = None):
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

def simulation_soltar_objeto(tool_name: str, frame_name: robolink.Item):
    if tool_name not in var.objetos_tcp:
        return False

    obj = var.objetos_tcp.get(tool_name)
    if obj is not None and obj.Valid():
        obj.setParentStatic(frame_name)

    tool = RDK.Item(tool_name, robolink.ITEM_TYPE_TOOL)
    if tool.Valid():
        tool.DetachAll(frame_name)

    var.objetos_tcp.pop(tool_name, None)
    return True