from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox

from modulos_python import simulation, var

tool_yaskawa = "EPick Bend"

def _transicion_objeto(obj_from, obj_to: str, frame, tool: robolink.Item):
    simulation.soltar_objeto(tool_yaskawa, frame)
    simulation.ocultar_objeto(obj_from)
    simulation.mostrar_objeto(obj_to)
    var.objetos_tcp[tool_yaskawa] = simulation.adjuntar_objeto(tool, obj_to)


def _bending_generico(bend_1: str, bend_2: str, obj_0: str, obj_1: str, obj_2: str):

    RDK = robolink.Robolink()

    r = RDK.Item("Yaskawa MH24 Prensado", robolink.ITEM_TYPE_ROBOT)
    sistRefBend = RDK.Item("Bending", robolink.ITEM_TYPE_FRAME)
    toolR = RDK.Item(tool_yaskawa, robolink.ITEM_TYPE_TOOL)

    # principio
    home = RDK.Item("Home", robolink.ITEM_TYPE_TARGET)
    place1 = RDK.Item("Place1", robolink.ITEM_TYPE_TARGET)
    bajaprensa1 = RDK.Item("BajaPrensa1", robolink.ITEM_TYPE_TARGET)

    # mid bending
    abreprensa1 = RDK.Item("AbrePrensa1", robolink.ITEM_TYPE_TARGET)
    retract1 = RDK.Item("Retract1", robolink.ITEM_TYPE_TARGET)
    gir180 = RDK.Item("Gir180", robolink.ITEM_TYPE_TARGET)

    place2 = RDK.Item("Place2", robolink.ITEM_TYPE_TARGET)
    bajaprensa2 = RDK.Item("BajaPrensa2", robolink.ITEM_TYPE_TARGET)

    abreprensa2 = RDK.Item("AbrePrensa2", robolink.ITEM_TYPE_TARGET)
    retract2 = RDK.Item("Retract2", robolink.ITEM_TYPE_TARGET)
    r.setFrame(sistRefBend)
    r.setTool(toolR)

    r.MoveL(home)
    r.MoveL(place1)
    r.MoveL(bajaprensa1)
    r.Pause(2000)

    bend1 = RDK.Item(bend_1, robolink.ITEM_TYPE_TARGET)
    r.MoveL(bend1)

    _transicion_objeto(obj_0, obj_1, sistRefBend, toolR)

    r.MoveL(abreprensa1)
    r.MoveL(retract1)
    r.Pause(2000)
    r.MoveJ(gir180)
    r.MoveJ(place2)
    r.MoveL(bajaprensa2)
    r.Pause(2000)

    bend2 = RDK.Item(bend_2, robolink.ITEM_TYPE_TARGET)
    r.MoveL(bend2)

    _transicion_objeto(obj_1, obj_2, sistRefBend, toolR)

    r.MoveL(abreprensa2)
    r.MoveL(retract2)

    simulation.setDO("BendingHecho", 1)

def bending_plancha_larga():
    _bending_generico("Bend1", "Bend2", "planxaLarga", "planchaLarga1", "planchaLarga2")

def bending_plancha_ancha():
    _bending_generico("BendA1", "BendA2", "planxaAncha", "planchaAncha1", "planchaAncha2")
