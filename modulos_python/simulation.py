from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox

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

def simulation_adjuntar_objeto(tool: robolink.Item):
    tool.AttachClosest()

def simulation_soltar_objeto(tool, frame: robolink.Item):
    tool.DetachClosest(frame)