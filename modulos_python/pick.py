from robodk import robolink
from modulos_python import simulation, var

def _pick_plancha(prepick_str, pick_str : str):
    
    RDK = robolink.Robolink()
    
    sistRefBending = RDK.Item(var.frame_bending, robolink.ITEM_TYPE_FRAME)
    sistRefPick = RDK.Item(var.frame_pick, robolink.ITEM_TYPE_FRAME)
    r = RDK.Item("Yaskawa MH24 Prensado", robolink.ITEM_TYPE_ROBOT)

    toolR = RDK.Item(var.tool_yaskawa, robolink.ITEM_TYPE_TOOL)
    
    r.setFrame(sistRefBending)
    r.setTool(toolR)
    
    home = RDK.Item("Home", robolink.ITEM_TYPE_TARGET)
    r.MoveJ(home)
    r.setFrame(sistRefPick)

    prepick = RDK.Item(prepick_str, robolink.ITEM_TYPE_TARGET)
    pick = RDK.Item(pick_str, robolink.ITEM_TYPE_TARGET)

    r.MoveL(prepick)
    r.Pause(1000)
    r.MoveL(pick)

    var.objetos_tcp[var.tool_yaskawa] = simulation.adjuntar_objeto(toolR)
    
    r.Pause(1000)
    r.MoveL(prepick)

    r.Pause(1000)

def pick_plancha_larga():
    _pick_plancha("PrePickLargo", "PickLargo")

def pick_plancha_ancha():
    _pick_plancha("PrePickAncho", "PickAncho")
    