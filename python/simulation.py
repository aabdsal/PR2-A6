from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox
RDK = robolink.Robolink()

def _resolve_tool(tool: robolink.Item | str | None = None) -> robolink.Item:
    if isinstance(tool, robolink.Item):
        return tool

    if isinstance(tool, str) and tool != "":
        return RDK.Item(tool, robolink.ITEM_TYPE_TOOL)

    return RDK.Item("", robolink.ITEM_TYPE_TOOL)


def simulation_ocultar_objeto(object_name: str):
    obj = RDK.Item(object_name, robolink.ITEM_TYPE_OBJECT)
    obj.setVisible(False)

def simulation_mostrar_objeto(object_name: str):
    obj = RDK.Item(object_name, robolink.ITEM_TYPE_OBJECT)
    obj.setVisible(True)

def simulation_adjuntar_objeto(tool: robolink.Item | str | None = None):
    gripper = _resolve_tool(tool)
    gripper.AttachClosest()

def simulation_soltar_objeto(tool: robolink.Item | str | None = None):
    gripper = _resolve_tool(tool)
    gripper.DetachClosest()

def simulation_reemplazar_pos_objeto(tool: robolink.Item | str | None = None):
    gripper = _resolve_tool(tool)
    #gripper.setPoseAbs()