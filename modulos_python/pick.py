from robodk import robolink
from modulos_python import simulation, var

def _pick_plancha(prepick_str, pick_str : str):
    
    RDK = robolink.Robolink()
    
    sistRefBending = RDK.Item("Bending", robolink.ITEM_TYPE_FRAME)
    home = RDK.Item("Home", robolink.ITEM_TYPE_TARGET)
    sistRefPick = RDK.Item("Pick", robolink.ITEM_TYPE_FRAME)
    r = RDK.Item("Yaskawa MH24", robolink.ITEM_TYPE_ROBOT)

    tool_yaskawa = "EPick Bend"
    toolR = RDK.Item(tool_yaskawa, robolink.ITEM_TYPE_TOOL)
    
    r.setFrame(sistRefBending)
    r.setTool(toolR)
    
    r.MoveJ(home)
    r.setFrame(sistRefPick)

    prepick = RDK.Item(prepick_str, robolink.ITEM_TYPE_TARGET)
    pick = RDK.Item(pick_str, robolink.ITEM_TYPE_TARGET)

    r.MoveL(prepick)
    r.Pause(1000)
    r.MoveL(pick)

    var.objetos_tcp[tool_yaskawa] = simulation.adjuntar_objeto(toolR)
    
    r.Pause(1000)
    r.MoveL(prepick)

    r.Pause(1000)

def pick_plancha_larga():
    _pick_plancha("PrePickLargo", "PickLargo")

def pick_plancha_ancha():
    _pick_plancha("PrePickAncho", "PickAncho")
    