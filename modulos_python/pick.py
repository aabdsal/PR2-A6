from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox
from typing import Optional

RDK = robolink.Robolink()

from modulos_python import simulation, var

sistRefBending = RDK.Item("Bending", robolink.ITEM_TYPE_FRAME)
home = RDK.Item("Home", robolink.ITEM_TYPE_TARGET)
sistRefPick = RDK.Item("Pick", robolink.ITEM_TYPE_FRAME)

def _pick_plancha(prepick_str, pick_str : str):
    tool_yaskawa = "EPick Bend"
    r = RDK.Item("Yaskawa MH24", robolink.ITEM_TYPE_ROBOT)
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

    var.objetos_tcp[tool_yaskawa] = simulation.simulation_adjuntar_objeto(toolR)
    
    r.Pause(1000)
    r.MoveL(prepick)

    r.Pause(1000)

def pick_plancha_larga():
    """
        sustituir el if por un wait para que la fotocelula
        de la cinta detecte un objeto mediante el collision 
    """
    
    if var.detecta_larga:
        _pick_plancha("PrePickLargo", "PickLargo")
        var.detecta_larga = False

def pick_plancha_ancha():
    """
        sustituir el if por un wait para que la fotocelula
        de la cinta detecte un objeto mediante el collision 
    """

    if var.detecta_ancha:
        _pick_plancha("PrePickAncho", "PickAncho")
        var.detecta_ancha = False
    