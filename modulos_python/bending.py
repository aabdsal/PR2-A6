from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox
RDK = robolink.Robolink()

import simulation 

r = RDK.Item("Yaskawa MH24", robolink.ITEM_TYPE_ROBOT)
sistRefBend = RDK.Item("Press Brake Base", robolink.ITEM_TYPE_FRAME)
toolR = RDK.Item("EPick Bend", robolink.ITEM_TYPE_TOOL)

# principio
home = RDK.Item("Home", robolink.ITEM_TYPE_TARGET)
place1 = RDK.Item("Place1", robolink.ITEM_TYPE_TARGET)
bajaprensa1 = RDK.Item("Bajaprensa1", robolink.ITEM_TYPE_TARGET)

# mid bending
abreprensa1 = RDK.Item("AbrePrensa1", robolink.ITEM_TYPE_TARGET)
retract1 = RDK.Item("Retract1", robolink.ITEM_TYPE_TARGET)
gir180 = RDK.Item("Gir180", robolink.ITEM_TYPE_TARGET)

place2 = RDK.Item("Place2", robolink.ITEM_TYPE_TARGET)
bajaprensa2 = RDK.Item("Bajaprensa2", robolink.ITEM_TYPE_TARGET)

abreprensa2 = RDK.Item("AbrePrensa2", robolink.ITEM_TYPE_TARGET)
retract2 = RDK.Item("Retract2", robolink.ITEM_TYPE_TARGET)

def _transicion_objeto(obj_from: str, obj_to: str):
    simulation.simulation_ocultar_objeto(obj_from)
    simulation.simulation_mostrar_objeto(obj_to)
    simulation.simulation_soltar_objeto(toolR)
    simulation.simulation_adjuntar_objeto(toolR)


def _bending_generico(bend_1: str, bend_2: str, obj_0: str, obj_1: str, obj_2: str):

    r.setFrame(sistRefBend)
    r.setTool(toolR)

    r.MoveL(home.Pose())
    r.MoveL(bajaprensa1.Pose())
    r.Pause(2000)

    bend1 = RDK.Item(bend_1, robolink.ITEM_TYPE_TARGET)
    r.MoveL(bend1.Pose())

    _transicion_objeto(obj_0, obj_1)

    r.MoveL(abreprensa1.Pose())
    r.MoveL(retract1.Pose())
    r.Pause(2000)
    r.MoveL(gir180.Pose())
    r.MoveL(place2.Pose())
    r.MoveL(bajaprensa2.Pose())
    r.Pause(2000)

    bend2 = RDK.Item(bend_2, robolink.ITEM_TYPE_TARGET)
    r.MoveL(bend2.Pose())

    _transicion_objeto(obj_1, obj_2)

    r.MoveL(abreprensa2.Pose())
    r.MoveL(retract2.Pose())


def bending_plancha_larga():
    _bending_generico(
        bend_1="Bend1",
        bend_2="Bend2",
        obj_0="planchaLarga",
        obj_1="planchaLarga1",
        obj_2="planchaLarga2",
    )


def bending_plancha_ancha():
    _bending_generico(
        bend_1="BendA1",
        bend_2="BendA2",
        obj_0="planchaAncha",
        obj_1="planchaAncha1",
        obj_2="planchaAncha2",
    )
