from robodk import robolink   
from modulos_python import var
from modulos_python import simulation

def _transicion_objeto(obj_from_plantilla, obj_to_plantilla: str, frame, tool: robolink.Item):
    
    RDK = robolink.Robolink()

    simulation.soltar_objeto(var.tool_yaskawa, frame)

    obj_from = RDK.Item(obj_from_plantilla)
    if not obj_from.Valid():
        raise RuntimeError("objeto no existe, revisa nombres")
    
    simulation.ocultar_objeto(obj_from.Name())
    obj_from.Delete() # ¡Importante! Elimina el objeto viejo.

    nuevo_objeto = simulation.duplicar_objeto(obj_to_plantilla, frame.Name())

    var.objetos_tcp[var.tool_yaskawa] = simulation.adjuntar_objeto(tool, nuevo_objeto.Name())
    
    return nuevo_objeto.Name()


def _bending_generico(bend_1: str, bend_2: str, obj_0: str, obj_1: str, obj_2: str):

    RDK = robolink.Robolink()

    r = RDK.Item(var.robot_yaskawa, robolink.ITEM_TYPE_ROBOT)
    sistRefBend = RDK.Item("Bending", robolink.ITEM_TYPE_FRAME)
    toolR = RDK.Item(var.tool_yaskawa, robolink.ITEM_TYPE_TOOL)

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

    nombre1 = _transicion_objeto(obj_0, obj_1, sistRefBend, toolR)

    r.MoveL(abreprensa1)
    r.MoveL(retract1)
    r.Pause(2000)
    r.MoveJ(gir180)
    r.MoveJ(place2)
    r.MoveL(bajaprensa2)
    r.Pause(2000)

    bend2 = RDK.Item(bend_2, robolink.ITEM_TYPE_TARGET)
    r.MoveL(bend2)

    _transicion_objeto(nombre1, obj_2, sistRefBend, toolR)

    r.MoveL(abreprensa2)
    r.MoveL(retract2)

    simulation.setDO("BendingHecho", 1)

def bending_plancha_larga(obj_name : str):
    _bending_generico("Bend1", "Bend2", obj_name, "plantilla_planchaLarga1", "plantilla_planchaLarga2")

def bending_plancha_ancha(obj_name : str):
    _bending_generico("BendA1", "BendA2", obj_name, "plantilla_planchaAncha1", "plantilla_planchaAncha2")
