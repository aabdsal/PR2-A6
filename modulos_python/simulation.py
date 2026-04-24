from robodk import robolink    
from robodk import robomath    
from typing import Optional

from modulos_python import var
RDK = robolink.Robolink()

def ocultar_objeto(object_name: str):
    obj = RDK.Item(object_name, robolink.ITEM_TYPE_OBJECT)
    obj.setVisible(False)

def mostrar_objeto(object_name: str):
    obj = RDK.Item(object_name, robolink.ITEM_TYPE_OBJECT)
    obj.setVisible(True)

def reemplazar_pos_objeto(object_name: str):
    item = RDK.Item(object_name, robolink.ITEM_TYPE_OBJECT)
    pose = var.objeto_pose[item.Name()]
    item.setPose(pose)

def adjuntar_objeto(tool_name: robolink.Item, object_name: Optional[str] = None):
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

def waitDI(param_name : str, valor : int):
    while int(RDK.getParam(param_name) or 0) != valor:
        robomath.pause(0.01)

def setDO(param_name: str, valor : int):
    RDK.setParam(param_name, str(valor))

